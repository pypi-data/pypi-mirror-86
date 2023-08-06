import logging
import os
import functools
import datetime
import inspect
from enum import Enum
from typing import Callable, Any
import requests
import uvicorn

from fastapi import FastAPI, Body
from pydantic import create_model
from mvi.logger import setup_logging


setup_logging(logging.DEBUG)

logger = logging.getLogger(__name__)

MVI_MANAGER_URL = os.environ.get("MVI_MANAGER_URL", "http://host.docker.internal")
MVI_MANAGER_HOSTNAME = os.environ.get("MVI_MANAGER_HOSTNAME", "localhost")

MVI_SERVICE_NAME = os.environ.get("mvi.name", "unknown")
MVI_SERVICE_VERSION = os.environ.get("mvi.version", "0.0.0")
MVI_SERVICE_TOKEN = os.environ.get("mvi.auth", "unknown")


def get_headers() -> dict:
    """Generating headers for API calls

    Returns:
        dict: Assembled header
    """
    return {
        "Authorization": f"Bearer {MVI_SERVICE_TOKEN}",
        "Content-Type": "application/json",
        "Host": MVI_MANAGER_HOSTNAME,
    }


class Severity(Enum):
    INFO = 0
    WARNING = 1
    CRITICAL = 2


class MviService:
    def __init__(self):
        self.app = FastAPI(
            root_path=f"/services/{MVI_SERVICE_NAME}_{MVI_SERVICE_VERSION}",
            title=f"{MVI_SERVICE_NAME} {MVI_SERVICE_VERSION}",
            description="Automatically generated, interactive API documentation",
        )
        self.parameters_endpoints = {}
        self.app.get("/~parameters")(self.get_all_parameters)

    def get_all_parameters(self) -> dict:
        """Get all registered parameter endpoints

        \f
        Returns:
            dict: The registered parameters and their current value
        """
        return self.parameters_endpoints

    def get_parameter(self, parameter: str) -> Any:
        """Get specific parameter

        Args:
            parameter (str): The name of the parameter

        Returns:
            Any: The value of the parameter
        """
        return self.parameters_endpoints[parameter]

    def add_parameter(self, parameter: str, value: Any):
        """Adds a parameter to the parameter endpoints.

        Args:
            parameter (str): The name of the parameter
            value: (Any) The value of the parameter

        Returns:
            dict: The parameter and its value
        """
        path = f"/~parameters/{parameter}"

        update_request = create_model(
            f"{parameter}_schema", value=(value.__class__, ...)
        )

        def update_parameter(update_request: update_request):
            self.parameters_endpoints[parameter] = update_request.value
            return {parameter: update_request.value}

        def get_parameter():
            return self.parameters_endpoints[parameter]

        self.parameters_endpoints[parameter] = value

        # Register GET and POST endpoints for the new parameter
        self.app.get(path)(get_parameter)
        self.app.post(path)(update_parameter)
        return {parameter: value}

    def run(self):
        """Runs the service

        This method is usually called at the end of the module when all
        entrypoints etc for the service has been specified
        """
        uvicorn.run(self.app, host="0.0.0.0", port=8000)

    def entrypoint(self, func: Callable = None, **fastapi_kwargs) -> Callable:
        """Registers a function as an entrypoint, which will make it reachable
        as an HTML method on your host machine.

        Decorate a function with this method to create an entrypoint for it::

            @mvi.entrypoint
            def my_function(arg1:type1) -> type2:
                ....

        It is strongly recommended to include types of the arguments and return
        objects for the decorated function.

        Args:
            func (Callable): The decorated function to make an entrypoint for.
            **fastapi_kwargs: Keyword arguments for the resulting API endpoint.
                See FastAPI for keyword arguments of the ``FastAPI.post()`` function.

        Raises:
            TypeError: If :obj:`func` is not callable.

        Returns:
            Callable: The decorated function: :obj:`func`.
        """
        # pylint: disable=protected-access
        def entrypoint_decorator(deco_func):
            path = f"/{deco_func.__name__}"
            signature = inspect.signature(deco_func)

            # Update default values to fastapi Body parameters to force all parameters
            # in a json body for the resulting HTML method
            new_params = []
            for parameter in signature.parameters.values():
                if parameter.default == inspect._empty:
                    default = Ellipsis
                else:
                    default = parameter.default
                new_params.append(parameter.replace(default=Body(default, embed=True)))
            signature = signature.replace(parameters=new_params)

            @functools.wraps(deco_func)
            def wrapper(*args, **kwargs):
                return deco_func(*args, **kwargs)

            wrapper.__signature__ = signature

            # Get response_model from return type hint
            return_type = signature.return_annotation
            if return_type == inspect._empty:
                return_type = None

            # Give priority to explicitly given response_model
            kwargs = dict(response_model=return_type)
            kwargs.update(fastapi_kwargs)

            # Create API endpoint
            self.app.post(path, **kwargs)(wrapper)

            return deco_func

        # This ensures that we can use the decorator with or without arguments
        if not (callable(func) or func is None):
            raise TypeError(f"{func} is not callable.")
        return entrypoint_decorator(func) if callable(func) else entrypoint_decorator


def call_service(
    service_name: str,
    method_name: str,
    arguments: dict = None,
    service_version: str = None,
) -> Any:
    """Call a method in a different service.

    Example usage::

        data = call_service(
            service_name="data_connector",
            method_name= "get_data",
        )

    Args:
        service_name (str): The service which contains the method to call.
        method_name (str): The name of the method to call.
            This method needs to be declared as an 'mvi entrypoint' in the
            other service.
            The return object(s) of this 'method' must be jsonable, i.e pass FastAPI's
            jsonable_encoder, otherwise this method won't be reachable.
        arguments (dict): Arguments to the method.
            In the form: {"argument_name": value, ...}. Default None.
        service_version (str): The specific version of the service to call.
            Default None, the main version and the shadows versions will be called.

    Returns:
        Any: The output from the method in the other service.
    """
    if service_version:
        url = (
            f"{MVI_MANAGER_URL}/services/"
            + f"{service_name}_{service_version}/{method_name}"
        )
    else:
        url = f"{MVI_MANAGER_URL}/services/{service_name}/{method_name}"

    arguments = arguments if arguments else {}

    if service_version:
        logger.info(
            f"Calling method: {method_name} in service:"
            + f"{service_name} ({service_version}) with: {arguments}"
        )
    else:
        logger.info(
            f"Calling method: {method_name} in service:"
            + f"{service_name} with: {arguments}"
        )
    logger.info(f"Sending POST request to: {url}")
    response = requests.request("POST", url=url, headers=get_headers(), json=arguments)
    logger.info(f"Response from method: {response.text}, code: {response.status_code}")
    return response.json()


def notify(msg: str, severity: Severity, dashboard=True, email=False, timer=0):
    """Generates and sends a notification

    Args:
        msg (str): The message to include for the recipient of the notification.
        severity (Severity): The severity of the notification.
        dashboard (bool, optional): If this is True, the notification will be shown
            on the mvi dashboard. Defaults to True.
        email (bool, optional): If this is True, the notification will be send as
            an email based on the email configuration. Defaults to False.
        timer (int, optional): The amount of time (in seconds) that has to pass
            before the same notification can be send again. Defaults to 0.
    """
    url = f"{MVI_MANAGER_URL}/notifications/"

    timer = 0 if timer < 0 else timer

    payload = {
        "service_name": MVI_SERVICE_NAME,
        "service_version": MVI_SERVICE_VERSION,
        "msg": msg,
        "severity": severity.value,
        "dashboard": dashboard,
        "email": email,
        "timer": timer,
        "timestamp": str(datetime.datetime.utcnow()),
    }

    logger.info(f"Notification was posted: {payload} to url: {url}")
    requests.request("POST", url, headers=get_headers(), json=payload)

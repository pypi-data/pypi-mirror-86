# MVI project: {{cookiecutter.project_name}}

# Creating the service
The ```service.py``` contains an example service and shows how to use the mvi SDK.

This example shows:
 - How to initiate an mvi service
 - How to register changeable parameters
 - How to register functions as entrypoints
 - How to log from the service
 - How to send notifications from the service
 - How to start the service

If the service requires external packages, they should be specified in the `requirements.txt` file.
# Deploying the service
The service can be deployed using the mvi command-line interface:

If this is a local project (mvi converts your project into a tar file which is then deployed):

```mvi deploy myservice 0.0.1 --tar {path_to_project} ```

If this project is a git repo:

```mvi deploy myservice 0.0.1 {git_url}```

# Documentation
Full documentation of the SDK and the CLI can be found here: TODO: insert link to documentation.

# Extra
If you want to change name of the service file ```service.py```, or deploy another file as the
mvi service then you have to change the ```APP_FILE``` key in the ```.s2i/environment``` file.
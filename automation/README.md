# Automation

- [Entry Point](#entry-point)
- [Modules](#modules)
  - [Slack](#slack)
    - [Slack API](#slack-api)
    - [Slack Bot](#slack-bot)
    - [Slack Configuration](#slack-configuration)
    - [Slack Features](#slack-features)
      - [channels](#channels)
  - [Azure DevOps](#azure-devops)
    - [Azure DevOps API](#azure-devops-api)
    - [Azure DevOps PAT Token](#azure-devops-pat-token)
    - [Azure DevOps Configuration](#azure-devops-configuration)
    - [Azure DevOps Features](#azure-devops-features)
      - [projects](#projects)
- [Secrets](#secrets)
- [Notes](#notes)

This folder will contain scripts that can be used to automate much of the setup of an organization based on the configuration generated by the `teamconfig` project.

```text
DISCLAIMER: This script is just a proof of concept right now. Apologies in advanced - my python skills are a little rusty.
```

## Entry Point

The entry point for this script is `program.py` which is located in the project root folder (`~/automation`). This file is responsible for setting the context of the script, creating all the dependencies for the different modules and initializing the modules themselves.

## Modules

A module represents an integration with a service that a company might want to automate, based on the teams configuration in the `~/teams` folder.

When creating a module, ensure that it inherits the Abstract Base Class (ABC) `Runnable` located in the `~/automation/modules/base.py` and that it implements the abstract `run()` method. This will make it easier to hook up in the `program.py` script.

### Slack

#### Slack API

This module will make use of the RESTful [Slack API](https://api.slack.com/docs). In order to integrate with Slack, we are required to create an app to act as an identity which will make changes to your workspace on your behalf via the API.

#### Slack Bot

As previously mentioned, you need to create a Slack app, which is a bot you can you to authenticate and work with the API with.

You can create a slack app / bot for free using [this guide](https://api.slack.com/authentication/basics). Once created, install to your workspace. It is private to your organization.

You can create this app manually using the UI as described in the guide. Alternatively, if you'd like this application to be defined in code and live in source control, you can also create an app [here](https://api.slack.com/apps?new_app=1) using an app manifest (hit 'Create New App' and hit 'From an app manifest'). An example app manifest would be:

```yml
display_information:
  name: workspace-admin
features:
  bot_user:
    display_name: workspace-admin
    always_online: false
oauth_config:
  scopes:
    bot:
      - channels:manage
      - channels:read
      - groups:read
      - im:read
      - mpim:read
settings:
  org_deploy_enabled: false
  socket_mode_enabled: false
  token_rotation_enabled: false
```

The app will need to be given specific permissions (scopes) in order for this script to make use of it. Under the 'Features > OAuth & Permissions > Scopes' section, add the following:

```text
channels:manage
channels:read
groups:read
im:read
mpim:read
```

Once the app is created and installed onto your workspace, take the bot token from the 'Oauth & Permissions' screen and place in slack section of the `automation.config.json` file for this app (see next section).

#### Slack Configuration

In order to use this module, you will need to create/update the `automation.config.json` file in the `~/automation` directory and add a new module (if one doesn't exist already) like this:

```json
{
    "modules": {
        "slack": {
            "config": {
                "API_TOKEN": "xoxb-XXX..."
            },
            "features": [
              // feature objects here
            ]
        }
    }
}
```

Once you've got your [bot token](#slack-bot), you can put it in the `modules:slack:config:API_TOKEN` field.

There is also a features section. This allows to to configure specific functionality in a particular module. If a feature is not specified here, it will not be executed. See next section for further details.

This config file has been excluded in the `.gitignore` file. You can make a copy of the `automation.config.example.json` file to get a template and remove the `example` part from the file name.

#### Slack Features

##### channels

This feature will automate the generation of slack channels based on the `teamconfig` output and uses the [Slack Conversations API](https://api.slack.com/methods/conversations.create).

To enable this feature, put the following object in the `modules:slack:features` array in the `automation.config.json` file:

```json
{
    "name": "channels"
}
```

This module does not require any feature specific settings.

### Azure DevOps

#### Azure DevOps API

This module will make use of the RESTful [Azure Devops API](https://docs.microsoft.com/en-us/rest/api/azure/devops/?view=azure-devops-rest-7.1&viewFallbackFrom=azure-devops-rest-6.0). In order to integrate with Azure DevOps, we are required to create a PAT token with the appropriate permissions / scopes which we can use to make changes to your Azure DevOps organization.

#### Azure DevOps PAT Token

You can create an Azure DevOps PAT token using this [guide](https://docs.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate?view=azure-devops&tabs=Windows).

To run this script, the token will need the following permissions / scopes:

```text
Project and Team (Read, Write & Manage)
```

#### Azure DevOps Configuration

In order to use this module, you will need to create/update the `automation.config.json` file in the `~/automation` directory and add a new module (if one doesn't exist already) like this:

```json
{
    "modules": {
        "azdevops": {
            "config": {
                "PAT_TOKEN": "",
                "Organisation": ""
            },
            "features": [
              // feature objects here
            ]
        }
    }
}
```

Once you've got your [PAT Token](#azure-devops-pat-token), you can put it in the `modules:azdevops:config:API_TOKEN` field. You will also need to specify your Azure DevOps organization in the `modules:azdevops:config:Organisation` field.

There is also a features section. This allows to to configure specific functionality in a particular module. If a feature is not specified here, it will not be executed. See next section for further details.

This config file has been excluded in the `.gitignore` file. You can make a copy of the `automation.config.example.json` file to get a template and remove the `example` part from the file name.

#### Azure DevOps Features

##### projects

This feature will automate the generation of Azure DevOps projects based on the `teamconfig` output and uses the [Azure DevOps API](https://docs.microsoft.com/en-us/rest/api/azure/devops/core/projects/create?view=azure-devops-rest-6.0)

To enable this feature, put the following object in the `modules:azdevops:features` array in the `automation.config.json` file:

```json
{
    "name": "projects",
    "settings": {
        "type": "6B724908-EF14-45CF-84F8-768B5384DA45"
    }
}

```

This module requires feature specific settings. Specifically, it needs to know what type of project to create. In the above example, the Agile Scrum project type is used. Other project types can be found [here](https://azure.microsoft.com/en-gb/resources/templates/visual-studio-team-services-project-create/).

### Secrets

We could plumb this script into a CI/CD pipeline that will run every time the `~/teams` folder in the project root is updated.

If this is the case, you should make the tokens a pipeline secret and replace the relevant fields in the `~/automation/automation.config.json` as part of the pipeline.

### Notes

At this time, this script doesn't treat this project as declarative. Therefore changes to teams data, such as channel names, will result in new channels being created as opposed to being renamed.

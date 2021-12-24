## Description

This product aims to programtiallcy create a Teams API for an entire organisation based on the [Team API](https://github.com/TeamTopologies/Team-API-template) put forward by [team topologies](https://teamtopologies.com/).
From this information and schema the goal is to validate the team setup based on business rules and also create automatic documentation.
The schema for the teams can be found in [teams.schema.json](/teams.schema.json) and an example implementation of team in [teams.json](/teams.json).
The example documentation this produces can be found in [docs/index.html](docs/index.html) to see the raw html, or to see it rendered as it currently is in the repo go [here](https://htmlpreview.github.io/?https://raw.githubusercontent.com/griff182uk/teamconfig/master/docs/index.html).

## Dependencies

* Pyton Installation
* [json2table](https://pypi.org/project/json2table/)
* [jsonschema](https://pypi.org/project/jsonschema/)

## Guide

To perform any of the actions below using the python code in this repo:

* Clone the repo to your machine.
* Activate the virtual python environment.

```bash
venv\scripts\activate
```

### How to Validate Teams Schema

* Within your virtual python environment, open a terminal and run [app/validate.py](app/validate.py). This should produce no errors and return the message "Schema validation passed".

```
(venv) D:\repos\teamconfig>app\validate.py      
Schema validation passed.
```

### How to Generate Documentation

* Within your virtual python environment, open a terminal and run [app/generate_docs.py](app/generate_docs.py). This will replace the html found in [docs/docs.html](docs/docs.html) with the current teams configuration. It should produce no errors and return the message "Docs created in docs/docs.html".

```
(venv) D:\repos\teamconfig>app\generate_docs.py 
Docs created in docs/docs.html
```

To preview this on github itself you can use this [example](https://htmlpreview.github.io/?https://raw.githubusercontent.com/griff182uk/teamconfig/master/docs/docs.html) to see it in the current repo, or g to [htmlpreview](https://htmlpreview.github.io/) for github.io and enter the URL of your own.

### How to Add Teams

To add a team you need to add information to the [teams.json](/teams.json) file that matches the schema of the [teams.schema.json](/teams.schema.json).
Once you have added a team you should [validate](#how-to-validate-teams-schema) the teams against the schema again to ensure no rules have been broken.

### How to Style Documentation

If you want to amend the style of the documentation, edit the [docs/docs.css](docs/docs.css) file with the styling you require.

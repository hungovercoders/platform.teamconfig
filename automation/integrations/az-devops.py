import os
import requests
import json
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_DIR)
import base

class AzureDevOpsManager(base.Runnable):
    def __init__(self, config, dataMapper):
        self.config = config
        self.dataMapper = dataMapper

    def run(self):
        self.generate_projects()

    def generate_projects(self):
        print('Generating Azure DevOps projects..')

        organization = self.config.get_config_value('Organisation')
        baseUrl = f'https://dev.azure.com/{organization}/_apis/projects?api-version=6.0'
        apiToken = self.config.get_config_value('PAT_TOKEN')
        headers = {'Authorization': f'Basic {apiToken}'}
        teamsDataPath = os.path.join('teams', '*.json')
        teamsData = self.dataMapper.extract_comms_data_for_medium(teamsDataPath, 'slack')

        for team in teamsData:
            print(f'Generating Azure DevOps project for {team.name}..')

            body = {
                "name": team.name,
                "description": "This is a new project using the Scrum working process",
                "capabilities": {
                    "versioncontrol": {
                        "sourceControlType": "Git"
                    },
                    "processTemplate": {
                        "templateTypeId": "6B724908-EF14-45CF-84F8-768B5384DA45" # Uses Agile Scrum template
                    }
                }
            }

            bodyJson = json.dumps(body, indent=4)

            response = requests.post(url, data=bodyJson, headers=headers)

            if (not response.status_code == 200 and response.text.__contains__("TF200019")):
                print(f"Project {team.name} already exists")
                continue
            elif (response.status_code in (203, 401)):
                print(f'Token used may not have the following scopes configured: vso.project_manage')
                print('See docs here for further details: https://docs.microsoft.com/en-us/rest/api/azure/devops/core/projects/create?view=azure-devops-rest-6.0#scopes')
                exit()
            elif (not response.status_code == 200):
                print(f'Something went wrong creating {team.name} project. Reason: {response.reason}: {response.text}. Exiting script.')
                exit()
            else:
                print(f"Done generating Azure DevOps project for {team.name}.")

        print('Azure DevOps projects generated.')
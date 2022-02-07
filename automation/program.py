import os
from mappers import mappers
from integrations import slack, azdevops
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from lib import utils

def set_context():
    scriptDirectory = os.path.dirname(os.path.abspath(__file__))
    repoRootDirectory = os.path.dirname(scriptDirectory)

    print(f'Changing directory to desired root folder.')
    os.chdir(repoRootDirectory)
    print(f'Context changed to: {repoRootDirectory}')

def start_up():
    integrationsFolder = os.path.join('automation', 'integrations')
    stringUtils = utils.StringUtils()
    fileLoader = utils.FileLoader()
    teamConfigDataMapper = mappers.TeamConfigCommunicationDataMapper(fileLoader, stringUtils)
    
    slackConfigFile = os.path.join(integrationsFolder, 'slack.config.json')
    slackConfig = utils.ConfigurationLoader(fileLoader, slackConfigFile)
    slackManagerApp = slack.SlackManagerApp(slackConfig, teamConfigDataMapper)
    
    azDevopsConfigFile = os.path.join(integrationsFolder, 'azdevops.config.json')
    azDevopsConfig = utils.ConfigurationLoader(fileLoader, azDevopsConfigFile)
    azDevopsManagerApp = azdevops.AzureDevOpsManager(azDevopsConfig, teamConfigDataMapper)
    
    return {
        "stringUtils": stringUtils,
        "fileLoader": fileLoader,
        "teamConfigDataMapper": teamConfigDataMapper,
        "config": slackConfig,
        "slackApp": slackManagerApp,
        "devopsApp": azDevopsManagerApp,
        "modules": [slackManagerApp, azDevopsManagerApp]
    }

def run():
    set_context()
    services = start_up()
    modules = services["modules"]
    for module in modules:
        module.run()

run()
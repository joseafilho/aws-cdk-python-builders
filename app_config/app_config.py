import sys
import yaml
from yaml.loader import SafeLoader
from constructs import Construct

class AppConfig():

    def __init__(self, enviroment: str):
        with open('./config/' + enviroment + '.yaml') as f:
            config = yaml.load(f, Loader=SafeLoader)

        self.__enviroment = config['enviroment']
        self.__enviroment_full_name = config['enviroment_full_name']
        self.__loja_subdomain = config['loja_subdomain']

    @property
    def enviroment(self) -> str:
        return self.__enviroment

    @property
    def enviroment_full_name(self) -> str:
        return self.__enviroment_full_name

    @property
    def loja_subdomain(self) -> str:
        return self.__loja_subdomain

class AppConfigBuilder():

    @staticmethod
    def get_config(scope: Construct) -> AppConfig:
        env = scope.node.try_get_context('config')

        if not env:
            gettrace = getattr(sys, 'gettrace', None)

            if gettrace():
                env = 'dev'
            else:
                raise Exception('Context variable missing on CDK command. Pass in as "-c config=[dev|prod]"')

        if env not in ['dev', 'prod']:
            raise Exception('Context invalid. Pass in as "-c config=[dev|prod]"')

        return AppConfig(env)

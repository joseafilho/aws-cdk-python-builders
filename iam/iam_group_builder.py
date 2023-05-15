from aws_cdk import (
    aws_iam as iam,
)

from constructs import Construct
from libraries.app_config.app_config import AppConfigBuilder

class IAMGroupBuilder():

    @property
    def group(self) -> iam.IGroup:
        return self.__iam_group
    
    def __init__(self, scope: Construct, id: str):
        self.__scope = scope
        self.__app_config = AppConfigBuilder.get_config(self.__scope)
        self.__id = id + f'-grp-{self.__app_config.enviroment}'
        self.__create_group()
    
    def __create_group(self):
        self.__iam_group = iam.Group(
            self.__scope, self.__id,            
            group_name = self.__id            
        )

        

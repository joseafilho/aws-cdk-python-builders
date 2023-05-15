from aws_cdk import (
    aws_logs as logs,
    Tags
)

from constructs import Construct
from libraries.app_config.app_config import AppConfigBuilder

class LogGroupBuilder():

    @property
    def log_group(self) -> logs.ILogGroup:
        return self.__log_group

    def __init__(self, scope: Construct, id: str, log_group_name: str, log_retention: logs.RetentionDays) -> None:
        self.__scope = scope
        self.__app_config = AppConfigBuilder.get_config(self.__scope)
        self.__id = id + f'-lg-{self.__app_config.enviroment}'
        self.__log_group_name = log_group_name
        self.__log_retention = log_retention

        self.__create_log_group()

    def __create_log_group(self):
        self.__log_group = logs.LogGroup(
            self.__scope, self.__id,
            log_group_name = self.__log_group_name,
            retention = self.__log_retention
        )

        Tags.of(self.__log_group).add('Name', self.__id)

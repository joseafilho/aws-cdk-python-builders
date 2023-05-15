from aws_cdk import (
    aws_ecr as ecr,
    Tags,
    Duration
)

from constructs import Construct
from libraries.app_config.app_config import AppConfigBuilder

class ECRBuilder():

    @property
    def repository(self) -> ecr.IRepository:
        return self.__repository

    def __init__(self, scope: Construct, id: str) -> None:
        self.__scope = scope
        self.__app_config = AppConfigBuilder.get_config(self.__scope)
        self.__id = id + f'-ecr-{self.__app_config.enviroment}'
        self.__create_life_cycle()
        self.__create_ecr()

    def __create_life_cycle(self):
        self.__life_cycle = ecr.LifecycleRule(
            description = 'Remove untagged images.',
            tag_status = ecr.TagStatus.UNTAGGED,
            max_image_age = Duration.days(1)
        )

    def __create_ecr(self):
        self.__repository = ecr.Repository(
            self.__scope, self.__id,
            repository_name = self.__id,
            lifecycle_rules = [self.__life_cycle]
        )

        Tags.of(self.__repository).add('Name', self.__id)

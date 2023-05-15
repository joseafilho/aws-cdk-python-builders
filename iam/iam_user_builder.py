from aws_cdk import (
    aws_iam as iam
)

import aws_cdk as cdk
from constructs import Construct
from libraries.app_config.app_config import AppConfigBuilder

class IAMUserBuilder():

    @property
    def user(self) -> iam.IUser:
        return self.__iam_user

    def __init__(self, scope: Construct, id: str, generate_access_key: bool = False, show_secret_key: bool = False):
        self.__scope = scope
        self.__app_config = AppConfigBuilder.get_config(self.__scope)
        self.__id = id + f'-usr-{self.__app_config.enviroment}'
        self.__show_secret_key = show_secret_key

        self.__create_user()

        if generate_access_key:
            self.__create_access_keys()

    def __create_user(self):
        self.__iam_user = iam.User(
            self.__scope, self.__id,
            user_name = self.__id
        )

    def __create_access_keys(self):
        accessKey = iam.CfnAccessKey(
            self.__scope, self.__id + 'ak',
            user_name = self.__iam_user.user_name
        )

        # Output of the secretAccessKey.
        if self.__show_secret_key:
            cdk.CfnOutput(
                self.__scope, 'secretAccessKey',
                value = accessKey.attr_secret_access_key
            )

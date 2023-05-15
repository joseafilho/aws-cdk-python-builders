from constructs import Construct
from aws_cdk import Tags

from aws_cdk import (
    aws_ecs as ecs,
    aws_ec2 as ec2
)

from libraries.app_config.app_config import AppConfigBuilder

class ECSClusterBuilder():

    @property
    def cluster(self) -> ecs.ICluster:
        return self.__cluster

    def __init__(self, scope: Construct, id: str, vpc: ec2.IVpc) -> None:
        self.__scope = scope
        self.__app_config = AppConfigBuilder.get_config(self.__scope)
        self.__id = id + f'-cluster-{self.__app_config.enviroment}'
        self.__vpc = vpc

        self.__create_cluster()

    def __create_cluster(self):
        self.__cluster = ecs.Cluster(
            self.__scope, self.__id,
            cluster_name = self.__id,
            vpc = self.__vpc,
            container_insights = True
        )

        Tags.of(self.__cluster).add('Name', self.__id)

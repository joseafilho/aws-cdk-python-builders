from aws_cdk import (
    aws_ecs as ecs,
    aws_ec2 as ec2,
    Tags,
    Duration
)

from constructs import Construct
from libraries.app_config.app_config import AppConfigBuilder

class ECSServiceBuilder():

    @property
    def service(self) -> ecs.FargateService:
        return self.__service

    def __init__(self, scope: Construct, id: str, task_definition: ecs.ITaskDefinition, cluster: ecs.ICluster, sg: ec2.ISecurityGroup,
        desired_count: int, enable_execute_command: bool = False, health_check_grace_period_in_seconds: int = None) -> None:

        self.__scope = scope
        self.__app_config = AppConfigBuilder.get_config(self.__scope)
        self.__id = id + f'-service-{self.__app_config.enviroment}'
        self.__task_definition = task_definition
        self.__cluster = cluster
        self.__sg = sg
        self.__desired_count = desired_count
        self.__enable_execute_command = enable_execute_command
        self.__health_check_grace_period_in_seconds = None if not health_check_grace_period_in_seconds else Duration.seconds(health_check_grace_period_in_seconds)

        self.__create_service()

    def __create_service(self):
        self.__service = ecs.FargateService(
            self.__scope, self.__id,
            task_definition = self.__task_definition,
            cluster = self.__cluster,
            service_name = self.__id,
            desired_count = self.__desired_count,
            health_check_grace_period = self.__health_check_grace_period_in_seconds,
            security_groups = [self.__sg],
            assign_public_ip = True,
            enable_execute_command = self.__enable_execute_command,
            circuit_breaker = ecs.DeploymentCircuitBreaker(
                rollback = True
            )
        )

        Tags.of(self.__service).add('Name', self.__id)

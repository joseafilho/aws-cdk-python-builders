from typing import (
    Mapping,
    Optional,
    Sequence
)

from aws_cdk import (
    aws_ecs as ecs,
    aws_ecr as ecr,
    aws_logs as logs,
    aws_iam as _iam,
    Tags
)

from constructs import Construct
from libraries.app_config.app_config import AppConfigBuilder
from libraries.cloud_watch.log_group_builder import LogGroupBuilder
from libraries.utils.system_consts import SystemConsts

class FargateTaskDefinitionBuilder():

    @property
    def definition(self) -> ecs.FargateTaskDefinition:
        return self.__task_definition

    def __init__(self, scope: Construct, id: str, cpu: int, memory_limit: int, port_mapping: int, task_role: _iam.IRole = None,
        execution_role: _iam.IRole = None,  repository: ecr.IRepository = None, image_name_docker_hub: str = '', tag_image: str = 'latest',
        env_vars: Optional[Mapping[str, str]] = None, entry_point: Optional[Sequence[str]] = None, command: Optional[Sequence[str]] = None,
        family: Optional[str] = None, log_group_name: Optional[str] = None) -> None:

        self.__id_source = id
        self.__scope = scope
        self.__app_config = AppConfigBuilder.get_config(self.__scope)
        self.__id = id + f'-task-def-{self.__app_config.enviroment}'
        self.__repository = repository
        self.__cpu = cpu
        self.__memory_limit = memory_limit
        self.__port_mapping = port_mapping
        self.__task_role = task_role
        self.__execution_role = execution_role
        self.__image_name_docker_hub = image_name_docker_hub
        self.__tag_image = tag_image
        self.__env_vars = env_vars
        self.__entry_point = entry_point
        self.__command = command
        self.__family = family
        self.__log_group_name = log_group_name

        self.__create_task_definition()

    def __create_task_definition(self):
        self.__task_definition = ecs.FargateTaskDefinition(
            self.__scope, self.__id,
            cpu = self.__cpu,
            memory_limit_mib = self.__memory_limit,
            family = self.__family,
            task_role = self.__task_role,
            execution_role = self.__execution_role
        )

        if self.__repository:
            image_task = ecs.ContainerImage.from_ecr_repository(
                repository = self.__repository,
                tag = self.__tag_image
            )
        else:
            image_task = ecs.ContainerImage.from_registry(self.__image_name_docker_hub)

        self.__task_definition.add_container(
            self.__id + '-ctn',
            image = image_task,
            environment = self.__env_vars,
            entry_point = self.__entry_point,
            command = self.__command,
            port_mappings = [
                ecs.PortMapping(
                    container_port = self.__port_mapping,
                    host_port = self.__port_mapping
                )
            ],
            logging = ecs.LogDriver.aws_logs(
                log_group = LogGroupBuilder(
                    self.__scope, self.__id_source,
                    log_group_name = self.__log_group_name,
                    log_retention = logs.RetentionDays.ONE_DAY if self.__app_config.enviroment == SystemConsts.DEV_ENVIROMENT_ID else logs.RetentionDays.ONE_WEEK

                ).log_group,
                stream_prefix = '/ecs'
            )
        )

        Tags.of(self.__task_definition).add('Name', self.__id)

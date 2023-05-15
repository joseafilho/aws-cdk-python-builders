import typing

from aws_cdk import (
    aws_iam as iam,
    Tags
)

from aws_cdk.aws_iam import (
    IManagedPolicy,
    IRole
)

from constructs import Construct
from libraries.app_config.app_config import AppConfigBuilder

class RoleBuiler():

    @property
    def role(self) -> IRole:
        return self.__role

    def __init__(self, scope: Construct, id: str, service_principal: str, aws_policy_names: typing.Optional[typing.Sequence[str]] = None, aws_policy: IManagedPolicy = None):
        self.__scope = scope
        self.__app_config = AppConfigBuilder.get_config(self.__scope)
        self.__id = id + f'-role-{self.__app_config.enviroment}'
        self.__service_principal = service_principal
        self.__aws_policy_names = aws_policy_names
        self.__aws_policy = aws_policy

        self.__crete_managed_policies()
        self.__create_role()

    def __crete_managed_policies(self):
        self.__managed_policies = []

        if self.__aws_policy:
            self.__managed_policies.append(self.__aws_policy)
        else:
            for policy_name in self.__aws_policy_names:
                self.__managed_policies.append(
                    iam.ManagedPolicy.from_aws_managed_policy_name(policy_name)
                )

    def __create_role(self):
        assume_by_ec2 = iam.ServicePrincipal(self.__service_principal)

        self.__role = iam.Role(
            self.__scope, self.__id,
            role_name = self.__id,
            assumed_by = assume_by_ec2,
            managed_policies = self.__managed_policies
        )

        Tags.of(self.__role).add('Name', self.__id)

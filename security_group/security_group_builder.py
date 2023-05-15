from aws_cdk import (
    aws_ec2 as ec2,
    Tags
)

from aws_cdk.aws_ec2 import (
    IVpc,
    ISecurityGroup
)

from constructs import Construct
from libraries.app_config.app_config import AppConfigBuilder

class SecurityGroupBuilder():

    @property
    def sg(self) -> ISecurityGroup:
        return self.__sg

    def __init__(self, scope: Construct, id: str, vpc: IVpc, description: str):
        self.__scope = scope
        self.__app_config = AppConfigBuilder.get_config(self.__scope)
        self.__id = id + f'-sg-{self.__app_config.enviroment}'
        self.__vpc = vpc
        self.__description = description
        self.__create_sg()

    def __create_sg(self):
        self.__sg = ec2.SecurityGroup(
            self.__scope,
            self.__id,
            vpc = self.__vpc,
            security_group_name = self.__id,
            description = self.__description
        )

        Tags.of(self.__sg).add('Name', self.__id)

    def add_role_from_sg_parent(self, port: int, rule_description: str, sg_parent: ISecurityGroup = None):
        self.__sg.connections.allow_from(sg_parent, ec2.Port.tcp(port), rule_description)

    def add_role_from_ip_address(self, port: int, rule_description: str, source_ip: str = '127.0.0.1/32'):
        self.__sg.add_ingress_rule(ec2.Peer.ipv4(source_ip), ec2.Port.tcp(port), rule_description)

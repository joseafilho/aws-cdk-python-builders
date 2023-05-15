from aws_cdk import (
    aws_elasticloadbalancingv2 as alb,
    aws_route53 as route53,
    aws_route53_targets as route53_targets,
    aws_cloudfront as cf
)

from constructs import Construct
from libraries.app_config.app_config import AppConfigBuilder

class SimpleRecordABuilder():

    @property
    def record(self) -> route53.ARecord:
        return self.__record

    def __init__(self, scope: Construct, id: str, zone: route53.IHostedZone, record_name: str):
        self.__scope = scope
        self.__app_config = AppConfigBuilder.get_config(self.__scope)
        self.__id = id + f'-rea-{self.__app_config.enviroment}'
        self.__zone = zone
        self.__record_name = record_name
        self.__record: route53.ARecord = None

    def add_record_target_loadbalancer(self, alb_target: alb.IApplicationLoadBalancer):
        self.__record = route53.ARecord(
            self.__scope, self.__id,
            target = route53.RecordTarget.from_alias(
                route53_targets.LoadBalancerTarget(alb_target)
            ),
            zone = self.__zone,
            record_name = self.__record_name
        )

    def add_record_target_cloudfront(self, cf_target: cf.IDistribution):
        self.__record = route53.ARecord(
            self.__scope, self.__id,
            target = route53.RecordTarget.from_alias(
                route53_targets.CloudFrontTarget(cf_target)
            ),
            zone = self.__zone,
            record_name = self.__record_name
        )

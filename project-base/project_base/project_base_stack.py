from aws_cdk import (
    aws_ec2 as ec2,
    core as cdk
)

from foundations.foundation_resources import FoundationResources
from applications.ecs_applications.beer_backend import BeerBackendResources
from applications.cloudfront_applications.beer_frontend import BeerFrontendResources
from databases.beer_application.beer_database_rds import BeerRDSResources
from storages.simple_bucket_private import SimpleBucketPrivate
from storages.bucket_private_ecs import BucketPrivateECS
from libraries.tags.default_tags import DefaultTags

class ProjectBaseStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        DefaultTags.apply(self)
        
        self.__vpc = ec2.Vpc.from_lookup(
            self, 'vpc-default', 
            vpc_name = 'vpc-default'
        )
        
        self.__foundation_resources = FoundationResources(
            self, 'foundation-resources',
            vpc = self.__vpc
        )

        self.__beer_backend = BeerBackendResources(
            self, 'beer_backend_resources',
            vpc = self.__vpc,
            sg_alb = self.__foundation_resources.sg_alb,
            alb_listener = self.__foundation_resources.alb_https_listener,
            certificate = self.__foundation_resources.cert_company_com_br
        )

        BeerFrontendResources(
            self, 'beer_frontend_resources',
            certificate = self.__foundation_resources.cert_company_com_br
        )

        BeerRDSResources(
            self, 'beer_rds_resources',
            vpc = self.__vpc,
            sg_beer_backend = self.__beer_backend.sg_beer_backend
        )

        SimpleBucketPrivate(
            self, 'company-bucket-private-bk'
        )

        BucketPrivateECS(
            self, 'company-bucket-private-ecs-bk'
        )



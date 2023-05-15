from aws_cdk import (
    aws_s3 as s3
)

from constructs import Construct
from libraries.app_config.app_config import AppConfigBuilder

class BucketPrivateBuilder():

    @property
    def bucket(self) -> s3.IBucket:
        return self.__bucket

    def __init__(self, scope: Construct, id: str):        
        self.__scope = scope
        self.__app_config = AppConfigBuilder.get_config(self.__scope)
        self.__id = id + f'-bk-{self.__app_config.enviroment}'

        self.__create_bucket()        
    
    def __create_bucket(self):
        self.__bucket = s3.Bucket(
            self.__scope, self.__id,
            bucket_name = self.__id,
            block_public_access = s3.BlockPublicAccess(
                block_public_acls = True, 
                block_public_policy = True, 
                ignore_public_acls = True,
                restrict_public_buckets = True
            )
        )
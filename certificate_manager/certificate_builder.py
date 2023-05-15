from typing import (
    Optional,
    Sequence
)

from aws_cdk import (
    aws_certificatemanager as cert,
    aws_route53 as route53,
    Tags
)

from constructs import Construct
from libraries.app_config.app_config import AppConfigBuilder

class CertificateBuilder():

    @property
    def certificate(self) -> cert.ICertificate:
        return self.__certificate

    def __init__(self, scope: Construct, id: str, domain: str, hosted_zone: route53.IHostedZone, alternative_names: Optional[Sequence[str]] = None):
        self.__scope = scope
        self.__app_config = AppConfigBuilder.get_config(self.__scope)
        self.__id = id + f'-cert-{self.__app_config.enviroment}'
        self.__domain_name = domain
        self.__hosted_zone = hosted_zone
        self.__alternative_names = alternative_names
        
        self.__create_certificate()

    def __create_certificate(self):
        self.__certificate = cert.Certificate(
            self.__scope, self.__id,
            domain_name = self.__domain_name,
            validation = cert.CertificateValidation.from_dns(self.__hosted_zone),
            subject_alternative_names = self.__alternative_names
        )

        Tags.of(self.__certificate).add('Name', self.__id)

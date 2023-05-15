from aws_cdk import (
    aws_route53 as route,
    Tags
)

from constructs import Construct

class Route53Builder(Construct):

    @property
    def hostedzone(self) -> route.IHostedZone:
        return self.__hostedzone
    
    def __init__(self, scope: Construct, id: str, zone_name: str, comment: str, **kwargs):
        super().__init__(scope, id, **kwargs)                       
        
        self.__id = id
        self.__zone_name = zone_name
        self.__comment = comment
        self.__createhostedzone()

    def __createhostedzone(self):      
        self.__hostedzone = route.HostedZone(
            self, 
            self.__id + '-hz',
            zone_name = self.__zone_name,
            comment = self.__comment
        )        
                        
        Tags.of(self.__hostedzone).add('Name', self.__id)
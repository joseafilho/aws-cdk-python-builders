import aws_cdk as cdk
from constructs import Construct

class PrintUtils():

    @staticmethod
    def print_output(scope: Construct, id: str, value: str):
        cdk.CfnOutput(
            scope, id,
            value = value
        )

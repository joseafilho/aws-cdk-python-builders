from constructs import Construct
import aws_cdk.aws_ec2 as ec2

class SubnetUtils():
    @staticmethod
    def get_all_public_subnets(scope: Construct, id: str) -> ec2.SubnetSelection:
        subnet_1a = ec2.Subnet.from_subnet_attributes(
            scope = scope,
            id = f'{id}-subnet-1a',
            subnet_id = '',
            availability_zone = 'us-east-1a'
        )

        subnet_1b = ec2.Subnet.from_subnet_attributes(
            scope = scope,
            id = f'{id}-subnet-1b',
            subnet_id = '',
            availability_zone = 'us-east-1b'
        )

        subnet_1c = ec2.Subnet.from_subnet_attributes(
            scope = scope,
            id = f'{id}-subnet-1c',
            subnet_id = '',
            availability_zone = 'us-east-1c'
        )

        subnet_1d = ec2.Subnet.from_subnet_attributes(
            scope = scope,
            id = f'{id}-subnet-1d',
            subnet_id = '',
            availability_zone = 'us-east-1d'
        )

        subnet_1e = ec2.Subnet.from_subnet_attributes(
            scope = scope,
            id = f'{id}-subnet-1e',
            subnet_id = '',
            availability_zone = 'us-east-1e'
        )

        subnet_1f = ec2.Subnet.from_subnet_attributes(
            scope = scope,
            id = f'{id}-subnet-1f',
            subnet_id = '',
            availability_zone = 'us-east-1f'
        )

        return ec2.SubnetSelection(
            subnets = [subnet_1a, subnet_1b, subnet_1c, subnet_1d, subnet_1e, subnet_1f]
        )

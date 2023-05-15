from typing import (
    Optional,
    Sequence
)

from aws_cdk import (
    aws_elasticloadbalancingv2 as alb,
    Duration
)

class ALBUtils():

    @staticmethod
    def add_target_in_listener(id: str, alb_listener: alb.IApplicationListener, target: alb.IApplicationLoadBalancerTarget,
        port: int, priority: int, health_check_path: str, host_headers: Sequence[str], paths: Optional[Sequence[str]] = None, health_check_interval_seconds: int = 30):

        rules = [alb.ListenerCondition.host_headers(host_headers)]

        if paths:
            rules.append(alb.ListenerCondition.path_patterns(paths))

        alb_listener.add_targets(
            id = id,
            target_group_name = id,
            port = port,
            protocol = alb.ApplicationProtocol.HTTP,
            targets = [target],
            conditions = rules,
            health_check = alb.HealthCheck(
                healthy_threshold_count = 5,
                path = health_check_path,
                timeout = Duration.seconds(2),
                interval = Duration.seconds(health_check_interval_seconds)
            ),
            priority = priority
        )

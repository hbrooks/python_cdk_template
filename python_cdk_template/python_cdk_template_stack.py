import os
# from aws_cdk import (
#     aws_ecr,
#     aws_iam as iam,
#     aws_lambda,
#     aws_sqs as sqs,
#     aws_sns as sns,
#     aws_sns_subscriptions as subs,
#     core
# )
import aws_cdk.core as core
import aws_cdk.aws_ecr as aws_ecr
import aws_cdk.aws_iam as iam
import aws_cdk.aws_lambda as aws_lambda
import aws_cdk.aws_sqs as sqs
import aws_cdk.aws_sns as sns
import aws_cdk.aws_sns_subscriptions as aws_sns_subscriptions



class PythonCdkTemplateStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        queue = sqs.Queue(
            self, "PythonCdkTemplateQueue",
            visibility_timeout=core.Duration.seconds(300),
        )

        topic = sns.Topic(
            self, "PythonCdkTemplateTopic"
        )

        topic.add_subscription(aws_sns_subscriptions.SqsSubscription(queue))

        ecr_image = aws_lambda.EcrImageCode.from_asset_image(
            directory = os.path.join(os.getcwd(), "python_lambda_code")
        )
        
        aws_lambda.Function(self, 
            id = "TestPythonLambdaFromContainer",
            description = "A Python Lambda built from a Container.",
            code = ecr_image,
            handler = aws_lambda.Handler.FROM_IMAGE,
            runtime = aws_lambda.Runtime.FROM_IMAGE,
            environment = {"hello":"world"},
            function_name = "TestPythonLambdaFromContainer",
            memory_size = 128,
            reserved_concurrent_executions = 10,
            timeout = core.Duration.seconds(1),
        )
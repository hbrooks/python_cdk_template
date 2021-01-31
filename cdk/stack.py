import os

import aws_cdk.core as core
import aws_cdk.aws_apigateway as apigateway
import aws_cdk.aws_ecr as aws_ecr
import aws_cdk.aws_iam as iam
import aws_cdk.aws_lambda as aws_lambda
import aws_cdk.aws_sqs as sqs
import aws_cdk.aws_sns as sns
import aws_cdk.aws_sns_subscriptions as aws_sns_subscriptions



class ExampleStack(core.Stack):

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
        
        my_lambda = aws_lambda.Function(self, 
            id = "Lambda-ExampleStack",
            description = "This Lambda handles all requests from the Front End of The Lab.",
            code = ecr_image,
            handler = aws_lambda.Handler.FROM_IMAGE,
            runtime = aws_lambda.Runtime.FROM_IMAGE,
            environment = {"hello":"world"},
            function_name = "Lambda-ExampleStack",
            memory_size = 128,
            reserved_concurrent_executions = 10,
            timeout = core.Duration.seconds(1),
        )

        api_gateway = apigateway.RestApi(self, "MyApiGateway",
            rest_api_name = "ApiGateway-ExampleStack",
            description = "Created using CDK."
        )

        get_widgets_integration = apigateway.LambdaIntegration(
            my_lambda,
            request_templates={"application/json": '{ "statusCode": "200" }'}
        )

        api_gateway.root.add_method("GET", get_widgets_integration) # Allows GET / to pass to the Lambda.
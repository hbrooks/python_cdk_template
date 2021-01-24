import json
import pytest

from aws_cdk import core
from python_cdk_template.python_cdk_template_stack import PythonCdkTemplateStack


def get_template():
    app = core.App()
    PythonCdkTemplateStack(app, "python-cdk-template")
    return json.dumps(app.synth().get_stack("python-cdk-template").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())

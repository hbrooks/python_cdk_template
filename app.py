#!/usr/bin/env python3

from aws_cdk import core

from python_cdk_template.python_cdk_template_stack import PythonCdkTemplateStack


app = core.App()
PythonCdkTemplateStack(app, "python-cdk-template", env={'region': 'us-east-1'})

app.synth()

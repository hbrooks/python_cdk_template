#!/usr/bin/env python3

from aws_cdk import core

from cdk.stack import ExampleStack


app = core.App()
ExampleStack(app, "MyExampleStack", env={'region': 'us-east-1'})

app.synth()

#!/usr/bin/env python3

from aws_cdk import core

from cdk_mwwa_blogpost.cdk_mwwa_blogpost_stack import CdkMwwaBlogpostStack


app = core.App()
CdkMwwaBlogpostStack(app, "cdk-mwwa-blogpost")

app.synth()

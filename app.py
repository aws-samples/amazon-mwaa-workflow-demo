#!/usr/bin/env python3

from aws_cdk import core

from cdk_mwwa_blogpost.VPCStack import VPCStack
from cdk_mwwa_blogpost.DataLakeStack import DataLakeStack
from cdk_mwwa_blogpost.IAMStack import IAMStack


app = core.App()


vpc = VPCStack(app, "cdk-mwaa-vpc")
data_lake = DataLakeStack(app, 'cdk-mwaa-s3')

s3_buckets = data_lake.buckets

iam = IAMStack(app, 'cdk-mwaa-iam', s3_buckets=s3_buckets)

app.synth()

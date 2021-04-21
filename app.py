#!/usr/bin/env python3

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from aws_cdk import core
from cdk_mwaa_blogpost.VPCStack import VPCStack
from cdk_mwaa_blogpost.DataLakeStack import DataLakeStack
from cdk_mwaa_blogpost.IAMStack import IAMStack

app = core.App()

vpc = VPCStack(app, "cdk-mwaa-vpc")
data_lake = DataLakeStack(app, 'cdk-mwaa-s3')

s3_buckets = data_lake.buckets

iam = IAMStack(app, 'cdk-mwaa-iam', s3_buckets=s3_buckets)

app.synth()

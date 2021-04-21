# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from aws_cdk import (core,
                     aws_ec2 as ec2
                     )


class VPCStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        public_subnet = ec2.SubnetConfiguration(name='mwaa_public_subnet',
                                                subnet_type=ec2.SubnetType.PUBLIC,
                                                cidr_mask=24
                                                )

        mwaa_sbnet = ec2.SubnetConfiguration(name='mwaa_dag_subnet',
                                             subnet_type=ec2.SubnetType.PRIVATE,
                                             cidr_mask=24
                                             )

        emr_subnet = ec2.SubnetConfiguration(name='mwaa_emr_subnet',
                                             subnet_type=ec2.SubnetType.PRIVATE,
                                             cidr_mask=24
                                             )

        vpc_mwaa = ec2.Vpc(self,
                           id='mwaa_vpc',
                           cidr='10.128.0.0/16',
                           subnet_configuration=[public_subnet, mwaa_sbnet, emr_subnet],
                           nat_gateways=1,
                           nat_gateway_subnets=ec2.SubnetSelection(subnet_group_name='mwaa_public_subnet'),
                           max_azs=2,
                           )

        # Outputs
        core.CfnOutput(self, 'vpc_id', value=vpc_mwaa.vpc_id)
        core.CfnOutput(self, 'emr_subnet_id',
                       value=vpc_mwaa.select_subnets(subnet_group_name='mwaa_emr_subnet').subnet_ids[0])
        core.CfnOutput(self, 'mwaa_subnets_id_1',
                       value=vpc_mwaa.select_subnets(subnet_group_name='mwaa_dag_subnet').subnet_ids[0])
        core.CfnOutput(self, 'mwaa_subnets_id_2',
                       value=vpc_mwaa.select_subnets(subnet_group_name='mwaa_dag_subnet').subnet_ids[1])

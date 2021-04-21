# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from aws_cdk import (core,
                     aws_iam as iam
                     )


class IAMStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, s3_buckets, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        emr_s3_statement_1 = iam.PolicyStatement(sid='AllowEMRS3',
                                                 effect=iam.Effect.ALLOW,
                                                 actions=[
                                                     "s3:PutAnalyticsConfiguration",
                                                     "s3:PutAccessPointConfigurationForObjectLambda",
                                                     "s3:GetObjectVersionTagging",
                                                     "s3:DeleteAccessPoint",
                                                     "s3:CreateBucket",
                                                     "s3:DeleteAccessPointForObjectLambda",
                                                     "s3:GetStorageLensConfigurationTagging",
                                                     "s3:ReplicateObject",
                                                     "s3:GetObjectAcl",
                                                     "s3:GetBucketObjectLockConfiguration",
                                                     "s3:DeleteBucketWebsite",
                                                     "s3:GetIntelligentTieringConfiguration",
                                                     "s3:PutLifecycleConfiguration",
                                                     "s3:GetObjectVersionAcl",
                                                     "s3:DeleteObject",
                                                     "s3:GetBucketPolicyStatus",
                                                     "s3:GetObjectRetention",
                                                     "s3:GetBucketWebsite",
                                                     "s3:GetJobTagging",
                                                     "s3:PutReplicationConfiguration",
                                                     "s3:PutObjectLegalHold",
                                                     "s3:GetObjectLegalHold",
                                                     "s3:GetBucketNotification",
                                                     "s3:PutBucketCORS",
                                                     "s3:GetReplicationConfiguration",
                                                     "s3:ListMultipartUploadParts",
                                                     "s3:PutObject",
                                                     "s3:GetObject",
                                                     "s3:PutBucketNotification",
                                                     "s3:DescribeJob",
                                                     "s3:PutBucketLogging",
                                                     "s3:GetAnalyticsConfiguration",
                                                     "s3:PutBucketObjectLockConfiguration",
                                                     "s3:GetObjectVersionForReplication",
                                                     "s3:GetAccessPointForObjectLambda",
                                                     "s3:GetStorageLensDashboard",
                                                     "s3:CreateAccessPoint",
                                                     "s3:GetLifecycleConfiguration",
                                                     "s3:GetInventoryConfiguration",
                                                     "s3:GetBucketTagging",
                                                     "s3:PutAccelerateConfiguration",
                                                     "s3:GetAccessPointPolicyForObjectLambda",
                                                     "s3:DeleteObjectVersion",
                                                     "s3:GetBucketLogging",
                                                     "s3:ListBucketVersions",
                                                     "s3:RestoreObject",
                                                     "s3:ListBucket",
                                                     "s3:GetAccelerateConfiguration",
                                                     "s3:GetBucketPolicy",
                                                     "s3:PutEncryptionConfiguration",
                                                     "s3:GetEncryptionConfiguration",
                                                     "s3:GetObjectVersionTorrent",
                                                     "s3:AbortMultipartUpload",
                                                     "s3:GetBucketRequestPayment",
                                                     "s3:DeleteBucketOwnershipControls",
                                                     "s3:GetAccessPointPolicyStatus",
                                                     "s3:UpdateJobPriority",
                                                     "s3:GetObjectTagging",
                                                     "s3:GetMetricsConfiguration",
                                                     "s3:GetBucketOwnershipControls",
                                                     "s3:DeleteBucket",
                                                     "s3:PutBucketVersioning",
                                                     "s3:GetBucketPublicAccessBlock",
                                                     "s3:ListBucketMultipartUploads",
                                                     "s3:PutIntelligentTieringConfiguration",
                                                     "s3:GetAccessPointPolicyStatusForObjectLambda",
                                                     "s3:PutMetricsConfiguration",
                                                     "s3:PutBucketOwnershipControls",
                                                     "s3:UpdateJobStatus",
                                                     "s3:GetBucketVersioning",
                                                     "s3:GetBucketAcl",
                                                     "s3:GetAccessPointConfigurationForObjectLambda",
                                                     "s3:PutInventoryConfiguration",
                                                     "s3:GetObjectTorrent",
                                                     "s3:GetStorageLensConfiguration",
                                                     "s3:DeleteStorageLensConfiguration",
                                                     "s3:PutBucketWebsite",
                                                     "s3:PutBucketRequestPayment",
                                                     "s3:PutObjectRetention",
                                                     "s3:CreateAccessPointForObjectLambda",
                                                     "s3:GetBucketCORS",
                                                     "s3:GetBucketLocation",
                                                     "s3:GetAccessPointPolicy",
                                                     "s3:ReplicateDelete",
                                                     "s3:GetObjectVersion"
                                                 ],
                                                 resources=[
                                                     s3_buckets['datalake_raw'].bucket_arn,
                                                     f"{s3_buckets['datalake_raw'].bucket_arn}/*",
                                                     s3_buckets['datalake_processed'].bucket_arn,
                                                     f"{s3_buckets['datalake_processed'].bucket_arn}/*",
                                                     s3_buckets['emr_scripts'].bucket_arn,
                                                     f"{s3_buckets['emr_scripts'].bucket_arn}/*",
                                                     s3_buckets['emr_logs'].bucket_arn,
                                                     f"{s3_buckets['emr_logs'].bucket_arn}/*"
                                                 ])

        emr_s3_statement_2 = iam.PolicyStatement(sid='AllowEMRS3List',
                                                 effect=iam.Effect.ALLOW,
                                                 actions=[
                                                     "s3:ListStorageLensConfigurations",
                                                     "s3:ListAccessPointsForObjectLambda",
                                                     "s3:GetAccessPoint",
                                                     "s3:GetAccountPublicAccessBlock",
                                                     "s3:ListAllMyBuckets",
                                                     "s3:ListAccessPoints",
                                                     "s3:ListJobs",
                                                     "s3:PutStorageLensConfiguration",
                                                     "s3:CreateJob"
                                                 ],
                                                 resources=['*'])

        emr_s3_policy_document = iam.PolicyDocument(statements=[emr_s3_statement_1, emr_s3_statement_2])

        emr_s3_policy = iam.Policy(self, id='emr_s3_policy',
                                   policy_name='emr_s3_policy',
                                   document=emr_s3_policy_document
                                   )

        emr_role = iam.Role(self, id='EMR_DefaultRole_MWAA',
                            role_name='EMR_DefaultRole_MWAA',
                            assumed_by=iam.ServicePrincipal('elasticmapreduce.amazonaws.com'),
                            managed_policies=[
                                iam.ManagedPolicy.from_aws_managed_policy_name(
                                    'service-role/AmazonElasticMapReduceRole')]
                            )

        emr_ec2_role = iam.Role(self, id='EMR_EC2_DefaultRole_MWAA',
                                role_name='EMR_EC2_DefaultRole_MWAA',
                                assumed_by=iam.ServicePrincipal('ec2.amazonaws.com'),
                                managed_policies=[
                                    iam.ManagedPolicy.from_aws_managed_policy_name(
                                        'service-role/AmazonElasticMapReduceforEC2Role')]
                                )

        emr_ec2_role_instance_profile = iam.CfnInstanceProfile(self, id='EMR_EC2_InstanceProfile_MWAA',
                                                               instance_profile_name='EMR_EC2_DefaultRole_MWAA',
                                                               roles=[emr_ec2_role.role_name]
                                                               )

        emr_s3_policy.attach_to_role(emr_role)
        emr_s3_policy.attach_to_role(emr_ec2_role)

        mwaa_s3_statement_1 = iam.PolicyStatement(sid='AllowMWAAS31',
                                                  effect=iam.Effect.ALLOW,
                                                  actions=["s3:ListStorageLensConfigurations",
                                                           "s3:ListAccessPointsForObjectLambda",
                                                           "s3:GetAccessPoint",
                                                           "s3:PutAccountPublicAccessBlock",
                                                           "s3:GetAccountPublicAccessBlock",
                                                           "s3:ListAllMyBuckets",
                                                           "s3:ListAccessPoints",
                                                           "s3:ListJobs",
                                                           "s3:PutStorageLensConfiguration",
                                                           "s3:CreateJob"],
                                                  resources=['*']
                                                  )

        mwaa_s3_statement_2 = iam.PolicyStatement(sid='AllowMWAAS32',
                                                  effect=iam.Effect.ALLOW,
                                                  actions=["s3:*"],
                                                  resources=[
                                                      s3_buckets['datalake_raw'].bucket_arn,
                                                      f"{s3_buckets['datalake_raw'].bucket_arn}/*",
                                                      s3_buckets['datalake_processed'].bucket_arn,
                                                      f"{s3_buckets['datalake_processed'].bucket_arn}/*"

                                                  ]
                                                  )

        mwaa_glue_statement_1 = iam.PolicyStatement(sid='AllowMWAAGlueCrawler',
                                                    effect=iam.Effect.ALLOW,
                                                    actions=[
                                                        "glue:ListSchemaVersions",
                                                        "glue:GetCrawler",
                                                        "glue:GetMLTaskRuns",
                                                        "glue:ListTriggers",
                                                        "glue:ListJobs",
                                                        "glue:QuerySchemaVersionMetadata",
                                                        "glue:ListMLTransforms",
                                                        "glue:ListDevEndpoints",
                                                        "glue:StartCrawler",
                                                        "glue:ListSchemas",
                                                        "glue:ListRegistries",
                                                        "glue:ListCrawlers",
                                                        "glue:GetMLTransforms",
                                                        "glue:ListWorkflows"
                                                    ],
                                                    resources=["*"]
                                                    )

        mwaa_glue_statement_2 = iam.PolicyStatement(sid='AllowMWAAGlueDatabase',
                                                    effect=iam.Effect.ALLOW,
                                                    actions=[
                                                        "glue:GetPartition",
                                                        "glue:GetTables",
                                                        "glue:GetPartitions",
                                                        "glue:ListSchemas",
                                                        "glue:GetTable"
                                                    ],
                                                    resources=[
                                                        f"arn:aws:glue:{self.region}:{self.account}:database/mwaa_movie_lens",
                                                        f"arn:aws:glue:{self.region}:{self.account}:catalog",
                                                        f"arn:aws:glue:{self.region}:{self.account}:table/*/*"
                                                    ]
                                                    )

        mwaa_emr_statement_1 = iam.PolicyStatement(sid='AllowMWAAEMR1',
                                                   effect=iam.Effect.ALLOW,
                                                   actions=[
                                                       "elasticmapreduce:DescribeStep",
                                                       "elasticmapreduce:AddJobFlowSteps",
                                                       "elasticmapreduce:RunJobFlow"
                                                   ],
                                                   resources=["*"]
                                                   )

        mwaa_emr_statement_2 = iam.PolicyStatement(sid='AllowMWAAEMR2',
                                                   effect=iam.Effect.ALLOW,
                                                   actions=["iam:PassRole"],
                                                   resources=[emr_role.role_arn,
                                                              emr_ec2_role.role_arn
                                                              ]
                                                   )

        mwaa_athena_statement_1 = iam.PolicyStatement(sid='AllowMWAAAthena1',
                                                      effect=iam.Effect.ALLOW,
                                                      actions=["athena:*"],
                                                      resources=["*"]
                                                      )

        mwaa_airflow_policy_document = iam.PolicyDocument(statements=[mwaa_s3_statement_1,
                                                                      mwaa_s3_statement_2,
                                                                      mwaa_glue_statement_1,
                                                                      mwaa_glue_statement_2,
                                                                      mwaa_emr_statement_1,
                                                                      mwaa_emr_statement_2,
                                                                      mwaa_athena_statement_1
                                                                      ])

        mwaa_airflow_policy = iam.ManagedPolicy(self, id='mwaa_demo_base_policy',
                                                managed_policy_name='mwaa_airflow_policy',
                                                document=mwaa_airflow_policy_document,
                                                )

        core.CfnOutput(self,
                       id='emr_jobflow_role',
                       value=emr_ec2_role.role_name)

        core.CfnOutput(self,
                       id='emr_service_role',
                       value=emr_role.role_name)

        core.CfnOutput(self,
                       id='mwaa_policy',
                       value=mwaa_airflow_policy.managed_policy_name)

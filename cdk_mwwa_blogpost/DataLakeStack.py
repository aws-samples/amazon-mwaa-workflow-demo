from aws_cdk import (core,
                     aws_s3 as s3,
                     aws_s3_deployment as s3_deployment,
                     aws_glue as glue,
                     aws_iam as iam
                     )


class DataLakeStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket_name_list = ['datalake_raw', 'datalake_processed', 'mwaa_config', 'emr_scripts', 'emr_logs']
        bucket_constructs = {}

        for bucket_name in bucket_name_list:
            bucket_constructs[bucket_name] = s3.Bucket(self,
                                                       id=bucket_name,
                                                       block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                                                       removal_policy=core.RemovalPolicy.DESTROY
                                                       )
            core.CfnOutput(self,
                           id=f'{bucket_name}_bucket',
                           value=bucket_constructs[bucket_name].bucket_name)

        s3_deployment.BucketDeployment(self, id='upload_dag',
                                       sources=[s3_deployment.Source.asset('./assets/mwaa_dags/')],
                                       destination_bucket=bucket_constructs.get('mwaa_config')
                                       )

        s3_deployment.BucketDeployment(self, id='upload_emr_scripts',
                                       sources=[s3_deployment.Source.asset('./assets/spark_scripts/')],
                                       destination_bucket=bucket_constructs.get('emr_scripts')
                                       )

        glue_database = glue.Database(self, id='glue_db_mwaa',
                                      database_name='mwaa_movie_lens'
                                      )

        glue_crawler_s3_target_name = bucket_constructs['datalake_processed'].bucket_name
        glue_crawler_s3_target_arn = bucket_constructs['datalake_processed'].bucket_arn

        statement = iam.PolicyStatement(actions=["s3:GetObject", "s3:PutObject"],
                                        resources=[glue_crawler_s3_target_arn,
                                                   f'{glue_crawler_s3_target_arn}/*']
                                        )

        write_to_s3_policy = iam.PolicyDocument(statements=[statement])

        glue_role = iam.Role(self, id='AWSGlueServiceRole-mwaa-demo-crawler',
                             role_name='AWSGlueServiceRole-mwaa-demo-crawler',
                             inline_policies=[write_to_s3_policy],
                             assumed_by=iam.ServicePrincipal('glue.amazonaws.com'),
                             managed_policies=[
                                 iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSGlueServiceRole')]
                             )

        # https://github.com/aws/aws-cdk/issues/13242
        glue_crawler = glue.CfnCrawler(self, id='glue_crawler_mwaa',
                                       description='Glue Crawler for MWAA Blogpost',
                                       name='mwaa_crawler_movie_lens',
                                       database_name=glue_database.database_name,
                                       role=glue_role.role_arn,
                                       targets=glue.CfnCrawler.TargetsProperty(s3_targets=[
                                           glue.CfnCrawler.S3TargetProperty(
                                               path=f's3://{glue_crawler_s3_target_name}')])
                                       )

        self.buckets = bucket_constructs

        # Outputs
        core.CfnOutput(self,
                       id='glue_database_name',
                       value=glue_database.database_name)

        core.CfnOutput(self,
                       id='glue_crawler_name',
                       value=glue_crawler.name)

    @property
    def get_buckets(self):
        return self.buckets

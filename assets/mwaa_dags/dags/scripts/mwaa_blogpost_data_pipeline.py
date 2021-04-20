import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.s3_key_sensor import S3KeySensor
from airflow.sensors.s3_prefix_sensor import S3PrefixSensor
from airflow.hooks.S3_hook import S3Hook
from airflow.contrib.operators.emr_add_steps_operator import EmrAddStepsOperator
from airflow.contrib.operators.emr_create_job_flow_operator import EmrCreateJobFlowOperator
from airflow.contrib.sensors.emr_step_sensor import EmrStepSensor
from custom.glue_trigger_crawler_operator import GlueTriggerCrawlerOperator
from airflow.contrib.operators.aws_athena_operator import AWSAthenaOperator
from airflow.models import Variable
import requests
from io import BytesIO
import zipfile

default_args = {
    "owner": "Airflow",
    "start_date": airflow.utils.dates.days_ago(1),
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "youremail@host.com",
    "retries": 1
}

SETUP_HADOOP_DEBUGGING = [
   {
       'Name': 'Setup hadoop debugging',
       'ActionOnFailure': 'TERMINATE_CLUSTER',
       'HadoopJarStep': {
           'Jar': 'command-runner.jar',
           'Args': ['state-pusher-script'],
       },
   }
]

JOB_FLOW_OVERRIDES = {
    'Name': 'mwaa-emr-cluster',
    'ReleaseLabel': 'emr-5.32.0',
    'LogUri': 's3://{{ var.value.emr_logs_bucket }}',
    'Applications': [
        {
            'Name': 'Hadoop'
        },
        {
            'Name': 'Spark'
        },
        {
            'Name': 'Hive'
        },
        {
            'Name': 'Pig'
        },
    ],
    'Instances': {
        'InstanceGroups': [
            {
                'Name': 'MASTER',
                'InstanceRole': 'MASTER',
                'InstanceCount': 1,
                'InstanceType': 'm5.xlarge',
            },
            {
                'Name': 'CORE',
                'InstanceRole': 'CORE',
                'InstanceCount': 2,
                'InstanceType': 'm5.xlarge',
            },
        ],
        "Ec2SubnetId": "{{ var.value.emr_subnet_id }}",
        'KeepJobFlowAliveWhenNoSteps': False,
        'TerminationProtected': False,
    },
    'VisibleToAllUsers': True,
    'JobFlowRole': '{{ var.value.emr_jobflow_role }}',
    'ServiceRole': '{{ var.value.emr_service_role }}',
    'EbsRootVolumeSize': 10,
    'Steps': SETUP_HADOOP_DEBUGGING,
    'Tags': [
        {
            'Key': 'Name',
            'Value': 'MWAA Blogpost Cluster'
        }
    ]
}

SPARK_STEPS = [
    {
        'Name': 'process_movies_{{ ds_nodash }}',
        'ActionOnFailure': 'CONTINUE',
        'HadoopJarStep': {
            'Jar': 'command-runner.jar',
            'Args': ['spark-submit',
                     '--deploy-mode',
                     'cluster',
                     '--master',
                     'yarn',
                     's3://{{ var.value.emr_scripts_bucket }}/SparkScript01.py',
                     '--source_bucket',
                     's3://{{ var.value.datalake_raw_bucket }}/movie/{{ ds }}/',
                     '--destination_bucket',
                     's3://{{ var.value.datalake_processed_bucket }}/movie/{{ ds }}/',
                     '--app_name',
                     'movies_ds'],
        },
    },
    {
        'Name': 'process_ratings_{{ ds_nodash }}',
        'ActionOnFailure': 'CONTINUE',
        'HadoopJarStep': {
            'Jar': 'command-runner.jar',
            'Args': ['spark-submit',
                     '--deploy-mode',
                     'cluster',
                     '--master',
                     'yarn',
                     's3://{{ var.value.emr_scripts_bucket }}/SparkScript01.py',
                     '--source_bucket',
                     's3://{{ var.value.datalake_raw_bucket }}/rating/{{ ds }}/',
                     '--destination_bucket',
                     's3://{{ var.value.datalake_processed_bucket }}/rating/{{ ds }}/',
                     '--app_name',
                     'ratings_ds'],
        },
    },
    {
        'Name': 'process_tags_{{ ds_nodash }}',
        'ActionOnFailure': 'CONTINUE',
        'HadoopJarStep': {
            'Jar': 'command-runner.jar',
            'Args': ['spark-submit',
                     '--deploy-mode',
                     'cluster',
                     '--master',
                     'yarn',
                     's3://{{ var.value.emr_scripts_bucket }}/SparkScript01.py',
                     '--source_bucket',
                     's3://{{ var.value.datalake_raw_bucket }}/tag/{{ ds }}/',
                     '--destination_bucket',
                     's3://{{ var.value.datalake_processed_bucket }}/tag/{{ ds }}/',
                     '--app_name',
                     'tags_ds'],
        },
    },
]


def download_dataset(**context):
    endpoint_path = context['endpoint_path']
    bucket_name = context['templates_dict']['bucket_name']
    bucket_partition = context['templates_dict']['bucket_partition']

    s3_hook = S3Hook(aws_conn_id='aws_default')
    movie_lens_data = requests.get(endpoint_path)

    if movie_lens_data:

        with zipfile.ZipFile(BytesIO(movie_lens_data.content)) as zip_movie_lens_file:

            for ziped_file in zip_movie_lens_file.namelist():

                if ziped_file.endswith('.csv'):
                    print(ziped_file)
                    # unziped_file = BytesIO(zip_movie_lens_file.read(ziped_file))
                    s3_folder_name = ziped_file.split('/')[-1].rstrip('.csv')
                    s3_object_name = ziped_file.split('/')[-1]
                    s3_hook.load_bytes(bucket_name=bucket_name,
                                       key=f'{s3_folder_name}/{bucket_partition}/{s3_object_name}',
                                       bytes_data=zip_movie_lens_file.read(ziped_file), replace=True)

        # Write Sucess File
        s3_hook.load_string(bucket_name=bucket_name, key='_SUCCESS', string_data='SUCCESS', replace=True)

        return True

    else:
        return False


with DAG(dag_id='mwaa_blogpost_data_pipeline', schedule_interval='@once', default_args=default_args, catchup=False,
         tags=['emr', 'blogpost', 'mwaa']) as dag:
    download_movie_lens = PythonOperator(
        task_id='download_movie_lens',
        python_callable=download_dataset,
        provide_context=True,
        op_kwargs={'endpoint_path': 'http://files.grouplens.org/datasets/movielens/ml-latest-small.zip'},
        templates_dict={'bucket_partition': "{{ ds }}", 'bucket_name': '{{ var.value.datalake_raw_bucket }}'}
    )

    check_raw_s3_bucket = S3KeySensor(
        task_id='check_raw_s3_bucket',
        aws_conn_id='aws_default',
        bucket_name='{{ var.value.datalake_raw_bucket }}',
        bucket_key='_SUCCESS'
    )

    create_emr_cluster = EmrCreateJobFlowOperator(
        task_id='create_emr_cluster',
        aws_conn_id='aws_default',
        job_flow_overrides=JOB_FLOW_OVERRIDES
    )

    emr_step_jobs_list = []
    emr_job_sensors_list = []

    for n_step, step in enumerate(SPARK_STEPS):
        add_emr_spark_step = EmrAddStepsOperator(
            task_id=f'add_emr_spark_step_{n_step}',
            aws_conn_id='aws_default',
            job_flow_id="{{ task_instance.xcom_pull(task_ids='create_emr_cluster') }}",
            steps=[step]
        )
        emr_step_jobs_list.append(add_emr_spark_step)

        emr_spark_job_sensor = EmrStepSensor(
            task_id=f'emr_spark_job_sensor_{n_step}',
            aws_conn_id='aws_default',
            job_flow_id="{{ task_instance.xcom_pull(task_ids='create_emr_cluster') }}",
            step_id=f"{{{{ task_instance.xcom_pull(task_ids='add_emr_spark_step_{n_step}')[0] }}}}"
        )
        emr_job_sensors_list.append(emr_spark_job_sensor)

    glue_crawler_name = Variable.get('glue_crawler_name')

    run_glue_crawler = GlueTriggerCrawlerOperator(
        task_id='run_glue_crawler',
        aws_conn_id='aws_default',
        crawler_name=glue_crawler_name
    )

    query_athena_results = AWSAthenaOperator(
        task_id='query_athena_results',
        aws_conn_id='aws_default',
        database='{{ var.value.glue_database_name }}',
        query="""
        SELECT movie.genres, AVG(rating.rating) as genre_rating, COUNT(movie.genres) as genre_count
        FROM movie
        JOIN rating ON movie.movieid = rating.movieid
        GROUP BY movie.genres
        HAVING COUNT(movie.genres) > 100
        ORDER BY genre_rating DESC
        LIMIT 10;
        """,
        output_location='s3://{{ var.value.datalake_processed_bucket }}/athena_results/{{ ds }}/'
    )


    download_movie_lens >> check_raw_s3_bucket >> create_emr_cluster
    [create_emr_cluster >> step >> sensor >> run_glue_crawler for step, sensor in
     zip(emr_step_jobs_list, emr_job_sensors_list)]
    run_glue_crawler >> query_athena_results

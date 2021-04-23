import json
import boto3

cft_client = boto3.client('cloudformation')
cft_output_stack_structure = {
    "cdk-mwaa-s3": ["datalake_processed_bucket", "datalake_raw_bucket", "emr_logs_bucket", "emr_scripts_bucket",
                    "glue_crawler_name", "glue_database_name"],
    "cdk-mwaa-vpc": ["emr_subnet_id"],
    "cdk-mwaa-iam": ["emr_jobflow_role", "emr_service_role"]
}

mwaa_variables = {}


def replace_underscore(underscore_string):
    return underscore_string.replace("_", '')


def main():
    for stack_name in cft_output_stack_structure.keys():

        expected_outputs = cft_output_stack_structure[stack_name]

        cft_stack_response = cft_client.describe_stacks(StackName=stack_name)

        cft_stack_response_outputs = cft_stack_response["Stacks"][0]["Outputs"]

        for expected_output in expected_outputs:

            for returned_output in cft_stack_response_outputs:

                if replace_underscore(expected_output) == returned_output["OutputKey"]:
                    mwaa_variables[expected_output] = returned_output["OutputValue"]

    with open("mwaa_demo_variables.json", "w") as outfile:
        json.dump(mwaa_variables, outfile)

    print(f"MWAA Variables Generated: {outfile.name}")


if __name__ == '__main__':
    main()

import boto3
import json
from botocore.exceptions import ClientError

# Inisialisasi client untuk API Gateway
client = boto3.client('apigateway')

def create_api_routes(api_id, lambda_function_name, table_names):
    """Create routes in API Gateway that connect to a specified Lambda function for given table names.

    Args:
        api_id (str): The ID of the API Gateway.
        lambda_function_name (str): The name of the Lambda function to connect to.
        table_names (list): A list of table names to create routes for.
    """
    try:
        root_resource_id = client.get_resources(restApiId=api_id)['items'][0]['id']

        for table_name in table_names:
            resource = client.create_resource(
                restApiId=api_id,
                parentId=root_resource_id,
                pathPart=table_name
            )
            print(f"Created resource: {json.dumps(resource, indent=2)}")

            client.put_method(
                restApiId=api_id,
                resourceId=resource['id'],
                httpMethod='GET',
                authorizationType='NONE' 
            )
            print(f"Created GET method for resource: {table_name}")

            client.put_integration(
                restApiId=api_id,
                resourceId=resource['id'],
                httpMethod='GET',
                type='AWS_PROXY',
                uri=f'arn:aws:lambda:{client.meta.region_name}:{client.get_caller_identity()["Account"]}:function:{lambda_function_name}',
                integrationHttpMethod='POST'
            )
            print(f"Created integration for GET method on resource: {table_name}")

            client.put_method(
                restApiId=api_id,
                resourceId=resource['id'],
                httpMethod='GET',
                authorizationType='NONE'
            )
            print(f"Created GET method for resource: {table_name}")

            client.put_integration(
                restApiId=api_id,
                resourceId=resource['id'],
                httpMethod='GET',
                type='AWS_PROXY',
                uri=f'arn:aws:lambda:{client.meta.region_name}:{client.get_caller_identity()["Account"]}:function:{lambda_function_name}',
                integrationHttpMethod='POST'
            )


            client.put_method(
                restApiId=api_id,
                resourceId=resource['id'],
                httpMethod='PUT',
                authorizationType='NONE'
            )
            print(f"Created PUT method for resource: {table_name}")

            client.put_integration(
                restApiId=api_id,
                resourceId=resource['id'],
                httpMethod='PUT',
                type='AWS_PROXY',
                uri=f'arn:aws:lambda:{client.meta.region_name}:{client.get_caller_identity()["Account"]}:function:{lambda_function_name}',
                integrationHttpMethod='POST'
            )

            client.put_method(
                restApiId=api_id,
                resourceId=resource['id'],
                httpMethod='DELETE',
                authorizationType='NONE'
            )
            print(f"Created DELETE method for resource: {table_name}")

            client.put_integration(
                restApiId=api_id,
                resourceId=resource['id'],
                httpMethod='DELETE',
                type='AWS_PROXY',
                uri=f'arn:aws:lambda:{client.meta.region_name}:{client.get_caller_identity()["Account"]}:function:{lambda_function_name}',
                integrationHttpMethod='POST'
            )

    except ClientError as e:
        print(f"Error creating API routes: {e.response['Error']['Message']}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
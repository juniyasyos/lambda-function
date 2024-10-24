import json
import boto3
from decimal import Decimal
from create_table_dynamon import create_tables_if_not_exist
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
client = boto3.client('dynamodb')

create_tables_if_not_exist(dynamodb)

routes = ["books", "categories", "authors", "transactions", "customers", "orders"]  

tables = {
    'books': dynamodb.Table('Books'),
    'categories': dynamodb.Table('Categories'),
    'authors': dynamodb.Table('Authors'),
    'transactions': dynamodb.Table('Transactions'),
    'customers': dynamodb.Table('Customers'),
    'orders': dynamodb.Table('Orders') 
}

def lambda_handler(event, context):
    route_key = event.get('routeKey', '')
    path_params = event.get('pathParameters', {})
    
    body = json.loads(event.get('body', '{}')) if event.get('body') else {}

    table_key = next((key for key in routes if key in route_key), None)
    if not table_key:
        return make_response(400, "Invalid route")

    table = tables[table_key]

    try:
        # Tangani operasi DELETE
        if route_key.startswith("DELETE"):
            item_id = path_params.get('id')
            if not item_id:
                raise KeyError("Item ID is required for DELETE operation")
            response = delete_item(table, item_id)

        # Tangani operasi GET berdasarkan ID
        elif route_key.startswith("GET") and '{id}' in route_key:
            item_id = path_params.get('id')
            if not item_id:
                raise KeyError("Item ID is required for GET operation")
            response = get_item(table, item_id)

        # Tangani operasi GET semua item
        elif route_key.startswith("GET"):
            response = get_all_items(table)

        # Tangani operasi PUT
        elif route_key.startswith("PUT"):
            if 'id' not in body:
                raise KeyError("Item ID is required for PUT operation")
            response = create_or_update_item(table, body)

        else:
            raise KeyError(f"Unsupported route: {route_key}")

        return make_response(200, response)

    except KeyError as e:
        return make_response(400, f"Unsupported route or missing parameters: {str(e)}")
    except ClientError as e:
        return make_response(500, f"ClientError: {e.response['Error']['Message']}")
    except Exception as e:
        return make_response(500, f"Error: {str(e)}")

def delete_item(table, item_id):
    try:
        table.delete_item(Key={'id': item_id})
        return f'Deleted {item_id} from {table.table_name}'
    except ClientError as e:
        raise e

def get_item(table, item_id):
    try:
        result = table.get_item(Key={'id': item_id})
        return result.get('Item', {})
    except ClientError as e:
        raise e

def get_all_items(table):
    try:
        result = table.scan()
        return result.get('Items', [])
    except ClientError as e:
        raise e

def create_or_update_item(table, data):
    try:
        table.put_item(
            Item={
                'id': data['id'],
                **{k: (Decimal(str(v)) if isinstance(v, float) else v) for k, v in data.items() if k != 'id'}
            }
        )
        return f"Item {data['id']} created/updated in {table.table_name}"
    except ClientError as e:
        raise e

def make_response(status_code, body):
    def convert_decimal(obj):
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, default=convert_decimal)
    }

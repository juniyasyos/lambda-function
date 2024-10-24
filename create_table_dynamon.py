import boto3
from botocore.exceptions import ClientError

def create_tables_if_not_exist(dynamodb):
    existing_table_names = dynamodb.meta.client.list_tables()['TableNames']
    
    if 'Books' not in existing_table_names:
        create_books_table(dynamodb)

    if 'Categories' not in existing_table_names:
        create_categories_table(dynamodb)
        
    if 'Transactions' not in existing_table_names:
        create_transactions_table(dynamodb)

    if 'Customers' not in existing_table_names:
        create_customers_table(dynamodb)

    if 'Authors' not in existing_table_names:
        create_Authors_table(dynamodb)

    if 'Orders' not in existing_table_names:
        create_orders_table(dynamodb)

def create_books_table(dynamodb):
    try:
        table = dynamodb.create_table(
            TableName='Books',
            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        table.wait_until_exists()
        print("Books table created successfully.")
    except ClientError as e:
        print(f"Error creating Books table: {e}")

def create_categories_table(dynamodb):
    try:
        table = dynamodb.create_table(
            TableName='Categories',
            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        table.wait_until_exists()
        print("Categories table created successfully.")
    except ClientError as e:
        print(f"Error creating Categories table: {e}")

def create_transactions_table(dynamodb):
    try:
        table = dynamodb.create_table(
            TableName='Transactions',
            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        table.wait_until_exists()
        print("Transactions table created successfully.")
    except ClientError as e:
        print(f"Error creating Transactions table: {e}")

def create_customers_table(dynamodb):
    try:
        table = dynamodb.create_table(
            TableName='Customers',
            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        table.wait_until_exists()
        print("Customers table created successfully.")
    except ClientError as e:
        print(f"Error creating Customers table: {e}")

def create_Authors_table(dynamodb):
    try:
        table = dynamodb.create_table(
            TableName='Authors',
            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        table.wait_until_exists()
        print("Authors table created successfully.")
    except ClientError as e:
        print(f"Error creating Authors table: {e}")

def create_orders_table(dynamodb):
    try:
        table = dynamodb.create_table(
            TableName='Orders',
            KeySchema=[{'AttributeName': 'order_id', 'KeyType': 'HASH'}],  
            AttributeDefinitions=[{'AttributeName': 'order_id', 'AttributeType': 'S'}], 
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}  
        )
        table.wait_until_exists()
        print("Orders table created successfully.")
    except ClientError as e:
        print(f"Error creating Orders table: {e}")

# Penggunaan fungsi
if __name__ == "__main__":
    dynamodb = boto3.resource('dynamodb')
    create_tables_if_not_exist(dynamodb)

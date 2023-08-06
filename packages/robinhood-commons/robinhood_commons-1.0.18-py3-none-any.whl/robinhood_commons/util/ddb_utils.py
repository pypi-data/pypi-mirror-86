import boto3


def ddb():
    return boto3.resource('dynamodb')


def init_table() -> None:
    table = ddb().create_table(
        TableName='Stocks',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1,
        }
    )


if __name__ == '__main__':
    init_table()

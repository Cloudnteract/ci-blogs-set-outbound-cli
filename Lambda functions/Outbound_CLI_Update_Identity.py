import boto3
import os

# Create a DynamoDB client
dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    
    # Get new outbound queue name from event
    new_identity_name = event['queryStringParameters']['outboundIdentityName']

    # Get agent's username from event
    agent_username = event['queryStringParameters']['agentUsername']
    
    print(f"Update request for: {agent_username}, outbound identity: {new_identity_name}")

    # Check if agent username already exists in the DynamoDB table
    response = dynamodb.get_item(
        TableName=os.environ['TABLE_NAME'],
        Key={
            'AgentUsername': {'S': agent_username}
        }
    )

    # If the agent username exists, update the 'IdentityName' column
    if 'Item' in response:
        dynamodb.update_item(
            TableName=os.environ['TABLE_NAME'],
            Key={
                'AgentUsername': {'S': agent_username}
            },
            UpdateExpression='SET IdentityName = :val',
            ExpressionAttributeValues={
                ':val': {'S': new_identity_name}
            }
        )
    # If the agent username doesn't exist, add a new record with the 'IdentityName' value
    else:
        dynamodb.put_item(
            TableName=os.environ['TABLE_NAME'],
            Item={
                'AgentUsername': {'S': agent_username},
                'IdentityName': {'S': new_identity_name}
            }
        )

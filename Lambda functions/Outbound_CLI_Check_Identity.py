import boto3
import os

# Replace with your DynamoDB table names
AGENT_IDENTITY_TABLE_NAME = os.environ['AGENT_IDENTITY_TABLE_NAME']
IDENTITY_CLI_TABLE_NAME = os.environ['IDENTITY_CLI_TABLE_NAME']

dynamodb = boto3.resource('dynamodb')
agent_table = dynamodb.Table(AGENT_IDENTITY_TABLE_NAME)
identity_table = dynamodb.Table(IDENTITY_CLI_TABLE_NAME)

def lambda_handler(event, context):
    
    # Get the value of 'agentUserName' from the event
    agent_username = event['Details']['ContactData']['Attributes']['agentUserName']
    
    print(f"outbound identity check for Agent: {agent_username}")
    
    # Look up the agent's current identity name in the agent table
    response = agent_table.get_item(Key={'AgentUsername': agent_username})
    if 'Item' not in response:
        print(f"AgentUsername not present in table: {agent_username}")
        return {'status': 'username_not_found'}
    identity_name = response['Item']['IdentityName']
    
    # Look up columns for the identity in the identity CLI table
    response = identity_table.get_item(Key={'IdentityName': identity_name})
    return response.get('Item', {})

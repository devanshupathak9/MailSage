import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    """
    PURPOSE: Receive emails from various sources
    INPUT: SNS, API Gateway, EventBridge, or direct invocation
    OUTPUT: Store raw email in DynamoDB, trigger next steps
    """
    print("📧 Email Consumer triggered")
    
    # 1. Parse incoming email
    email_data = parse_incoming_email(event)
    
    # 2. Store in DynamoDB
    store_email(email_data)
    
    # 3. Trigger processing (next step)
    trigger_email_processing(email_data)
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Email consumed successfully', 'email_id': email_data['email_id']})
    }

def parse_incoming_email(event):
    # Handle different input sources
    if 'Records' in event:  # SNS/SQS
        message = json.loads(event['Records'][0]['Sns']['Message'])
    elif 'body' in event:   # API Gateway
        message = json.loads(event['body'])
    else:                   # Direct invocation
        message = event
    
    return {
        'email_id': f"email_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        'subject': message.get('subject', 'No Subject'),
        'from': message.get('from', 'unknown@example.com'),
        'body': message.get('body', ''),
        'received_at': datetime.now().isoformat(),
        'status': 'received'
    }
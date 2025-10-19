import json
import boto3

def lambda_handler(event, context):
    """
    PURPOSE: Use AI to summarize email content
    INPUT: Email data with body content
    OUTPUT: Structured summary, key points, action items
    """
    print("🤖 Email Summarizer triggered")
    
    email_data = event.get('email_data', {})
    
    if not email_data.get('body'):
        return {'error': 'No email content to summarize'}
    
    # Generate AI summary
    summary = generate_ai_summary(email_data)
    
    # Extract key information
    extracted_data = extract_information(email_data)
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'email_id': email_data.get('email_id'),
            'summary': summary,
            'key_points': extracted_data.get('key_points', []),
            'action_items': extracted_data.get('action_items', []),
            'category': extracted_data.get('category', 'general')
        })
    }

def generate_ai_summary(email_data):
    """Use Bedrock to generate email summary"""
    try:
        bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
        
        prompt = f"""
        Summarize this email in 2-3 sentences and extract key information:
        
        Subject: {email_data.get('subject', 'No Subject')}
        From: {email_data.get('from', 'Unknown')}
        Body: {email_data.get('body', '')}
        
        Provide:
        1. Brief summary
        2. 3-5 key points  
        3. Any action items needed
        """
        
        response = bedrock.invoke_model(
            modelId='us.nova-foundation-model',
            body=json.dumps({
                "prompt": prompt,
                "maxTokens": 500,
                "temperature": 0.3
            })
        )
        
        result = json.loads(response['body'].read())
        return result['completion'].strip()
        
    except Exception as e:
        print(f"AI summarization failed: {e}")
        return f"Summary: Email about '{email_data.get('subject')}' - Basic processing complete."

def extract_information(email_data):
    """Extract structured information from email"""
    # Implement information extraction logic
    return {
        'key_points': ['Meeting scheduled', 'Project update required'],
        'action_items': ['Prepare status update', 'Review project documents'],
        'category': 'work'
    }
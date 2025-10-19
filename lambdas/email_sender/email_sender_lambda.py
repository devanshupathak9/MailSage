import json

def lambda_handler(event, context):
    """
    PURPOSE: Send emails via SES/Gmail API
    INPUT: Recipient, subject, body, attachments
    OUTPUT: Send confirmation
    """
    print("✉️ Email Sender triggered")
    
    send_data = {
        'to': event.get('to'),
        'subject': event.get('subject', 'No Subject'),
        'body': event.get('body', ''),
        'from': event.get('from', 'noreply@mailsage.ai')
    }
    
    # Validate required fields
    if not send_data['to']:
        return {'error': 'Missing recipient email'}
    
    # Send email (implement SES or Gmail API)
    result = send_via_ses(send_data)
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Email sent successfully',
            'message_id': result.get('message_id'),
            'to': send_data['to']
        })
    }

def send_via_ses(email_data):
    # TODO: Implement Amazon SES integration
    print(f"📤 SENDING EMAIL: To: {email_data['to']}, Subject: {email_data['subject']}")
    return {'message_id': 'mock_message_id_123'}
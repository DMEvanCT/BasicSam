import boto3 
import os
import uuid
import json

INSURE_TABLE = os.getenv('TABLE_NAME')
if not INSURE_TABLE:
    raise ValueError("Environment variable TABLE_NAME is not set")

def lambda_handler(event, context):
    # Get the body from the event
    body = event.get('body')
    if body is None:
        return {
            "statusCode": 400,
            "body": "No body provided"
        }

    # Parse the body if it's in JSON format
    try:
        body = json.loads(body)
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": "Invalid JSON format in body"
        }

    # Initialize DynamoDB resource
    dynamo = boto3.resource('dynamodb')
    
    # Generate a unique ID
    dynamo_id = str(uuid.uuid4())
    
    # Extract fields from the parsed body
    FirstName = body.get('FirstName')
    LastName = body.get('LastName')
    Age = body.get('Age')
    Email = body.get('Email')
    Phone = body.get('Phone')
    Address = body.get('Address')

    # Ensure all required fields are provided
    if not all([FirstName, LastName, Age, Email, Phone, Address]):
        return {
            "statusCode": 400,
            "body": "Missing one or more required fields"
        }

    # Write to DynamoDB
    try:
        dynamo.Table(INSURE_TABLE).put_item(
            Item={
                "id": dynamo_id,
                'firstName': FirstName,
                'lastName': LastName,
                'age': Age,
                'email': Email,
                'phone': Phone,
                'address': Address
            }
        )
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error inserting item into DynamoDB: {str(e)}"
        }

    # Return a success response
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Item inserted successfully",
            "id": dynamo_id
        })
    }

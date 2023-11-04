import boto3
import csv
import os

def lambda_handler(event, context):
    # Initialize AWS clients
    iam_client = boto3.client('iam')
    s3_client = boto3.client('s3')
    
    # Retrieve the list of users
    response = iam_client.list_users()
    users = response['Users']
    
    # Create a temporary CSV file in the /tmp directory
    csv_filename = '/tmp/user_list.csv'
    csv_fields = ['Username', 'UserId', 'CreateDate']
    
    # Write user information to the CSV file
    with open(csv_filename, 'w', newline='') as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=csv_fields)
        csv_writer.writeheader()
        
        for user in users:
            csv_writer.writerow({
                'Username': user['UserName'],
                'UserId': user['UserId'],
                'CreateDate': user['CreateDate'].strftime('%Y-%m-%d %H:%M:%S')
            })
    
    # Set S3 bucket and key
    s3_bucket = 'iam-users12345' #use your own S3 bucket
    s3_key = 'user_list.csv'
    
    # Upload the CSV file to S3
    s3_client.upload_file(csv_filename, s3_bucket, s3_key)
    
    return {
        'statusCode': 200,
        'body': 'User information has been stored in S3.'
    }

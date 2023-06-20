import boto3
import csv
from io import StringIO

def lambda_handler(event, context):

    # Create a CSV file in memory
    csv_buffer = StringIO()
    writer = csv.writer(csv_buffer)
    
    csv_data = ['nomnoms', 'Age', 'Country']
    writer.writerow(csv_data)
    
    csv_data = ['John Doe', 30, 'USA']
    writer.writerow(csv_data)
    
    csv_data = ['Jane Smith', 25, 'Canada']
    writer.writerow(csv_data)
    
    # Save the CSV file to S3
    s3 = boto3.resource('s3')
    bucket_name = 'lambdamonitor'
    file_name = 'test2.csv'
    
    s3.Object(bucket_name, file_name).put(Body=csv_buffer.getvalue())
    
    return {
        'statusCode': 200,
        'body': 'CSV file created and saved to S3 successfully.'
    }

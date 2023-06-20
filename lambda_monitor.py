import boto3
import csv
from io import StringIO

lambdas = boto3.client('lambda')

def lambda_handler(event, context):

    totalsize = 0
    
    # Create a CSV file in memory
    csv_buffer = StringIO()
    writer = csv.writer(csv_buffer)
    
    #add headers
    csv_data = ['Name', 'Version', 'Size']
    writer.writerow(csv_data)
    
    #Get a list of all Lambda functions and all versions
    lambdalist = lambdas.list_functions(FunctionVersion='ALL', MaxItems=9999)
    
    #Iterate through the list of functions
    for function in lambdalist['Functions']:
        
        #calculate the total code size
        totalsize = totalsize + function['CodeSize']
        
        #create the CSV row
        csv_data = [function['FunctionName'], function['Version'], function['CodeSize']]
        writer.writerow(csv_data)
    
    #add row for total code size
    csv_data = ['Total', 'None', totalsize]
    writer.writerow(csv_data)
    
     # Save the CSV file to S3
    s3 = boto3.resource('s3')
    bucket_name = 'lambdamonitor'
    file_name = 'function-info.csv'
    
    #insert the CSV file into the S3 bucket
    s3.Object(bucket_name, file_name).put(Body=csv_buffer.getvalue())

    return {'statusCode' : 200, 'LambdaStats' : 'success'}

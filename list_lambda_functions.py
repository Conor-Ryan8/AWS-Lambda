import boto3

cloudwatch = boto3.client('cloudwatch', region_name='eu-north-1')
lambdas = boto3.client('lambda', region_name='eu-north-1')

def lambda_handler(event, context):
    lambda_list = lambdas.list_functions(FunctionVersion='ALL', MaxItems=123)
    print(lambda_list)
    return lambda_list

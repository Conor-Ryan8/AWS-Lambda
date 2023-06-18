import boto3

lambdas = boto3.client('lambda', region_name='eu-north-1')

function_list = []

def lambda_handler(event, context):
    
    lambda_list = lambdas.list_functions(FunctionVersion='ALL', MaxItems=123)
    
    for function in lambda_list['Functions']:
        name = function['FunctionName']
        codesize = str(function['CodeSize']) + " bytes"
        memsize = str(function['MemorySize']) + "MB"
        version = function['Version']
        function_list.append([name, codesize, memsize, version])
        
    return function_list

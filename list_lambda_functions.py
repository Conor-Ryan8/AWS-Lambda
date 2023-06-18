import boto3

lambdas = boto3.client('lambda', region_name='eu-north-1')

function_list = {}

def lambda_handler(event, context):

    lambda_list = lambdas.list_functions(FunctionVersion='ALL', MaxItems=123)

    for function in lambda_list['Functions']:

        name = function['FunctionName']
        codesize = str(function['CodeSize']) + " bytes"
        memsize = str(function['MemorySize']) + "MB"
        version = function['Version']

        if name in function_list.keys():
            function_list[name].append({'Version:' : version, 'CodeSize:' : codesize, 'MemorySize:' : memsize})
        else:
            function_list[name] = [{'Version:' : version, 'CodeSize:' : codesize, 'MemorySize:' : memsize}]

    return {'statusCode' : 200, 'function list' : function_list}

import boto3

lambdas = boto3.client('lambda')

def lambda_handler(event, context):
    
    functions = {}
    size = 0
    
    #Get a list of all Lambda functions and all versions
    lambdalist = lambdas.list_functions(FunctionVersion='ALL', MaxItems=9999)
    
    #Iterate through the list of functions
    for function in lambdalist['Functions']:
        
        #Extract the function name
        name = function['FunctionName']
        
        #Extract the function version
        version = function['Version']
        
        #Extract the code size
        codesize = str(function['CodeSize']) + " bytes"

        #calculate the total code size
        size = size + function['CodeSize']

        #Check if function is already in payload
        if name in functions.keys():
            
            #If it is then add a new version for this function
            functions[name].append({'Version:' : version, 'CodeSize:' : codesize})
        else:
            #If it is not then add this version to the payload
            functions[name] = [{'Version:' : version, 'CodeSize:' : codesize}]

    #Add the total code size to the payload
    functions['TotalSize'] = str(size) + " bytes"

    #Check if the total code size exceeds 90% of 75GB
    if size >= 72477573120:
        functions['Alert'] = "YES"
    else:
        functions['Alert'] = "NO"
    
    #Return the payload
    return {'statusCode' : 200, 'function list' : functions}

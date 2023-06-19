import boto3

lambdas = boto3.client('lambda')

def get_lambda_list():
    
    functionlist = {}
    totalsize = 0
    
    #Get a list of all Lambda functions and all versions
    lambdalist = lambdas.list_functions(FunctionVersion='ALL', MaxItems=9999)
    
    #Iterate through the list of functions
    for function in lambdalist['Functions']:
        
        #Extract the function name
        name = function['FunctionName']
        
        #Extract the function version
        version = function['Version']
        
        #Extract the code size
        codesize = function['CodeSize']

        #calculate the total code size
        totalsize = totalsize + function['CodeSize']

        #Check if function is already in payload
        if name in functionlist.keys():
            
            #If it is then add a new version for this function
            functionlist[name].append({'VersionName' : version, 'CodeSize' : codesize})
        else:
            #If it is not then add this version to the payload
            functionlist[name] = [{'VersionName' : version, 'CodeSize' : codesize}]
            
    return totalsize, functionlist


def lambda_handler(event, context):
    
    totalsize, functionlist = get_lambda_list()
    
    functioninfo = {}
    
    #Add the total code size to the payload
    functioninfo['TotalSize'] = str(totalsize) + " bytes"

    #Check if the total code size exceeds 90% of 75GB
    if totalsize >= 72477573120:
        functioninfo['EmailAlert'] = "YES"
        # Send Email alert 
    else:
        functioninfo['EmailAlert'] = "NO"
        
    #Sort and process the function data
    for item in functionlist.items():
    
        name = item[0]
        
        #if only 1 version exists
        if len(item[1]) == 1:
            
            #Update the function info
            functioninfo[name] = {'Versioning' : 'Disabled'}
            functioninfo[name]['Size'] = item[1][0]['CodeSize']

        #if multiple versions exist
        else:
            #Update the function info
            functioninfo[name] = {'Versioning' : 'Enabled'}
            functioninfo[name]['VersionCount'] = len(item[1])
            
            #track the largest and smallest versions
            largestsize = 0
            largestname = ''
            smallestsize = item[1][0]['CodeSize']
            smallestname = ''
            
            #iterate through the versions
            for version in item[1]:
                
                #if the version is latest
                if version['VersionName'] == '$LATEST':
                    functioninfo[name]['Size'] = version['CodeSize']
                
                #find largest version
                if version['CodeSize'] > largestsize:
                    largestsize = version['CodeSize']
                    largestname = version['VersionName']
                
                #find smallest version
                if version['CodeSize'] < smallestsize:
                    smallestsize = version['CodeSize']
                    smallestname = version['VersionName']
            
            #update function info
            functioninfo[name]['LargestVersion'] = {'Name' : largestname, 'Size' : largestsize}
            functioninfo[name]['SmallestVersion'] = {'Name' : smallestname, 'Size' : smallestsize}
   
    return {'statusCode' : 200, 'LambdaStats' : functioninfo}

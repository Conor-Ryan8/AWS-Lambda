import boto3

def lambda_handler(event, context):

    sns = boto3.client('sns')

    sns.publish(
    TopicArn='arn:aws:sns:eu-north-1:248997530403:LambdaCapacityAlert',
    Message='Lambda Code Size has reached 90% capacity!',
    Subject='Capacity Alert!'
    )

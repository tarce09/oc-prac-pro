import os
import boto3
username = 'aryan09'
password = 'ARYan@#2001'
try:
    client = boto3.client('cognito-idp', region_name='us-east-1')
    response = client.initiate_auth(
        ClientId="5u8q10mi2u3fe17f0bpu6ucnpn",
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': username,
            'PASSWORD': password
        }
    )
    '''
    print('*********************')
    print('AccessToken', response['AuthenticationResult']['AccessToken'])
    print('*********************')
    print('RefreshToken', response['AuthenticationResult']['RefreshToken'])
    '''
    access_token = response['AuthenticationResult']['AccessToken']
    response = client.get_user(
        AccessToken=access_token
    )
    attr_sub = None
    for attr in response['UserAttributes']:
        if attr['Name'] == 'name':
            attr_sub = attr['Value']
            break
    print("Welcome " + attr_sub)

except:
    print("Invalid credentials or sign up")
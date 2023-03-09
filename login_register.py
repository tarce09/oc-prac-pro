import boto3
import hashlib

def register(email,name,password,age,gender):
    table_name= 'Users'
    dynamodb_resource = boto3.resource("dynamodb")
    table = dynamodb_resource.Table(table_name)
    
    get_response = table.get_item(
        Key = {
           "Email":email
        }
    )
    if 'Item' in get_response:
        response = "user exists"
    else:
        
        hashed=hashlib.sha256(password.encode())
        response = table.put_item(
            Item={
                "Email":email,
                "Name":name,
                "Password":hashed.hexdigest(),
                "Age":age,
                "Gender":gender
            },
            ReturnConsumedCapacity="TOTAL"
        )
        
        
def login(email,password):
    table_name= 'Users'
    dynamodb_resource = boto3.resource("dynamodb")
    table = dynamodb_resource.Table(table_name)
    try:
        get_response = table.get_item(
            Key = {
            "Email":email
            }
        )
        hashed=hashlib.sha256(password.encode())
        if(get_response['Item']['Password']==hashed.hexdigest()):
            print("logged in")
            user = get_response['Item']
            print(user)
        else:
            print('invalid password')
    except:
        print('invalid email')
        

#register('aryan@mail.com','aryan','aryan2001',21,'male')
#login('aryan@mail.com','aryan2001')


import boto3
#import json


def get_train(tr_no,pnr,status):
    dynamodb = boto3.resource('dynamodb')

    travel_table = dynamodb.Table('TrainTravel')
    get_response = travel_table.get_item(
    Key = {
       "Tr_no":tr_no
    }
)

    tr_no = get_response['Item']['Tr_no']
    route_id = get_response['Item']['RouteId'] # To get Route ID
    train_id = get_response['Item']['TrainId'] # To get Train ID
    arr_time = get_response['Item']['Arrivaltime'] # To get Arrival Time
    dep_time = get_response['Item']['Deptime'] # To get Departure Time
    fro, to = get_route(route_id)
    train_name,capacity = get_train_name(train_id)
    if status == 'Waiting':
        waiting_list = get_response['Item']['Waitinglist']
        waiting_no = waiting_list.index('Mumbai') + 1
        return tr_no,arr_time,dep_time,waiting_no,fro,to,train_name
    return tr_no,arr_time,dep_time,fro,to,train_name

            

    # while 'LastEvaluatedKey' in response:
    #     response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    #     data.extend(response['Items'])


def get_route(route_id):
    dynamodb = boto3.resource('dynamodb')

    route_table = dynamodb.Table('TrainRoutes')
    get_response = route_table.get_item(
        Key = {
           "RouteId":route_id
        }
    ) 
    fro = get_response['Item']['From']
    to = get_response['Item']['To']
    return fro,to

def get_train_name(train_id):
    dynamodb = boto3.resource('dynamodb')

    train_table = dynamodb.Table('Trains')

    get_response = train_table.get_item(
        Key = {
           "TrainId":train_id
        }
    )   
    train_name = get_response['Item']['Name']
    capacity = get_response['Item']['Capacity']
    return train_name,capacity

def get_train_details(pnr):
    full_info = {}
    dynamodb = boto3.resource('dynamodb')

    booking_table = dynamodb.Table('Bookings')

    get_response = booking_table.get_item(
        Key = {
           "PNR":pnr
        }
    )
    tr_no = get_response['Item']['Tr_no']
    seat_no = get_response['Item']['SeatNo']
    status = get_response['Item']['Status']
    name = get_response['Item']['Name']
    email = get_response['Item']['Email']
    age = get_response['Item']['Age']
    gender = get_response['Item']['Gender']
    


    if status == 'Waiting':
        tr_no,arr_time,dep_time,waiting_no,fro,to,train_name = get_train(tr_no,pnr,status)
        full_info.update({'Name':name, 'Email':email,'Age':age, 'Gender':gender, 'Tr_no':tr_no, 'From':fro, 'To':to, 'Train Name':train_name, 'Arrival_Time':arr_time, 'Departure_Time':dep_time, 'Waiting_No':waiting_no, 'Status':status})
    else:
        tr_no,arr_time,dep_time,fro,to,train_name = get_train(tr_no,pnr,status)
        full_info.update({'Name':name, 'Email':email,'Age':age, 'Gender':gender, 'Tr_no':tr_no, 'From':fro, 'To':to, 'Train Name':train_name, 'Arrival_Time':arr_time, 'Departure_Time':dep_time, 'Seat_No':seat_no, 'Status':status})

    print(full_info)
        


get_train_details('8W6OKP1I')  

    



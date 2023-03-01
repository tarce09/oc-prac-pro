import boto3
from boto3.dynamodb.conditions import Attr
#import json
def get_route(route_id):
    print(route_id)
    dynamodb = boto3.resource('dynamodb')

    route_table = dynamodb.Table('TrainRoutes')
    get_response = route_table.get_item(
        Key = {
           "RouteId":route_id
        }
    ) 
    print(get_response)
    fro = get_response['Item']['From']
    to = get_response['Item']['To']
    return fro,to


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



def get_train_name(train_id):
    dynamodb = boto3.resource('dynamodb')

    train_table = dynamodb.Table('Trains')

    get_response = train_table.get_item(
        Key = {
           "TrainId":train_id
        }
    )   
    train_name = get_response['Item']['Name']
    capacity = int(get_response['Item']['Capacity'])
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
        full_info.update({'Name':name, 'Email':email,'Age':int(age), 'Gender':gender, 'Tr_no':int(tr_no), 'From':fro, 'To':to, 'Train_Name':train_name, 'Arrival_Time':arr_time, 'Departure_Time':dep_time, 'Waiting_No':int(waiting_no), 'Status':status})
    else:
        tr_no,arr_time,dep_time,fro,to,train_name = get_train(tr_no,pnr,status)
        full_info.update({'Name':name, 'Email':email,'Age':int(age), 'Gender':gender, 'Tr_no':int(tr_no), 'From':fro, 'To':to, 'Train_Name':train_name, 'Arrival_Time':arr_time, 'Departure_Time':dep_time, 'Seat_No':int(seat_no), 'Status':status})

    print(full_info)
    
    
    return full_info
        
def view_route(route_id):
    dynamodb = boto3.resource('dynamodb')
    travel_table = dynamodb.Table('TrainTravel')
    response = travel_table.scan(
    FilterExpression=Attr('RouteId').eq(route_id)
    )
    view_trains = []
    no_of_trains = len(response['Items'])
    for i in range(no_of_trains):
        train_id = response['Items'][i]['TrainId']
        len_seats = len(response['Items'][i]['Availableseats'])
        len_wait = len(response['Items'][i]['Waitinglist'])
        arr_time = response['Items'][i]['Arrivaltime']
        dep_time = response['Items'][i]['Deptime']
        train_name, capacity = get_train_name(train_id)
        tr_no=response['Items'][i]['Tr_no']
        view_trains.append({'Tr_no':tr_no,'Train_Name':train_name, 'Capacity':capacity, 'AvaiableSeats': len_seats, 'Arrival_Time':arr_time, 'Departure_Time':dep_time, 'Waiting': len_wait})
    print(view_trains)

def get_train_travel(tr_no):
    dynamodb = boto3.resource('dynamodb')
    travel_table = dynamodb.Table('TrainTravel')
    get_response = travel_table.get_item(
        Key = {
           "Tr_no":tr_no
        }
    )
    res={}
    res['Tr_no']=int(get_response['Item']['Tr_no'])
    res['Waiting']=len(get_response['Item']['Waitinglist'])
    res['Deptime']=get_response['Item']['Deptime']
    res['Arrivaltime']=get_response['Item']['Arrivaltime']
    res['Available']=len(get_response['Item']['Availableseats'])
    
    train_table = dynamodb.Table('Trains')
    new_response = train_table.get_item(
        Key = {
           "TrainId":get_response['Item']['TrainId']
        }
    )
    res['Train_name']=new_response['Item']['Name']
    res['Route']=get_response['Item']['RouteId']
    
    return res
    
    
    
    
#get_train_details('BXZ6NUTV')  

view_route('Che-Mum')    

#get_train_travel(1)


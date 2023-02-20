import boto3
import json


def get_train(tr_no,pnr,status):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('TrainTravel')

    response = table.scan()
    data = response['Items'] 
    
    for i in range(len(data)):
        if data[i]['Tr_no'] == tr_no:
            tr_no = data[i]['Tr_no']
            route_id = data[i]['RouteId'] # To get Route ID
            train_id = data[i]['TrainId'] # To get Train ID
            arr_time = data[i]['Arrivaltime'] # To get Arrival Time
            dep_time = data[i]['Deptime'] # To get Departure Time
            fro, to = get_route(route_id)
            train_name,capacity = get_train_name(train_id)
            if status == 'Waiting':
                waiting_list = data[i]['Waitinglist']
                for j in range(len(waiting_list)):
                    if waiting_list[j] == pnr:
                        waiting_no = j+1
                    return tr_no,arr_time,dep_time,waiting_no,fro,to,train_name
            return tr_no,arr_time,dep_time,fro,to,train_name

            
    

    # while 'LastEvaluatedKey' in response:
    #     response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    #     data.extend(response['Items'])


def get_route(route_id):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('TrainRoutes')

    response = table.scan()
    list_of_routes = response['Items']
    for i in range(len(list_of_routes)):
        if list_of_routes[i]['RouteId'] == route_id:
            fro = list_of_routes[i]['From']
            to = list_of_routes[i]['To']
            return fro,to
            # print(list_of_routes[i]['From'])
            # print(list_of_routes[i]['To'])

def get_train_name(train_id):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('Trains')

    response = table.scan() 
    list_of_train_names = response['Items']
    for i in range(len(list_of_train_names)):
        if list_of_train_names[i]['TrainId'] == train_id:
            train_name = list_of_train_names[i]['Name']
            capacity = list_of_train_names[i]['Capacity']
            return train_name,capacity

def get_train_details(pnr):
    full_info = []
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('Bookings')

    response = table.scan()
    list_of_tickets = response['Items']
    for i in range(len(list_of_tickets)):
        if list_of_tickets[i]['PNR'] == pnr:
            tr_no = list_of_tickets[i]['Tr_no']
            seat_no = list_of_tickets[i]['SeatNo']
            status = list_of_tickets[i]['Status']
            name = list_of_tickets[i]['Name']
            email = list_of_tickets[i]['Email']
            age = list_of_tickets[i]['Age']
            gender = list_of_tickets[i]['Gender']
    


    if status == 'Waiting':
        tr_no,arr_time,dep_time,waiting_no,fro,to,train_name = get_train(tr_no,pnr,status)
        full_info.extend([name,email,age,gender,tr_no,fro,to,train_name,arr_time,dep_time,waiting_no,status])
    else:
        tr_no,arr_time,dep_time,fro,to,train_name = get_train(tr_no,pnr,status)
        full_info.extend([name,email,age,gender,tr_no,fro,to,train_name,arr_time,dep_time,seat_no,status])
    print(full_info)
        


get_train_details('8W6OKP1I')
get_train_details('AUQ0Y6H8')
    



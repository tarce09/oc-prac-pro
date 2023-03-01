import boto3
import json
import string    
import random
from datetime import datetime


def put_train():
    table_name= 'TrainTravel'
    dynamodb_resource = boto3.resource("dynamodb")
    table = dynamodb_resource.Table(table_name)
    arr1=[]
    for i in range(1,11):
        arr1.append(int(i))
    response = table.put_item(
        Item={
            "Tr_no":3,
            "RouteId":"Che-Mum",
            "TrainId":1,
            "Deptime":"02/27/23 13:55:26",
            "Arrivaltime":"02/28/23 03:35:46",
            "Availableseats":arr1,
            "Waitinglist":[]
        },
        ReturnConsumedCapacity="TOTAL"
    )
    print(json.dumps(response, indent=2))



def add_booking(Tr_no,Email,Name,Age,Gender):
    fetch_table='TrainTravel'
    dynamodb_resource = boto3.resource("dynamodb")
    db_fetch=boto3.resource("dynamodb")
    get_table = db_fetch.Table(fetch_table)
    get_response = get_table.get_item(
        Key = {
           "Tr_no":Tr_no
        }
    )
    item = get_response['Item']
    all_seats=item['Availableseats']
        
    status="Booked"
    
    table_name= 'Bookings'    
    table = dynamodb_resource.Table(table_name)
    while(True):
        pnr = str("".join(random.choices(string.ascii_uppercase + string.digits, k = 8)))
        response=table.get_item(
            Key = {
                "PNR":pnr
            }
        )
        print(response)
        if 'Item' in response:
            print(pnr)
        else:
            break

        
    print(pnr)
    if(len(all_seats)==0):
        status="Waiting"
        wait_list=item['Waitinglist']
        print(wait_list)
        wait_list.append(pnr)
        item['Waitinglist']=wait_list
        taken_seat=-1
        print(wait_list)
    elif(len(all_seats)>0):
        taken_seat = all_seats[0]
        print(taken_seat)
        all_seats.remove(taken_seat)
        item['Availableseats']=all_seats

    get_table.put_item(
        Item=item
    )
        
    now = datetime.now()
        
    dt=str(now.strftime("%d/%m/%Y %H:%M:%S"))
    response = table.put_item(
        Item={
            "PNR":pnr,
            "Tr_no":Tr_no,
            "Email": Email,
            "Name": Name,
            "Age" : Age,
            "Gender": Gender,
            "SeatNo": taken_seat,
            "Time and date" : dt,
            "Status": status
        },
    ReturnConsumedCapacity="TOTAL"
    )
    
    print("created successfuly")


    
#put_train()
#add_booking(2,"mrraju2","myrajumail",63,"gg")
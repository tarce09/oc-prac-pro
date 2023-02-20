import boto3
from update_ops import updateTrainTravelonCancel
from datetime import datetime

def cancel_booking(pnr):
    
    BookingsResource=boto3.resource('dynamodb')
    BookingsTable=BookingsResource.Table('Bookings')
    
    get_response = BookingsTable.get_item(
        Key = {
           "PNR":pnr
        }
    )
    item = get_response['Item']
    tr_no=item['Tr_no']
    
    
    
    if check_time_diff(tr_no)==True and item['Status']!="Canceled":
        item['Status']='Canceled'
        seatno = item['SeatNo']
        item['SeatNo']=-1
        response = BookingsTable.put_item(
            Item=item,
        ReturnConsumedCapacity="TOTAL"
        )
        updateTrainTravelonCancel(seatno,tr_no)
    else:
        print("ticket cannot be canceled 48 hrs prior to departure or has been previously canceled")
        return
    


def check_time_diff(tr_no):   
    TrainTravelResource=boto3.resource('dynamodb')
    TrainTravelTable=TrainTravelResource.Table('TrainTravel')
    
    get_response = TrainTravelTable.get_item(
        Key = {
           "Tr_no":tr_no
        }
    )
    item=get_response['Item']
    
    data1 = datetime.now()
    data2=item['Deptime']
    datetime_object = datetime.strptime(data2, '%m/%d/%y %H:%M:%S')
    diff = datetime_object - data1

    days, seconds = diff.days, diff.seconds
    hours = days * 24 + seconds // 3600
    
    if hours<49:
        return False
    else:
        return True
    

cancel_booking('YHUF2ALQ')
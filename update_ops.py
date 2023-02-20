import boto3


def updateWaitingonCancel(tr_no):
    TrainTravelResource=boto3.resource('dynamodb')
    TrainTravelTable=TrainTravelResource.Table('TrainTravel')
    
    get_response = TrainTravelTable.get_item(
        Key = {
           "Tr_no":tr_no
        }
    )
    item=get_response['Item']
    
    seat_no=item['Availableseats'][0]
    item['Availableseats'].remove(seat_no)
    
    waiting_pnr=item['Waitinglist'][0]
    item['Waitinglist'].remove(waiting_pnr)
    
    response = TrainTravelTable.put_item(
        Item=item,
    ReturnConsumedCapacity="TOTAL"
    )
    
    BookingsResource=boto3.resource('dynamodb')
    BookingsTable=BookingsResource.Table('Bookings')
    
    get_response = BookingsTable.get_item(
        Key = {
           "PNR":waiting_pnr
        }
    )
    item = get_response['Item']
    item['Status']='Booked'
    item['SeatNo']=seat_no
    print(seat_no,waiting_pnr)
    
    response = BookingsTable.put_item(
        Item=item,
    ReturnConsumedCapacity="TOTAL"
    )
    
def updateTrainTravelonCancel(seatno,tr_no):
    TrainTravelResource=boto3.resource('dynamodb')
    TrainTravelTable=TrainTravelResource.Table('TrainTravel')
    
    get_response = TrainTravelTable.get_item(
        Key = {
           "Tr_no":tr_no
        }
    )
    item=get_response['Item']
    
    lst_avlb=item['Availableseats']
    lst_avlb.append(seatno)
    lst_avlb.sort()
    item['Availableseats']=lst_avlb
    
    response = TrainTravelTable.put_item(
        Item=item,
    ReturnConsumedCapacity="TOTAL"
    )
    
    wait_len=len(item['Waitinglist'])
    if(wait_len>0):
        updateWaitingonCancel(tr_no)
    else:
        return None
        

    

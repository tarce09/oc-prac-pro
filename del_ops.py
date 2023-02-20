import boto3
from update_ops import updateTrainTravelonCancel

def cancel_booking(pnr):
    BookingsResource=boto3.resource('dynamodb')
    BookingsTable=BookingsResource.Table('Bookings')
    
    get_response = BookingsTable.get_item(
        Key = {
           "PNR":pnr
        }
    )
    item = get_response['Item']
    item['Status']='Canceled'
    seatno = item['SeatNo']
    tr_no=item['Tr_no']
    item['SeatNo']=-1
    
    response = BookingsTable.put_item(
        Item=item,
    ReturnConsumedCapacity="TOTAL"
    )
    
    updateTrainTravelonCancel(seatno,tr_no)
    
    
cancel_booking('302D6JFM')
    
    
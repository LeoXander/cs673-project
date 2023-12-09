import requests
import json
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get('/serviceproviderreport')
async def get_service_rpt(serviceName:str|None=None):
    # Request Services Offered API for service report
    servOfferedresponse = requests.get('https://team3-598fa58116f6.herokuapp.com/api/servicesOffered')
    if servOfferedresponse.status_code != 200:
        raise HTTPException(status_code=404, detail="Service Offered API Error")
    bookingsresponse = requests.get('https://team3-598fa58116f6.herokuapp.com/api/booking/details')
    if bookingsresponse.status_code != 200:
        raise HTTPException(status_code=404, detail="Bookings API Error")
    servicesOfferedJson = servOfferedresponse.json()
    bookingsJson = bookingsresponse.json()
    servicesList=[]
    serviceRptJson = {'services':list}
    if serviceName is not None:
        allRecordsFlag = False
    else:
        allRecordsFlag = True
    for service in servicesOfferedJson:
        services={}
        for key,value in service.items():
            if allRecordsFlag == True or service['serviceName']==serviceName:
                if key not in ['id','skillId','vendorId']:
                    services[key] = value
                elif key == 'id':
                    bookingList = []
                    bookingsDict = {}
                    for booking in bookingsJson:
                        for k, v in booking.items():
                            if value == booking['serviceId']:
                                if k == 'bookings':
                                    for book in v:
                                        for bk,bv in book.items():
                                            if bk not in ['serviceId','bookingId','employeeId']:
                                                bookingsDict[bk]=bv
                        bookingList.append(bookingsDict)
                    services['recentVisits'] = bookingList
        if len(services) > 0:
            servicesList.append(services)
    serviceRptJson['services']=servicesList
    serviceRptJson = json.loads(json.dumps(serviceRptJson))
    return serviceRptJson
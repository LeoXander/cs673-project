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
            if allRecordsFlag == True or service['serviceName'].lower()==serviceName.lower():
                if key not in ['id','skillId','vendorId']:
                    services[key] = value
                elif key == 'vendorId':
                    vendorId=str(value)
                    vendorApi = 'https://team3-598fa58116f6.herokuapp.com/api/vendors/'+vendorId
                    vendorresponse = requests.get(vendorApi)
                    if vendorresponse.status_code != 200:
                        raise HTTPException(status_code=404, detail="Vendors API Error")
                    vendorsJson = vendorresponse.json()
                    services['serviceProviderName']=vendorsJson['name']
                elif key == 'id':
                    bookingList = []
                    bookingsDict = {}
                    for booking in bookingsJson:
                        for k, v in booking.items():
                            if value == booking['serviceId']:
                                if k == 'bookings':
                                    for book in v:
                                        for bk,bv in book.items():
                                            if bk == 'status':
                                                if bv is None:
                                                    bookingsDict[bk]="Completed"
                                                else:
                                                    bookingsDict[bk]=bv
                                            if bk not in ['serviceId','bookingId','employeeId','status']:
                                                bookingsDict[bk]=bv
                        if len(bookingsDict) > 0:
                            bookingList.append(bookingsDict)
                    services['recentVisits'] = bookingList
        if len(services) > 0:
            servicesList.append(services)
    serviceRptJson['services']=servicesList
    serviceRptJson = json.loads(json.dumps(serviceRptJson))
    return serviceRptJson
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
    patientsresponse = requests.get('https://patient-intake-api-8ce23f3e5c62.herokuapp.com/patients')
    if patientsresponse.status_code != 200:
        raise HTTPException(status_code=404, detail="Patient Intake API Error")
    servicesOfferedJson = servOfferedresponse.json()
    bookingsJson = bookingsresponse.json()
    patientsJson = patientsresponse.json()
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
                    averageRating=0
                    noBookings = 0
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
                                            if bk == 'remarks':
                                                if bv is None:
                                                    bookingsDict[bk]='No remarks'
                                                else:
                                                    bookingsDict[bk]=bv
                                            if bk == 'startTime':
                                                if bv is None:
                                                    bookingsDict[bk]='2023-12-01T09:00:00'
                                                else:
                                                    bookingsDict[bk]=bv
                                            if bk == 'endTime':
                                                if bv is None:
                                                    bookingsDict[bk]='2023-12-31T09:00:00'
                                                else:
                                                    bookingsDict[bk]=bv
                                            if bk == 'bookingId':
                                                url = 'https://team3-598fa58116f6.herokuapp.com/api/progress-notes/booking/'+str(bv)
                                                ratingresponse = requests.get(url)
                                                if ratingresponse.status_code == 200:
                                                    ratingsJson=ratingresponse.json()
                                                    for rating in ratingsJson:
                                                        for rKey,rVal in rating.items():
                                                            if rKey not in ['bookingId','id','goalId']:
                                                                if rVal is not None:
                                                                    averageRating += int(rVal)/4
                                                                    noBookings+=1
                                                                else:
                                                                    averageRating += 5/4
                                                                    noBookings+=1
                                                else:
                                                    averageRating += 5
                                                    noBookings+=1
                                            if bk == 'patientId':
                                                bookingsDict[bk]=bv
                        if len(bookingsDict) > 0:
                            bookingList.append(bookingsDict)
                    services['recentVisits'] = bookingList
                    if noBookings!=0:
                        services['rating']=averageRating/noBookings
                    else:
                        services['rating']=averageRating
        if len(services) > 0:
            servicesList.append(services)
    serviceRptJson['services']=servicesList
    serviceRptJson = json.loads(json.dumps(serviceRptJson))
    return serviceRptJson
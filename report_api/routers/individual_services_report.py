import requests
import json
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get('/servicesachievementsreport')
async def get_service_achievement_rpt(serviceName:str|None=None):
    servicesAchievementRptJson = {}
    bookingsAllResponse = requests.get('https://team3-598fa58116f6.herokuapp.com/api/bookings/all')
    if bookingsAllResponse.status_code != 200:
        raise HTTPException(status_code=404, detail="Bookings API Error")
    bookingAllJson = bookingsAllResponse.json()
    servOfferedresponse = requests.get('https://team3-598fa58116f6.herokuapp.com/api/servicesOffered')
    if servOfferedresponse.status_code != 200:
        raise HTTPException(status_code=404, detail="Service Offered API Error")
    servicesOfferedJson = servOfferedresponse.json()
    servicesBookingCntList = []
    if serviceName is not None:
        allRecordsFlag = False
    else:
        allRecordsFlag = True
    for service in servicesOfferedJson:
        servicesBookingCntDict = {}
        for sk, sv in service.items():
            if allRecordsFlag == True or (service['serviceName'].lower()==serviceName.lower()):
                if sk == 'id':
                    bookingScheduledCnt = 0
                    bookingCompletedCnt = 0
                    for booking in bookingAllJson:
                        for bk, bv in booking.items():
                            if sv == booking['serviceId'] and booking['serviceId'] is not None:
                                if bk == 'status':
                                    if bv is None:
                                        bookingCompletedCnt += 1
                                    else:
                                        bookingScheduledCnt += 1
                    servicesBookingCntDict['scheduledServicesCount'] = bookingScheduledCnt
                    servicesBookingCntDict['completedServicesCount'] = bookingCompletedCnt
                if sk == 'serviceName':
                    servicesBookingCntDict['serviceName'] = sv
        if len(servicesBookingCntDict) > 0:
            servicesBookingCntList.append(servicesBookingCntDict)
    servicesAchievementRptJson['services']=servicesBookingCntList
    servicesAchievementRptJson=json.loads(json.dumps(servicesAchievementRptJson))
    return servicesAchievementRptJson
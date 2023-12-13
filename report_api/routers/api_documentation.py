import json
from fastapi import APIRouter
router = APIRouter()

@router.get('/apiDocumentation')
async def apiDOcumentation():
    apiEndPoints = {}
    apiEndPointsList=[]
    apiEndPointsList.append({'Endpoint':'/serviceproviderreport','Operation':'GET','Status Codes':'200,404','Purpose':'Retrieves the data for the service provider report like services offered and the history patients and the reviews.'})
    apiEndPointsList.append({'Endpoint':'/casemanagerperformancereport','Operation':'GET','Status Codes':'200,404','Purpose':'Retrieves the data for the case manager performance report.'})
    apiEndPointsList.append({'Endpoint':'/casemanagerutilizationreport','Operation':'GET','Status Codes':'200,404','Purpose':'Retrieves the data for the case manager utilization report.'})
    apiEndPointsList.append({'Endpoint':'/demographicchart','Operation':'GET','Status Codes':'200,404','Purpose':'Retrieves the data for the demographics chart.'})
    apiEndPoints['apiEndpoints'] = apiEndPointsList
    apiEndPoints = json.loads(json.dumps(apiEndPoints))
    return apiEndPoints
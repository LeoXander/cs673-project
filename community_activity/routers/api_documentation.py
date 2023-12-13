import json
from fastapi import APIRouter
router = APIRouter()

@router.get('/apiDocumentation')
async def apiDOcumentation():
    apiEndPoints = {}
    apiEndPointsList=[]
    apiEndPointsList.append({'Endpoint':'/activitytypes','Operation':'GET','Status Codes':'200,404','Purpose':'Retrieves the activity types associated to the community event.'})    
    apiEndPointsList.append({'Endpoint':'/primaryentities','Operation':'GET','Status Codes':'200,404','Purpose':'Retrieves the primary entities associated to the community event.'})
    apiEndPointsList.append({'Endpoint':'/issueareas','Operation':'GET','Status Codes':'200,404','Purpose':'Retrieves the issue areas associated to the community event.'})
    apiEndPointsList.append({'Endpoint':'/communityactivity','Operation':'GET','Status Codes':'200,404','Purpose':'Retrieves all the community activity events in the system.'})
    apiEndPointsList.append({'Endpoint':'/communityactivity','Operation':'POST','Status Codes':'201,404','Purpose':'Add a new community activity event to the system.'})
    apiEndPointsList.append({'Endpoint':'/communityactivity','Operation':'PUT','Status Codes':'200,404','Purpose':'Update an existing community activity event to the system.'})
    apiEndPointsList.append({'Endpoint':'/communityactivity','Operation':'DELETE','Status Codes':'200,404','Purpose':'Delete an existing community activity event from the system.'})
    apiEndPointsList.append({'Endpoint':'/communityactivityreport','Operation':'GET','Status Codes':'200,404','Purpose':'Retrieve the data needed for the community activity report.'})
    apiEndPoints['apiEndpoints'] = apiEndPointsList
    apiEndPoints = json.loads(json.dumps(apiEndPoints))
    return apiEndPoints
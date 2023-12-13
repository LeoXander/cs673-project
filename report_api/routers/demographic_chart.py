from collections import defaultdict
import requests
import json
from datetime import datetime
from fastapi import APIRouter, HTTPException

router = APIRouter()

# Global function to calculate age of a patient.
def calculateAge(birthDate):
    today = datetime.today()
    patientAge = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
    return patientAge

@router.get('/demographicchart')
async def get_demographicchart(startDt:datetime|None=None, endDt: datetime|None=None):
    if (endDt is None and startDt is not None) or (endDt is not None and startDt is None):
        return json.loads(json.dumps({"error":"Invalid data entered"}))
    if endDt is not None and startDt is not None and (endDt < startDt):
        return json.loads(json.dumps({"error":"Invalid data entered"}))
    # Request Patient Intake API for patient demographics information
    response = requests.get('https://patient-intake-api-8ce23f3e5c62.herokuapp.com/patients')
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Patient Intake API Error")
    
    today = datetime.today()
    patientJson = response.json()
    sexList, dobList, ageList, disabilityList = [], [], [], []
    ageRange = {'0-9':0,'10-19':0,'20-29':0,'30-39':0,'40-49':0,'50-59':0,'60-69':0,'70-79':0,'80-89':0,'90-99':0, '> 100':0}
    sex = {'Male': 0, 'Female':0, 'Other':0}
    demographicDict = {'ageRange':list(),'sex':list(),'disabilityType':list()}
    disabilityDict=defaultdict(int)
    count = 0

    if startDt is not None and endDt is not None:
        allRecordsFlag = False
    else:
        allRecordsFlag = True
    # Iterate the Patient Intake Response JSON.
    for key, value in patientJson.items():
        for i in value:
            for k,v in i.items():
                created_Dt = datetime.strptime(i['created_at'][:-5], '%Y-%m-%dT%H:%M:%S')
                if allRecordsFlag == True or (created_Dt >= startDt and created_Dt <= endDt):
                    if k == 'gender':
                        if v is not None:
                            sexList.append(v)
                    if k == 'dob':
                        if v is not None:
                            dobList = v.split('-')
                            # Only consider patients with valid date of birth
                            if int(dobList[0]) <= today.year and int(dobList[1]) <= today.month and int(dobList[2]) <= today.day:
                                ageList.append(calculateAge(datetime(int(dobList[0]), int(dobList[1]), int(dobList[2]))))
                    if k == 'race':
                        if v is None:
                            pass

                    if k == 'disability_type':
                        count+=1
                        if count > 1 and v is None:
                            disabilityDict['Other2']+=1
                        elif v is None:
                            disabilityDict['Other']+=1
                        else:
                            disabilityDict[v]+=1
            disabilityList.append(disabilityDict)
    # Iterate the sexList to generate the count by category.
    if len(sexList) > 0:
        for s in sexList:
            if s[0] == 'M':
                sex['Male'] += 1
            elif s[0] == 'F':
                sex['Female'] += 1
            else:
                sex['Other'] += 1
    else:
        sex={'message':'No data for the entered filter'}

    # Iterate the ageList to generate the count by age ranges.
    if len(ageList) > 0:
        for a in ageList:
            if a >= 0 and a <= 9:
                ageRange['0-9']+=1
            elif a >= 10 and a <= 19:
                ageRange['10-19'] += 1
            elif a >= 20 and a <= 29:
                ageRange['20-29'] += 1
            elif a >= 30 and a <= 39:
                ageRange['30-39'] += 1
            elif a >= 40 and a <= 49:
                ageRange['40-49'] += 1
            elif a >= 50 and a <= 59:
                ageRange['50-59'] += 1
            elif a >= 60 and a <= 69:
                ageRange['60-69'] += 1
            elif a >= 70 and a <= 79:
                ageRange['70-79'] += 1
            elif a >= 80 and a <= 89:
                ageRange['80-89'] += 1
            elif a >= 90 and a <= 99:
                ageRange['90-99'] += 1
            else:
                ageRange['> 100'] += 1
    else:
        ageRange={'message':'No data for the entered filter'}

    # Populate the demographicDict with ageRanges, sex, disabilityTypes, Race and Ethnicities.
    for k,v in sex.items():
        demographicDict['sex'].append({k:v})
    for k,v in ageRange.items():
        demographicDict['ageRange'].append({k:v})
    demographicDict['disabilityType']=disabilityList
    demographicChartJson = json.loads(json.dumps(demographicDict))
    
    return demographicChartJson
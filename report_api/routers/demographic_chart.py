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
async def get_demographicchart(startDt:str|None=None, endDt: str|None=None):
    # Request Patient Intake API for patient demographics information
    response = requests.get('https://patient-intake-api-8ce23f3e5c62.herokuapp.com/patients')
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Patient Intake API Error")
    
    today = datetime.today()
    patientJson = response.json()
    sexList, dobList, ageList = [], [], []
    ageRange = {'0-9':0,'10-19':0,'20-29':0,'30-39':0,'40-49':0,'50-59':0,'60-69':0,'70-79':0,'80-89':0,'90-99':0, '> 100':0}
    sex = {'Male': 0, 'Female':0, 'Other':0}
    demographicDict = {'ageRange':list(),'sex':list()}
    
    # Iterate the Patient Intake Response JSON.
    for key, value in patientJson.items():
        for i in value:
            for k,v in i.items():
                if k == 'gender':
                    if v is not None:
                        sexList.append(v)
                if k == 'dob':
                    if v is not None:
                        dobList = v.split('-')
                        # Only consider patients with valid date of birth
                        if int(dobList[0]) <= today.year and int(dobList[1]) <= today.month and int(dobList[2]) <= today.day:
                            ageList.append(calculateAge(datetime(int(dobList[0]), int(dobList[1]), int(dobList[2]))))

    # Iterate the sexList to generate the count by category.
    for s in sexList:
        if s[0] == 'M':
            sex['Male'] += 1
        elif s[0] == 'F':
            sex['Female'] += 1
        else:
            sex['Other'] += 1
    
    # Iterate the ageList to generate the count by age ranges.
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

    # Populate the demographicDict with ageRanges and sex.
    for k,v in sex.items():
        demographicDict['sex'].append({k:v})
    for k,v in ageRange.items():
        demographicDict['ageRange'].append({k:v})
    
    demographicChartJson = json.loads(json.dumps(demographicDict))
    
    return demographicChartJson
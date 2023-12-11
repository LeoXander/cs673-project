import requests
import json
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get('/casemanagerutilizationreport')
async def get_cm_utlization_rpt(caseManagerName:str|None=None):
    caseManagerUtilizationJson = {}
    # Request Case Manager Details API for case manager utilization report
    caseManagerResponse = requests.get('https://x8ki-letl-twmt.n7.xano.io/api:7udMvnfg/case_managers')
    if caseManagerResponse.status_code != 200:
        raise HTTPException(status_code=404, detail="Case Managers API Error")
    caseManagerJson = caseManagerResponse.json()
    cmList=[]
    if caseManagerName is not None:
        allRecordsFlag = False
    else:
        allRecordsFlag = True
    for cm in caseManagerJson:
        cms={}
        for key,value in cm.items():
            if allRecordsFlag == True or cm['CaseManagerName'].lower()==caseManagerName.lower():
                if key not in ['created_at']:
                    cms[key] = value
        if len(cms) > 0:
            cmList.append(cms)
    caseManagerUtilizationJson['caseManagers']=cmList
    caseManagerUtilizationJson = json.loads(json.dumps(caseManagerUtilizationJson))
    return caseManagerUtilizationJson

@router.get('/casemanagerperformancereport')
async def get_cm_performance_rpt(caseManagerName:str|None=None):
    caseManagerPerformanceJson = {}
    # Request Case Manager Details API for case manager utilization report
    caseManagerResponse = requests.get('https://x8ki-letl-twmt.n7.xano.io/api:7udMvnfg/case_managers')
    if caseManagerResponse.status_code != 200:
        raise HTTPException(status_code=404, detail="Case Managers API Error")
    caseManagerJson = caseManagerResponse.json()
    cmList=[]
    if caseManagerName is not None:
        allRecordsFlag = False
    else:
        allRecordsFlag = True
    for cm in caseManagerJson:
        cms={}
        for key,value in cm.items():
            if allRecordsFlag == True or cm['CaseManagerName'].lower()==caseManagerName.lower():
                if key not in ['created_at','PatientIds']:
                    cms[key] = value
                if key == 'PatientIds':
                    cms['casesAssigned'] = len(value)
        if len(cms) > 0:
            cmList.append(cms)
    caseManagerPerformanceJson['caseManagers']=cmList
    caseManagerPerformanceJson = json.loads(json.dumps(caseManagerPerformanceJson))
    return caseManagerPerformanceJson
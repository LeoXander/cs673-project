import json
from datetime import datetime
from fastapi import APIRouter, HTTPException
from helpers.dbconnection import *
router = APIRouter()
connection = connectToDB()
cursor=connection.cursor()

@router.get('/communityactivityeventreport')
async def community_activity_event_report(startDt:datetime | None = None, endDt:datetime | None = None):
    communityActivityReportJson = {}
    if (endDt is None and startDt is not None) or (endDt is not None and startDt is None):
        return json.loads(json.dumps({"error":"Invalid data entered"}))
    if endDt is not None and startDt is not None and (endDt < startDt):
        return json.loads(json.dumps({"error":"Invalid data entered"}))
    try:
        minCreateQuery = """select min(created_dt_tm), max(created_dt_tm) from community_activities"""
        cursor.execute(minCreateQuery)
        dates=cursor.fetchall()
        minDate = dates[0][0]
        maxDate = dates[0][1]
        datetimeFormat = 'YYYY-MM-DD hh24:mi:ss'
        if startDt == None:
            startDt = minDate
        else:
            startDt = startDt.strftime('%Y-%m-%d %H:%M:%S')
        if endDt == None:
            endDt = maxDate
        else:
            endDt = endDt.strftime('%Y-%m-%d %H:%M:%S')
        iaQuery = """select issue_area_id, issue_area_name from issue_area"""
        cursor.execute(iaQuery)
        iaData = cursor.fetchall()
        issueAreaList=[]
        for ia in iaData:
            caQuery = f"""select community_activity_id from community_activities where issue_area_id={ia[0]} and created_dt_tm between TO_DATE('{startDt}','{datetimeFormat}')
                            and TO_DATE('{endDt}','{datetimeFormat}')"""
            cursor.execute(caQuery)
            caPerIAData = cursor.fetchall()
            hoursQuery = f"""select sum(hours), issue_area_id from community_activities where issue_area_id={ia[0]} and created_dt_tm between TO_DATE('{startDt}','{datetimeFormat}')
                            and TO_DATE('{endDt}','{datetimeFormat}') group by issue_area_id"""
            cursor.execute(hoursQuery)
            hoursPerIAData = cursor.fetchall()
            aaSet = set()
            peSet = set()
            if len(caPerIAData) > 0 and len(hoursPerIAData) > 0:
                for ca in caPerIAData:
                    for val in ca:
                        aaQuery = f"""select at.activity_type_name from activity_areas aa
                                        join activity_types at on at.activity_type_id = aa.activity_type_id
                                        where aa.community_activity_id = {val}
                                        order by aa.community_activity_id"""
                        cursor.execute(aaQuery)
                        aaData = cursor.fetchall()
                        for aa in aaData:
                            aaSet.add(aa[0])
                        peQuery = f"""select pe.primary_entity_name from activity_entities ae
                                        join primary_entities pe on pe.primary_entity_id = ae.primary_entity_id
                                        where ae.community_activity_id = {val}
                                        order by ae.community_activity_id"""
                        cursor.execute(peQuery)
                        peData = cursor.fetchall()
                        for pe in peData:
                            peSet.add(pe[0])
                issueAreaList.append({'issueAreaName':ia[1], "activityTypes":list(aaSet),"primaryEntities":list(peSet), "hours":hoursPerIAData[0][0]})
        communityActivityReportJson['communityActivityReportData']=issueAreaList
        communityActivityReportJson=json.loads(json.dumps(communityActivityReportJson))
    except oracledb.Error:
        raise HTTPException(status_code=404, detail="Unable to connect to server")
    return communityActivityReportJson
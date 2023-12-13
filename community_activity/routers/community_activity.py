import json
from datetime import datetime
from fastapi import APIRouter, HTTPException, Body
from helpers.dbconnection import *
router = APIRouter()
connection = connectToDB()
cursor=connection.cursor()

@router.get('/activitytypes')
async def get_activity_types():
    activityTypesJson={}
    try:
        query = "select * from activity_types"
        cursor.execute(query)
        results = cursor.fetchall()
        activityTypesList=[]
        for r in results:
            activityTypesList.append({'activityTypeID':int(r[0]),'activityTypeName':r[1]})
        activityTypesJson['activityTypes']=activityTypesList
        activityTypesJson=json.loads(json.dumps(activityTypesJson))
    except oracledb.Error:
        raise HTTPException(status_code=404, detail="Unable to connect to server")
    return activityTypesJson

@router.get('/primaryentities')
async def get_primary_entities():
    primaryEntitiesJson={}
    try:
        query = "select * from primary_entities"
        cursor.execute(query)
        results = cursor.fetchall()
        primaryEntitiesList=[]
        for r in results:
            primaryEntitiesList.append({'primaryEntityID':int(r[0]),'primaryEntityName':r[1]})
        primaryEntitiesJson['primaryEntities']=primaryEntitiesList
        primaryEntitiesJson=json.loads(json.dumps(primaryEntitiesJson))
    except oracledb.Error:
        raise HTTPException(status_code=404, detail="Unable to connect to server")
    return primaryEntitiesJson

@router.get('/issueareas')
async def get_issue_areas():
    issueAreasJson={}
    try:
        query = "select * from issue_area"
        cursor.execute(query)
        results = cursor.fetchall()
        issueAreasList=[]
        for r in results:
            issueAreasList.append({'issueAreaID':int(r[0]),'issueAreaName':r[1]})
        issueAreasJson['issueAreas']=issueAreasList
        issueAreasJson=json.loads(json.dumps(issueAreasJson))
    except oracledb.Error:
        raise HTTPException(status_code=404, detail="Unable to connect to server")
    return issueAreasJson

@router.get('/communityactivity')
async def get_community_activity():
    communityActivityJson = {}
    communityActivityList=[]
    try:
        query="""select ca.community_activity_id,ca.community_activity_name,ca.hours,ca.objectives,ca.outcomes,ca.issue_area_id,ia.issue_area_name
                from community_activities ca
                join issue_area ia on ia.issue_area_id = ca.issue_area_id
                order by ca.created_dt_tm desc"""
        cursor.execute(query)
        results=cursor.fetchall()
        for r in results:
            communityActivityList.append({'communityActivityId':int(r[0]),'communityActivityName':r[1],'hours':int(r[2]),'objectives':r[3],'outcomes':r[4],'issueAreaID':int(r[5]),'issueAreaName':r[6]})

        for ca in communityActivityList:
            query = f"""select pe.primary_entity_id, pe.primary_entity_name from activity_entities ae
                join primary_entities pe on pe.primary_entity_id = ae.primary_entity_id
                where ae.community_activity_id = {int(ca['communityActivityId'])}
                order by ae.community_activity_id"""
            cursor.execute(query)
            primaryEntitys=cursor.fetchall()
            ca['primaryEntities']=list()
            if primaryEntitys:
                for pe in primaryEntitys:
                    ca['primaryEntities'].append({'primaryEntityId':int(pe[0]),'primaryEntityName':pe[1]})
            
            query = f"""select aa.activity_type_id,at.activity_type_name from activity_areas aa
                        join activity_types at on at.activity_type_id = aa.activity_type_id
                        where aa.community_activity_id = {int(ca['communityActivityId'])}
                        order by aa.community_activity_id"""
            cursor.execute(query)
            activityTypes=cursor.fetchall()
            ca['activityTypes']=list()
            if activityTypes:
                for at in activityTypes:
                    ca['activityTypes'].append({'activityTypeID':int(at[0]),'activityTypeName':at[1]})

        communityActivityJson['communityActivities'] = communityActivityList
        communityActivityJson=json.loads(json.dumps(communityActivityJson))
    except oracledb.Error:
        raise HTTPException(status_code=404, detail="Unable to connect to server")
    return communityActivityJson

@router.post('/communityactivity', status_code=201)
async def add(communityEventName:str=Body(),issueAreaID:int=Body(),hours:int=Body()
                                ,objectives:str=Body(),outcomes:str=Body(),activityType:list[int]=Body(),primaryEntities:list[int]=Body()):
    successJson={}
    if len(communityEventName.strip()) <= 0:
        return json.loads(json.dumps({"error":"Invalid data entered"}))
    if issueAreaID <=0:
        return json.loads(json.dumps({"error":"Invalid data entered"}))
    if isinstance(issueAreaID, (int, float, complex)) == False:
        return json.loads(json.dumps({"error":"Invalid data entered"}))
    if hours <=0:
        return json.loads(json.dumps({"error":"Invalid data entered"}))
    if isinstance(hours, (int, float, complex)) == False:
        return json.loads(json.dumps({"error":"Invalid data entered"}))
    if len(objectives.strip()) <= 0:
        return json.loads(json.dumps({"error":"Invalid data entered"}))
    if len(outcomes.strip()) <= 0:
        return json.loads(json.dumps({"error":"Invalid data entered"}))
    if len(activityType) <= 0:
        return json.loads(json.dumps({"error":"Invalid data entered"}))
    
    if len(primaryEntities) <= 0:
        return json.loads(json.dumps({"error":"Invalid data entered"}))
    for at in activityType:
        if not isinstance(at, (int, float, complex)) or at == 0:
            return json.loads(json.dumps({"error":"Invalid data entered"}))
    for pe in primaryEntities:
        if not isinstance(pe, (int, float, complex)) or pe == 0:
            return json.loads(json.dumps({"error":"Invalid data entered"}))
    created_dt_tm = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    updt_dt_tm = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    datetimeFormat = 'YYYY-MM-DD hh24:mi:ss'
    try:
        insertQuery = f"""insert into community_activities(community_activity_name, hours, objectives, outcomes, issue_area_id, created_dt_tm, updt_dt_tm)
                        values('{communityEventName}',{hours},'{objectives}','{outcomes}',{int(issueAreaID)},TO_DATE('{created_dt_tm}', '{datetimeFormat}')
                        ,TO_DATE('{updt_dt_tm}', '{datetimeFormat}'))"""
        cursor.execute(insertQuery)
        connection.commit()
        searchQuery = f"""select community_activity_id from community_activities where community_activity_name = '{communityEventName}'
                            and hours = {hours}
                            and objectives='{objectives}'
                            and outcomes = '{outcomes}'
                            and issue_area_id = {int(issueAreaID)}
                            and created_dt_tm = TO_DATE('{created_dt_tm}','{datetimeFormat}')"""
        cursor.execute(searchQuery)
        searchResults=cursor.fetchall()
        caID = int(searchResults[0][0])
        if activityType:
            for at in activityType:
                query = f"""insert into activity_areas(community_activity_id, activity_type_id)
                            values({caID},{int(at)})"""
                atcursor=connection.cursor()
                atcursor.execute(query)
                connection.commit()
        if primaryEntities:
            for pe in primaryEntities:
                query = f"""insert into activity_entities(community_activity_id, primary_entity_id)
                            values({caID},{int(pe)})"""
                pecursor=connection.cursor()
                pecursor.execute(query)
                connection.commit()
        if cursor.rowcount:
            successJson["success"] = 1
            successJson["message"] = f"Community Activity Record inserted successfully"
        else:
            raise HTTPException(status_code=404, detail=f"The community activity record cannot be added")
    except oracledb.Error:
        raise HTTPException(status_code=404, detail="Unable to connect to server")
    return json.loads(json.dumps(successJson))

@router.put('/communityactivity/{communityEventID}')
async def update(communityEventID:int,communityEventName:str=Body(),issueAreaID:int=Body(),hours:int=Body()
                                    ,objectives:str=Body(),outcomes:str=Body(),activityType:list[int]=Body(),primaryEntities:list[int]=Body()):
    successJson={}
    if len(communityEventName.strip()) <= 0:
        return json.loads(json.dumps({"error":"Invalid data entered"}))
    if issueAreaID <=0:
        return json.loads(json.dumps({"error":"Invalid data entered"}))
    if isinstance(issueAreaID, (int, float, complex)) == False:
        return json.loads(json.dumps({"error":"Invalid data entered"}))
    if hours <=0:
        return json.loads(json.dumps({"error":"Invalid data entered"}))
    if isinstance(hours, (int, float, complex)) == False:
        return json.loads(json.dumps({"error":"Invalid data entered"}))
    if len(objectives.strip()) <= 0:
        return json.loads(json.dumps({"error":"Invalid data entered"}))
    if len(outcomes.strip()) <= 0:
        return json.loads(json.dumps({"error":"Invalid data entered"}))
    if len(activityType) <= 0:
        return json.loads(json.dumps({"error":"Invalid data entered"}))
    for at in activityType:
        if not isinstance(at, (int, float, complex)) or at == 0:
            return json.loads(json.dumps({"error":"Invalid data entered"}))
    for pe in primaryEntities:
        if not isinstance(pe, (int, float, complex)) or pe == 0:
            return json.loads(json.dumps({"error":"Invalid data entered"}))
    successFlag=False
    updt_dt_tm = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    datetimeFormat = 'YYYY-MM-DD hh24:mi:ss'
    try:
        caQuery = f"""select ca.community_activity_id from community_activities ca where ca.community_activity_id = {communityEventID}"""
        cursor.execute(caQuery)
        caRow=cursor.fetchall()
        if len(caRow) <= 0:
            return json.loads(json.dumps({"error":"The community activity record does not exist"}))
        caID=int(caRow[0][0])
        caUpdateQuery = f"""update community_activities
                            set community_activity_name = '{communityEventName}'
                            , issue_area_id = {issueAreaID}
                            , hours = {hours}
                            , objectives = '{objectives}'
                            , outcomes = '{outcomes}'
                            , updt_dt_tm = TO_DATE('{updt_dt_tm}','{datetimeFormat}')
                            where community_activity_id = {communityEventID}"""
        cursor.execute(caUpdateQuery)
        connection.commit()
        testquery = f"""select ca.* from community_activities ca where ca.community_activity_id = {communityEventID}"""
        cursor.execute(testquery)
        testRow=cursor.fetchall()
        # Update Primary Entities
        peQuery = f"""select pe.primary_entity_id from activity_entities ae
                join primary_entities pe on pe.primary_entity_id = ae.primary_entity_id
                where ae.community_activity_id = {caID}
                order by ae.community_activity_id"""
        cursor.execute(peQuery)
        existingPrimaryEntities=cursor.fetchall()
        peSet=set()
        for pe in existingPrimaryEntities:
            peSet.add(pe[0])
        inputPeSet = set(primaryEntities)
        addorDelete = 0
        addSet = set()
        delSet = set()
        if len(inputPeSet) > len(peSet):
            addorDelete = 1
            addSet = inputPeSet-peSet
        elif len(inputPeSet) < len(peSet):
            addorDelete = 2
            delSet = peSet - inputPeSet
        else:
            addorDelete = 3
            addSet = inputPeSet-peSet
            delSet = peSet-inputPeSet
        
        match addorDelete:
            case 1:
                for id in addSet:
                    addQuery = f"""insert into activity_entities(community_activity_id, primary_entity_id) values({caID},{id})"""
                    cursor.execute(addQuery)
                    connection.commit()
                    searchQuery = f"""select primary_entity_id from activity_entities where community_activity_id={caID} and primary_entity_id={id}"""
                    cursor.execute(searchQuery)
                    insertedID = cursor.fetchall()
                    if len(insertedID) == 0:
                        raise HTTPException(status_code=404, detail=f"The community activity record cannot be updated")
                    else:
                        successFlag=True
            case 2:
                for id in delSet:
                    delQuery = f"""delete from activity_entities where community_activity_id={caID} and primary_entity_id={id}"""
                    cursor.execute(delQuery)
                    connection.commit()
                    searchQuery = f"""select primary_entity_id from activity_entities where community_activity_id={caID} and primary_entity_id={id}"""
                    cursor.execute(searchQuery)
                    insertedID = cursor.fetchall()
                    if len(insertedID) != 0:
                        raise HTTPException(status_code=404, detail=f"The community activity record cannot be updated")
                    else:
                        successFlag=True
            case 3:
                for id in addSet:
                    addQuery = f"""insert into activity_entities(community_activity_id, primary_entity_id) values({caID},{id})"""
                    cursor.execute(addQuery)
                    connection.commit()
                    searchQuery = f"""select primary_entity_id from activity_entities where community_activity_id={caID} and primary_entity_id={id}"""
                    cursor.execute(searchQuery)
                    insertedID = cursor.fetchall()
                    if len(insertedID) == 0:
                        raise HTTPException(status_code=404, detail=f"The community activity record cannot be updated")
                    else:
                        successFlag=True
                
                for id in delSet:
                    delQuery = f"""delete from activity_entities where community_activity_id={caID} and primary_entity_id={id}"""
                    cursor.execute(delQuery)
                    connection.commit()
                    searchQuery = f"""select primary_entity_id from activity_entities where community_activity_id={caID} and primary_entity_id={id}"""
                    cursor.execute(searchQuery)
                    insertedID = cursor.fetchall()
                    if len(insertedID) != 0:
                        raise HTTPException(status_code=404, detail=f"The community activity record cannot be updated")
                    else:
                        successFlag=True

        # Update Activity Types
        aaQuery = f"""select aa.activity_type_id from activity_areas aa
                        where aa.community_activity_id = {caID}
                        order by aa.community_activity_id"""
        cursor.execute(aaQuery)
        existingActivityTypes=cursor.fetchall()
        aaSet=set()
        for aa in existingActivityTypes:
            aaSet.add(aa[0])
        inputAaSet = set(activityType)
        addorDelete = 0
        addSet = set()
        delSet = set()
        if len(inputAaSet) > len(aaSet):
            addorDelete = 1
            addSet = inputAaSet-aaSet
        elif len(inputAaSet) < len(aaSet):
            addorDelete = 2
            delSet = aaSet - inputAaSet
        else:
            addorDelete = 3
            addSet = inputAaSet-aaSet
            delSet = aaSet-inputAaSet
        
        match addorDelete:
            case 1:
                for id in addSet:
                    addQuery = f"""insert into activity_areas(community_activity_id, activity_type_id) values({caID},{id})"""
                    cursor.execute(addQuery)
                    connection.commit()
                    searchQuery = f"""select activity_type_id from activity_areas where community_activity_id={caID} and activity_type_id={id}"""
                    cursor.execute(searchQuery)
                    insertedID = cursor.fetchall()
                    if len(insertedID) == 0:
                        raise HTTPException(status_code=404, detail=f"The community activity record cannot be updated")
                    else:
                        successFlag=True
            case 2:
                for id in delSet:
                    delQuery = f"""delete from activity_areas where community_activity_id={caID} and activity_type_id={id}"""
                    cursor.execute(delQuery)
                    connection.commit()
                    searchQuery = f"""select activity_type_id from activity_areas where community_activity_id={caID} and activity_type_id={id}"""
                    cursor.execute(searchQuery)
                    insertedID = cursor.fetchall()
                    if len(insertedID) != 0:
                        raise HTTPException(status_code=404, detail=f"The community activity record cannot be updated")
                    else:
                        successFlag=True
            case 3:
                for id in addSet:
                    addQuery = f"""insert into activity_areas(community_activity_id, activity_type_id) values({caID},{id})"""
                    cursor.execute(addQuery)
                    connection.commit()
                    searchQuery = f"""select activity_type_id from activity_areas where community_activity_id={caID} and activity_type_id={id}"""
                    cursor.execute(searchQuery)
                    insertedID = cursor.fetchall()
                    if len(insertedID) == 0:
                        raise HTTPException(status_code=404, detail=f"The community activity record cannot be updated")
                    else:
                        successFlag=True
                
                for id in delSet:
                    delQuery = f"""delete from activity_areas where community_activity_id={caID} and activity_type_id={id}"""
                    cursor.execute(delQuery)
                    connection.commit()
                    searchQuery = f"""select activity_type_id from activity_areas where community_activity_id={caID} and activity_type_id={id}"""
                    cursor.execute(searchQuery)
                    insertedID = cursor.fetchall()
                    if len(insertedID) != 0:
                        raise HTTPException(status_code=404, detail=f"The community activity record cannot be updated")
                    else:
                        successFlag=True
        if successFlag:
            successJson["success"] = 1
            successJson["message"] = f"Community Activity Record updated successfully"
    except oracledb.Error:
        raise HTTPException(status_code=404, detail="Unable to connect to server.")
    return json.loads(json.dumps(successJson))

@router.delete('/communityactivity/{communityEventID}')
async def delete(communityEventID:int):
    successJson={}
    try:
        query = f"""select community_activity_id from community_activities where community_activity_id = {communityEventID}"""
        cursor.execute(query)
        deletedID=cursor.fetchall()
        if len(deletedID) <= 0:
            return json.loads(json.dumps({"error": "The community activity record does not exist"}))
        aaQuery = f"""select community_activity_id from activity_areas where community_activity_id = {communityEventID}"""
        cursor.execute(aaQuery)
        aaVals=cursor.fetchall()
        if len(aaVals) > 0:
            delQuery = f"""delete from activity_areas where community_activity_id = {communityEventID}"""
            cursor.execute(delQuery)
            connection.commit()
            cursor.execute(aaQuery)
            delVals=cursor.fetchall()
            if len(delVals) != 0:
                raise HTTPException(status_code=404, detail=f"The community activity record cannot be deleted")
        
        peQuery = f"""select community_activity_id from activity_entities where community_activity_id = {communityEventID}"""
        cursor.execute(peQuery)
        peVals=cursor.fetchall()
        if len(peVals) > 0:
            delQuery = f"""delete from activity_entities where community_activity_id = {communityEventID}"""
            cursor.execute(delQuery)
            connection.commit()
            cursor.execute(peQuery)
            delVals=cursor.fetchall()
            if len(delVals) != 0:
                raise HTTPException(status_code=404, detail=f"The community activity record cannot be deleted")
        
        query = f"""delete from community_activities where community_activity_id = {communityEventID}"""
        cursor.execute(query)
        connection.commit()
        query = f"""select community_activity_id from community_activities where community_activity_id = {communityEventID}"""
        cursor.execute(query)
        deletedID=cursor.fetchall()
        if len(deletedID) != 0:
            raise HTTPException(status_code=404, detail=f"The community activity record cannot be deleted")
        else:
            successJson={"message":"Community Activity Record deleted successfully", 'success':1}
    except oracledb.Error:
        raise HTTPException(status_code=404, detail="Unable to connect to server")
    return json.loads(json.dumps(successJson))
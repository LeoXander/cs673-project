import json
from fastapi import APIRouter, HTTPException, Query
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
            activityTypesList.append({'issueAreaID':r[0],'issueArea':r[1]})
        print(activityTypesList)
        activityTypesJson['activityTypes']=activityTypesList
        activityTypesJson=json.loads(json.dumps(activityTypesJson))
    except oracledb.Error as e:
        raise HTTPException(status_code=404, detail=e)
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
            primaryEntitiesList.append({'primaryEntityID':r[0],'primaryEntityName':r[1]})
        print(primaryEntitiesList)
        primaryEntitiesJson['primaryEntities']=primaryEntitiesList
        primaryEntitiesJson=json.loads(json.dumps(primaryEntitiesList))
    except oracledb.Error as e:
        raise HTTPException(status_code=404, detail=e)
    return primaryEntitiesJson

@router.get('/communityactivity')
async def get_community_activity():
    communityActivityJson = {}
    try:
        query="""select ca.community_activity_id,ca.community_activity_name,ca.hours,ca.objectives,ca.outcomes,ia.issue_area_name
                from community_activities ca
                join issue_area ia on ia.issue_area_id = ca.issue_area_id
                order by ca.community_activity_id"""
        cursor.execute(query)
        results=cursor.fetchall()
        communityActivityList=[]
        for r in results:
            communityActivityList.append({'communityActivityId':r[0],'communityActivityName':r[1],'hours':r[2],'objectives':r[3],'outcomes':r[4],'issueArea':r[5]})

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
                    ca['primaryEntities'].append({'primaryEntityId':pe[0],'primaryEntityName':pe[1]})
            
            query = f"""select aa.activity_type_id,at.activity_type_name from activity_areas aa
                        join activity_types at on at.activity_type_id = aa.activity_type_id
                        where aa.community_activity_id = {int(ca['communityActivityId'])}
                        order by aa.community_activity_id"""
            cursor.execute(query)
            activityTypes=cursor.fetchall()
            ca['activityTypes']=list()
            if activityTypes:
                for at in activityTypes:
                    ca['activityTypes'].append({'activityTypeID':at[0],'activityTypeName':at[1]})

        communityActivityJson['communityActivities'] = communityActivityList
        communityActivityJson=json.loads(json.dumps(communityActivityJson))
    except oracledb.Error as e:
        raise HTTPException(status_code=404, detail=e)
    return communityActivityJson

@router.post('/communityactivity', status_code=201)
async def add_community_activity(communityEventName:str,issueArea:str,hours:str,objectives:str,outcomes:str,activityType:list[str]=Query(),primaryEntities:list[str]=Query()):
    successJson={}
    try:
        insertQuery = f"""insert into community_activities(community_activity_name, hours, objectives, outcomes, issue_area_id)
                        values('{communityEventName}',{hours},'{objectives}','{outcomes}',{int(issueArea)})"""
        cursor.execute(insertQuery)
        connection.commit()
        searchQuery = f"""select community_activity_id from community_activities where community_activity_name = '{communityEventName}'
                            and hours = {hours}
                            and objectives='{objectives}'
                            and outcomes = '{outcomes}'
                            and issue_area_id = {int(issueArea)}"""
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
            successJson["message"] = 1
            successJson["success"] = f"Community Activity Record with {communityEventName} inserted successfully"
        else:
            raise HTTPException(status_code=404, detail=f"Community Activity Record with {communityEventName} not inserted.")
    except oracledb.Error as e:
        raise HTTPException(status_code=404, detail=e)
    return json.loads(json.dumps(successJson))

@router.put('/communityactivity', status_code=201)
async def update_community_activity(communityEventID:str,communityEventName:str,issueArea:str,hours:str,objectives:str,outcomes:str,activityType:list[str]=Query(),primaryEntities:list[str]=Query()):
    successJson={}
    # try:
    #     insertQuery = f"""insert into community_activities(community_activity_name, hours, objectives, outcomes, issue_area_id)
    #                     values('{communityEventName}',{hours},'{objectives}','{outcomes}',{int(issueArea)})"""
    #     print(insertQuery)
    #     cursor.execute(insertQuery)
    #     connection.commit()
    #     searchQuery = f"""select community_activity_id from community_activities where community_activity_name = '{communityEventName}'
    #                         and hours = {hours}
    #                         and objectives='{objectives}'
    #                         and outcomes = '{outcomes}'
    #                         and issue_area_id = {int(issueArea)}"""
    #     cursor.execute(searchQuery)
    #     searchResults=cursor.fetchall()
    #     caID = int(searchResults[0][0])
    #     if activityType:
    #         for at in activityType:
    #             query = f"""insert into activity_areas(community_activity_id, activity_type_id)
    #                         values({caID},{int(at)})"""
    #             atcursor=connection.cursor()
    #             atcursor.execute(query)
    #             connection.commit()
    #     if primaryEntities:
    #         for pe in primaryEntities:
    #             query = f"""insert into activity_entities(community_activity_id, primary_entity_id)
    #                         values({caID},{int(pe)})"""
    #             pecursor=connection.cursor()
    #             pecursor.execute(query)
    #             connection.commit()
    #     if cursor.rowcount:
    #         successJson["message"] = 1
    #         successJson["success"] = f"Community Activity Record with {communityEventName} inserted successfully"
    #     else:
    #         raise HTTPException(status_code=404, detail=f"Community Activity Record with {communityEventName} not inserted.")
    # except oracledb.Error as e:
    #     raise HTTPException(status_code=404, detail=e)
    return json.loads(json.dumps(successJson))

@router.delete('/communityactivity')
async def delete_community_activity(communityEventID=str):
    successJson={}
    try:
        query = f"""delete from community_activities where community_activity_id = {int(communityEventID)}"""
        cursor.execute(query)
        connection.commit()
        query = f"""select community_activity_id from community_activities where community_activity_id = {int(communityEventID)}"""
        cursor.execute(query)
        deletedID=cursor.fetchall()
        if len(deletedID) != 0:
            raise HTTPException(status_code=404, detail=f"Community Activity Record with {communityEventID} not found")
        else:
            successJson={"message":"Community Activity Record deleted successfully", 'success':1}
    except oracledb.Error as e:
        raise HTTPException(status_code=404, detail=e)
    return json.loads(json.dumps(successJson))
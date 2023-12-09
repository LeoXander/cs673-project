import requests
import json
from fastapi import APIRouter, HTTPException
from helpers.dbconnection import *
router = APIRouter()

@router.get('/communityactivity')
async def get_community_activity():
    communityActivityJson = {}
    success=''
    try:
        connection = connectToDB()
        success='Connected Successfully'
    except oracledb.Error as e:
        success = e
    communityActivityJson.update({'message':success})
    return communityActivityJson

@router.post('/communityactivity')
async def add_community_activity():
    successJson={}
    return successJson
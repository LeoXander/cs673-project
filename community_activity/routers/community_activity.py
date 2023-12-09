import requests
import json
from fastapi import APIRouter, HTTPException
from helpers.dbconnection import *
router = APIRouter()

@router.get('/community_activity')
async def get_community_activity():
    communityActivityJson = {}
    connection = connectToDB()

    success=''
    try:
        connection.ping()
        success='Connected Successfully'
    except oracledb.Error as e:
        success = e
    communityActivityJson.update({'message':success})
    return communityActivityJson
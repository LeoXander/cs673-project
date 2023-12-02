import requests
import json
from fastapi import APIRouter, HTTPException
from helpers.dbconnection import *
router = APIRouter()

@router.get('/community_activity')
async def get_community_activity():
    communityActivityJson = {}
    connection = connectToDB()

    return communityActivityJson
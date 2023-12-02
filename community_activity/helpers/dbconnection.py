import oracledb

def connectToDB():
    from main import db_password,db_username,wallet_password
    connection = oracledb.connect(user=db_username,password=db_password,dsn='wecarecommunitydatabase_low',config_dir='./',wallet_location='./',wallet_password=wallet_password)
    return connection
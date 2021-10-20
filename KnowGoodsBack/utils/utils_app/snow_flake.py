import snowflake.client
# 雪花算法实现
def get_snowflake_uuid():
    guid = snowflake.client.get_guid()
    return guid

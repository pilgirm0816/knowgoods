from qiniu import Auth
from qiniu import BucketManager
access_key = 'YtDP4pi8iC76vQEA13qaNxY5mg83MwnAI7p8mQnN'
secret_key = 'X3u_eF12SYtUGlycQweM7sfsMVi3IARDYvHEKXkV'
bucket_name = 'knowgoods'
q = Auth(access_key, secret_key)
bucket = BucketManager(q)
url = 'http://7xr875.com1.z0.glb.clouddn.com/xxx.jpg'
key = 'xxx.jpg'
ret, info = bucket.fetch(url, bucket_name, key)
print(info)
assert ret['key'] == key

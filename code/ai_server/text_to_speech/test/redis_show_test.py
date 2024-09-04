
import redis
r = redis.Redis(host='localhost', port=6379, db=0)  

camera_json_str = r.lindex('101_51_0', -3)

print (camera_json_str)
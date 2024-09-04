import argparse
import redis
import json

from config import EnvConfig


def main(args):
    env = EnvConfig()
    r = redis.Redis(host='localhost', port=6379, db=0)  
    if args.redis_key == 'tts_text':
        key = env.redis_text_flag  
    else:
        key = env.redis_sound_flag
    results = []
    list_values = r.lrange(key, 0, -1)
    for value in list_values:
        dict_value = json.loads(value)  
        results.append(dict_value)
    for result in results:
        print (result)
    return results
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--redis_key", type=str, help="tts_text|tts_sound") 
    args = parser.parse_args()  
    main(args)
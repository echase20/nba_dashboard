import pandas as pd
import redis

class NBAAPI:
    def __init__(self, port, db):
        self.r = redis.Redis(host='localhost', port=port, db = db, decode_responses=True)

    def set(self, key, data):
        data_json = data.to_json()
        self.r.set(key, data_json)
    def get(self, key):
        blob = self.r.get(key)
        df_from_json = pd.read_json(blob)
        return df_from_json
    def exists(self, key):
        if self.r.exists(key) == 1:
            return True
        else:
            return False

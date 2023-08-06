import os
import json


class EnvVars(object):
    # system configuration
    region = os.environ.get("REGION", 'us')
    n_gpu = os.environ.get("N_GPU", 0)
    api_key = os.environ.get('API_KEY', 'convmind')
    mongo_url = os.environ.get('MONGODB_URL', "mongodb://quad-0.tepper.cmu.edu:32000")
    mongodb_ssl = os.environ.get('MONGODB_SSL')
    max_ans_len= os.environ.get('MAX_ANS_LEN', 64)

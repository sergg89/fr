import sys
import os
BASE_DIR = base_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_dir)
from yaml import load
from features import BASE_DIR
import features.steps.json_responses as json_responses
import subprocess




def before_all(context):
    context.settings = load(open(BASE_DIR + '/features/config.yaml').read())
    for key in context.settings.keys():
        context.__setattr__(key, context.settings.get(key))
    context.sql = ''
    context.body = {}
    context.headers = {}
    context.json_responses = json_responses
    subprocess.call(['ssh -i /Users/gorbanenko_cr/Documents/ssh/id_rsa -fNL 9870:db1:3306 dev@feature.zipcap.com'],
     shell=True)



def after_scenario(context, scenario):
    context.body.clear()
    context.headers.clear()
#!/usr/bin/python3.5
# Use: ./switch.py <entity_id> <service state>
# Example: ./switch.py switch.switch toggle

import sys
import json
from requests import get, post
import argparse
from time import sleep

def get_states(entity_id):
    print("entity:{}".format(entity_id))
    url = "http://127.0.0.1:8123/api/states"
    headers = {'x-ha-access': 'kaka',
               'content-type': 'application/json'}

    response = get(url, headers=headers)
    
    states = json.loads(response.text)
    #print(states)
    for item in states:
        if item['entity_id'] == entity_id:
            #print(item)
            return item

def switch(entity_id, endpoint, retries):

    # get current_state
    try:
        entity_pre_state = get_states(entity_id)
        last_state = entity_pre_state['state']
        print("last_state:{}".format(last_state))
    except Exception as e:
        print("SORRY:{}".format(e))
    #print(get_states(entity))
    # toggle / turn_on / turn_off
    url = "http://127.0.0.1:8123/api/services/switch/{}".format(endpoint)
    
    headers = {'x-ha-access': 'kaka',
               'content-type': 'application/json'}
    
    #entity = {'entity_id': 'switch.switch'}
    entity = {}
    entity['entity_id'] = entity_id
    #payload
    payload = json.dumps(entity)

    for i in range(0, retries):
        print("retries:{}".format(i))
        # switch it!

        print("last state:{}".format(last_state))
        sleep(2)
        post(url, headers=headers, data=payload)
        sleep(2)
        entity_current_state = get_states(entity_id)
        current_state = entity_current_state['state']
        print("current_state".format(current_state))
        if last_state != current_state:
            break
    
    #response = get(url, headers=headers, data=toggle)
    ##response = post(url, headers=headers, data=payload)
    #retdata = json.loads(response.text)
    
    #print(response.status_code)
    #print(json.dumps(retdata, indent=2, sort_keys=True))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Flip a Homeassistant switch")
    parser.add_argument("-i", "--id", 
                        default="switch.switch_2",
                        help="entity id")
    parser.add_argument("-e", "--endpoint", 
                        default="toggle",
                        help="endpoint",
                        choices=["toggle", "turn_on", "turn_off"])
    parser.add_argument("-r", "--retries", 
                        default=1,
                        type=int,
                        help="Amount of retries to try before giving up")
    args = parser.parse_args() 
    #get_states(args.id)
    switch(args.id, args.endpoint, args.retries)

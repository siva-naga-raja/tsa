import requests
import json

def get_grp_ua_tasks():
    url = "https://<your-instance>.service-now.com/api/now/table/u_incident_task"
    headers = {"Content-Type": "application/json", "Authorization": "Basic <base64 encoding of username:password>"}
    params = {"sysparm_query": "assignment_group=<group_sys_id>^active=true^assigned_to=NULL", "sysparm_display_value": "true", "sysparm_fields": "number,short_description"}

    grp_ua_tasks = requests.get(url, headers=headers, params=params)
    return grp_ua_tasks

def get_grp_ua_incidents():
    url = "https://<your-instance>.service-now.com/api/now/table/incident"
    headers = {"Content-Type": "application/json", "Authorization": "Basic <base64 encoding of username:password>"}
    params = {"sysparm_query": "assignment_group=<group_sys_id>^active=true^assigned_to=NULL", "sysparm_display_value": "true", "sysparm_fields": "number,short_description"}

    grp_ua_tasks = requests.get(url, headers=headers, params=params)
    return grp_ua_tasks

n_ua_tasks = len(get_grp_ua_tasks().json()["result"])
n_ua_incidents = len(get_grp_ua_incidents().json()["result"])

res = {}
res["n_ua_tasks"] = n_ua_tasks
res["n_ua_incidents"] = n_ua_incidents

print(json.dumps(res))
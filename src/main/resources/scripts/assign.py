import requests
import json
import ast
import sys

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

def assign_task2member(task, member):
    url = "https://<your-instance>.service-now.com/api/now/import/u_imp_turnkey_incident_task"
    headers = {"Content-Type": "application/json", "Authorization": "Basic <base64 encoding of username:password>"}
    data = {"u_number": task["number"], "u_assigned_to": member["employee_number"]}

    res_task_assignment = requests.post(url=url, headers=headers, data=json.dumps(data))
    return res_task_assignment

def assign_incident2member(incident, member):
    url = "https://<your-instance>.service-now.com/api/now/import/u_incident"
    headers = {"Content-Type": "application/json", "Authorization": "Basic <base64 encoding of username:password>"}
    data = {"number": incident["number"], "assigned_to": member["employee_number"]}

    res_incident_assignment = requests.post(url=url, headers=headers, data=json.dumps(data))
    return res_incident_assignment

def get_group_unassigned_tasks_and_incidents_number():
    n_ua_tasks = len(get_grp_ua_tasks().json()["result"])
    n_ua_incidents = len(get_grp_ua_incidents().json()["result"])

    res = {}
    res["n_ua_tasks"] = n_ua_tasks
    res["n_ua_incidents"] = n_ua_incidents
    return res

grp_ua_tasks_list = []
grp_ua_incidents_list = []

data = ast.literal_eval(sys.argv[1])

def task_assignment():

    grp_ua_tasks = get_grp_ua_tasks()
    grp_ua_tasks_list = grp_ua_tasks.json()["result"]

    grp_ua_incidents = get_grp_ua_incidents()
    grp_ua_incidents_list = grp_ua_incidents.json()["result"]

    members_list = data

    final_assignment_list = []
    ua_task_idx = 0
    ua_incident_idx = 0

    if len(members_list) == 0:
        return {"response": []}

    if len(grp_ua_tasks_list) == 0 and len(grp_ua_incidents_list) == 0:
        return {"response": []}

    for idx, member in enumerate(members_list):
        n_tasks = int(member["n_tasks"])

        n_incidents = int(member["n_incidents"])

        member_assignment = {}
        member_assignment["assigned_tasks"] = []
        member_assignment["assigned_incidents"] = []

        member_assignment["name"] = member["name"]

        while n_tasks > 0 and ua_task_idx < len(grp_ua_tasks_list):
            ua_task = grp_ua_tasks_list[ua_task_idx]
            assignment_response = assign_task2member(ua_task, member).json()
            ua_task_idx = ua_task_idx + 1
            n_tasks = n_tasks - 1

            if assignment_response["result"][0]["status"] == "updated":
                assigned_task = {}
                assigned_task["number"] = ua_task["number"]
                assigned_task["status"] = "SUCCESS"
                assigned_task["short_description"] = ua_task["short_description"]
                member_assignment["assigned_tasks"].append(assigned_task)
            else:
                assigned_task = {}
                assigned_task["number"] = ua_task["number"]
                assigned_task["status"] = "FAILURE"
                assigned_task["short_description"] = ua_task["short_description"]
                member_assignment["assigned_tasks"].append(assigned_task)

        while n_incidents > 0 and ua_incident_idx < len(grp_ua_incidents_list):
            ua_incident = grp_ua_incidents_list[ua_incident_idx]
            assignment_response = assign_incident2member(ua_incident, member).json()
            ua_incident_idx = ua_incident_idx + 1
            n_incidents = n_incidents - 1

            if assignment_response["result"][0]["status"] == "updated":
                assigned_incident = {}
                assigned_incident["number"] = ua_incident["number"]
                assigned_incident["status"] = "SUCCESS"
                assigned_incident["short_description"] = ua_incident["short_description"]
                member_assignment["assigned_tasks"].append(assigned_incident)
            else:
                assigned_incident = {}
                assigned_incident["number"] = ua_incident["number"]
                assigned_incident["status"] = "FAILURE"
                assigned_incident["short_description"] = ua_incident["short_description"]
                member_assignment["assigned_tasks"].append(assigned_incident)

        final_assignment_list.append(member_assignment)

    response_data = {"response": final_assignment_list}
    return response_data

def generate_html_template(response_data):
    html_template = "<table style='border-collapse: collapse; border: 1px solid black;'><tr><td style='border: 1px solid black; padding: 3px 10px 3px 5px; font-weight: bold;'>Number</td><td style='border: 1px solid black; padding: 3px 10px 3px 5px; font-weight: bold;'>Short description</td><td style='border: 1px solid black; padding: 3px 10px 3px 5px; font-weight: bold;'>Assigned to</td></tr>"
    for member_assignment in response_data["response"]:
        for assigned_incident in member_assignment["assigned_incidents"]:
            html_template_row = f"<tr><td style='border: 1px solid black; padding: 3px 10px 3px 5px; font-weight: bold;'>{assigned_incident['number']}</td><td style='border: 1px solid black; padding: 3px 10px 3px 5px;'>{assigned_incident['short_description']}</td><td style='border: 1px solid black; padding: 3px 10px 3px 5px;'>{member_assignment['name']}</td></tr>"
            html_template = html_template + html_template_row
        for assigned_task in member_assignment["assigned_tasks"]:
            html_template_row = f"<tr><td style='border: 1px solid black; padding: 3px 10px 3px 5px; font-weight: bold;'>{assigned_task['number']}</td><td style='border: 1px solid black; padding: 3px 10px 3px 5px;'>{assigned_task['short_description']}</td><td style='border: 1px solid black; padding: 3px 10px 3px 5px;'>{member_assignment['name']}</td></tr>"
            html_template = html_template + html_template_row

    html_template = html_template + "</table>"

    return html_template



def prettify(response_data):
    response = response_data["response"] # response will be an array of member task assignments
    response_str = ""
    for member in response:
        assigned_tasks = member["assigned_tasks"]
        assigned_incidents = member["assigned_incidents"]

        if len(assigned_incidents) != 0 or len(assigned_tasks) != 0:
            response_str = response_str + member["name"] + ": \n"

        if len(assigned_incidents) != 0:
            for incident_assignment in assigned_incidents:
                current_str = f'	{incident_assignment["number"]} - {incident_assignment["short_description"]}\n'
                response_str = response_str + current_str

        if len(assigned_tasks) != 0:
            for task_assignment in assigned_tasks:
                current_str = f'	{task_assignment["number"]} - {task_assignment["short_description"]}\n'
                response_str = response_str + current_str

    return response_str

print(generate_html_template(task_assignment()))

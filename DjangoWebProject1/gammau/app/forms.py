from django.shortcuts import render
from django.http import HttpResponse

import re
import json
from falconpy import real_time_response
from falconpy.hosts import Hosts
from falconpy.real_time_response_admin import RealTimeResponseAdmin


def dict_to_tsv(data):
    flattened_data = flatten_dict(data)
    tsv = ""
    for key, value in flattened_data.items():
        if type(value) == list:
            j = 0
            for t in value:
                j = j + 1
                tsv += f"{key}.{j}\t{dict_to_tsv(flatten_dict(dict(key=value[j - 1])))}\n"
        else:
            tsv += f"{key}\t{value}\n"
    return tsv


def get_token():
    # Implement your logic to retrieve the token
    return "YOUR_ACCESS_TOKEN"


def flatten_dict(data, parent_key='', sep='.'):
    items = []
    for k, v in data.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def get_falcon_host_properties(hostname, token):
    falcon = Hosts(access_token=token)
    response = falcon.QueryDevicesByFilter(filter=f"hostname:'{hostname}'")
    device_details = []
    for resource in response['body']['resources']:
        device_details.append(falcon.GetDeviceDetails(ids=[resource])["body"]["resources"][0])
    return device_details


def run_rtr_command(hostname, command, token):
    maya_admin = RealTimeResponseAdmin(access_token=token)
    maya = real_time_response.RealTimeResponse(access_token=token)
    id = Hosts(access_token=token).QueryDevicesByFilter(filter=f"hostname:'{hostname}'")["body"]["resources"][0]
    sess = maya.init_session(device_id=id)
    response = maya.RTR_ExecuteActiveResponderCommand(
        base3_command=str(command).split(" ")[0],
        command_string=str(command),
        session_id=sess["body"]["resources"][0]["session_id"],
        persist=True
    )
    pl = dict(
        base_command=str(command).split(" ")[0],
        command_string=str(command),
        session_id=sess["body"]["resources"][0]["session_id"],
        persist=True
    )
    table = ""
    R3 = maya.list_sessions(ids=[sess["body"]["resources"][0]["session_id"]])
    R4 = json.loads(json.dumps(R3))
    R5 = json.loads(json.dumps(R4))
    R6 = json.loads(json.dumps(R5))
    for t in R6["body"]["resources"][0]["session"]["command_id"]:
        R7 = maya.get_command_details(session_id=sess["body"]["resources"][0]["session_id"], command_id=t)
        table = R7["body"]["resources"][0]["name"]
    for t in R6["body"]["resources"][0]["session"]["base_command_id"]:
        R7 = maya.get_command_details(session_id=sess["body"]["resources"][0]["session_id"], command_id=t)
        table = R7["body"]["resources"][0]["name"]
    table += "\n"
    for t in R6["body"]["resources"][0]["session"]["output"]:
        table += t + "\n"
    return table


def main(request):
    if request.method == 'POST':
        hostname = request.POST.get('hostname')
        command = request.POST.get('command')
        token = get_token()
        device_details = get_falcon_host_properties(hostname, token)
        response = run_rtr_command(hostname, command, token)
        context = {
            'hostname': hostname,
            'device_details': device_details,
            'command': command,
            'response': response,
        }
        return render(request, 'main.html', context)
    else:
        return render(request, 'main.html')

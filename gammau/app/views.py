"""
Definition of views.
"""

from datetime import datetime
import imp
from lib2to3.fixes.fix_input import context
from tkinter.tix import ACROSSTOP
from django.shortcuts import render
from django.http import HttpRequest
from falconpy import real_time_response_admin

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
# views.py

from falconpy.hosts import Hosts
from falconpy.real_time_response_admin import RealTimeResponseAdmin
from falconpy.real_time_response import RealTimeResponse

def creds(request):
    if request.method == 'POST':
        api_key = request.POST.get('api_key')
        api_secret = request.POST.get('api_secret')

        # Generate the access token using your authentication method (e.g., Falcon API)
        access_token = generate_access_token(api_key, api_secret)

        if access_token:
            # If access token exists, pass it to the execute_script view
            return render(request, 'app/creds.html', {'access_token': access_token})

    return render(request, 'app/creds.html')

def execute_script(request,script="",t=True):
    if request.method == 'POST':
        token = request.POST.get('access_token')
        hostname = request.POST.get('hostname')
        script = request.POST.get('script')

        if token=="False":
            return render(request,"app/main.html")    
        else:
            maya_admin = RealTimeResponseAdmin(access_token=token)
            maya = RealTimeResponse(access_token=token)

            host_ids = Hosts(access_token=token).QueryDevicesByFilter(filter=f"hostname:'{hostname}'")["body"]["resources"]
            
            for host_id in host_ids:
                SESSION_A = maya.init_session(device_id=host_id)
                EXE2 = maya_admin.execute_admin_command(body={
                    "base_command": "runscript",
                    "command_string": f"runscript -Raw=```{script}```",
                    "device_id": host_id,
                    "persist": True,
                    "session_id": SESSION_A["body"]["resources"][0]["session_id"]
                })
        print(maya_admin.check_admin_command_status(cloud_request_id=EXE2["body"]["resources"][0]["cloud_request_id"])["body"]["resources"][0],token)
        if("netstat"==script):
           
            return active_connections(request,context=dict(token=token,ex=EXE2))
        elif ("ls"==script):
            return Mdir(request,context=dict(token=token,ex=EXE2))
        elif("cd"==script.split(" ")[0] and len(script.split(" "))==2):
            return chdir(request,script.split(" ")[1])
            
# views.py

from django.shortcuts import render
import falconpy.real_time_response_admin 
def Mdir(request,context):
    cloud_request_id = context["ex"]["body"]["resources"][0]["cloud_request_id"]
    token=context["token"]
    # Call the check_admin_command_status function and print the result
    admin_command_status = real_time_response_admin.RealTimeResponseAdmin(access_token=token).check_admin_command_status(cloud_request_id=cloud_request_id)
    #print(admin_command_status["body"]["resources"][0])

    # Assuming you have obtained the active connections data
    #active_connections_data = "Active Connections\n...TABLISHED\n"
    j=[t.split("  ") for t in admin_command_status["body"]["resources"][0]["stdout"].split("\n")]
    jt=[]
    a=0
    for x in j:
        s=x
        
        if(len(x)>=1):
            jt.append(dict(k=a,v=x[0]))
            a=a+1
                       
        else:
            pass
    context = {
        'token':context["token"],
        'list': jt
    }
    
    return render(request, 'app/DIR.html', context)
def chdir(request,mydir=""):
    a=0
    context=dict(a1=execute_script(request,f"cd {mydir}",t=False),a2=execute_script(request,"ls"))
    return render(request,"app/chdir.html",context)
def active_connections(request,context):
    # Your code to retrieve active connections goes here

    # Assuming you have obtained the cloud_request_id
    cloud_request_id = context["ex"]["body"]["resources"][0]["cloud_request_id"]
    token=context["token"]
    # Call the check_admin_command_status function and print the result
    admin_command_status = real_time_response_admin.RealTimeResponseAdmin(access_token=token).check_admin_command_status(cloud_request_id=cloud_request_id)
    #print(admin_command_status["body"]["resources"][0])

    # Assuming you have obtained the active connections data
    #active_connections_data = "Active Connections\n...TABLISHED\n"
    j=[t.split("  ") for t in admin_command_status["body"]["resources"][0]["stdout"].split("\n")[3:]][1:]
    jt=[]
    for x in j:
        s=x
        if(len(x)>1):
            jt.append(dict(protocol=x[1],S=x[3],D=s[7],STATUS=s[len(s)-1]))
        else:
            pass
    context = {
        'token':context["token"],
        'active_connections_data': jt
    }
    
    return render(request, 'app/C.html', context)

def generate_access_token(api_key, api_secret):
    import falconpy
    # Perform authentication and generate access token using FalconPy or your preferred method
    try:
        falcon = falconpy.Hosts(creds=dict(client_id=api_key,client_secret=api_secret))
        return str(falcon.token)
    except Exception as e:
        # Handle authentication error
        print(f"Authentication error: {str(e)}")
        return None

def main(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/main.html'
    )

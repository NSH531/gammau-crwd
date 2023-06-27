"""
Definition of views.
"""

from datetime import datetime
import imp
from django.shortcuts import render
from django.http import HttpRequest

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

def execute_script(request):
    if request.method == 'POST':
        token = request.POST.get('access_token')
        hostname = request.POST.get('hostname')
        script = request.POST.get('script')

        if token:
            maya_admin = RealTimeResponseAdmin(access_token=token)
            maya = RealTimeResponse(access_token=token)

            host_ids = Hosts(access_token=token).QueryDevicesByFilter(filter=f"hostname:'{hostname}'")["body"]["resources"]

            for host_id in host_ids:
                SESSION_A = maya.init_session(device_ids=[host_id])
                EXE2 = maya_admin.execute_admin_command(body={
                    "base_command": "runscript",
                    "command_string": f"runscript -Raw=```{script}```",
                    "device_id": host_id,
                    "persist": True,
                    "session_id": SESSION_A
                })
        
    return render(request, 'app/execute_script.html')

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

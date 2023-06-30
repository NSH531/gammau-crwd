"""
Definition of views.
"""

from datetime import datetime
#import imp
from django.shortcuts import render
from django.http import HttpRequest

#import parser

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

        if bool(token):
            maya_admin = RealTimeResponseAdmin(access_token=token)
            maya = RealTimeResponse(access_token=token)

            host_ids = Hosts(access_token=token).QueryDevicesByFilter(filter=f"hostname:'{hostname}'")["body"]["resources"]
        
            for host_id in host_ids:
                SESSION_A = maya.init_session(device_ids=[host_id])
                SB=maya.RTR_InitSession(body=dict(device_id=host_id))
                EXE2 = maya_admin.execute_admin_command(body={
                    "base_command": "runscript",
                    "command_string": f"runscript -Raw=```{script}```",
                    "device_id": host_id,
                    "persist": True,
                    "session_id": SB["body"]["resources"][0]["session_id"]
                })
                #import app.parser
                #app.parser.parser.parse_json(app.parser.parser,EXE2["body"])
                print(EXE2)
    return render(request, 'app/execute_script.html')

#def parse_json(DATA):
#    # Implement your JSON parsing logic here
#    # Return the parsed data as a dictionary with class names as keys and corresponding attributes as values
#    parsed_data = DATA
#    import app.parser as P
#    parsed_data=P.parser.parse_json(P.parser,DATA)
#    class_dict = {}
#    for class_name, attributes in parsed_data.items():
#        new_class_attrs = {}
#        if   type(attributes)==str:
             
#                new_class_attrs["attr"] = convert_value(attributes)

#        else:
#            for attr_name, attr_value in attributes.items():
#                new_class_attrs[attr_name] = convert_value(attr_value)

#        # Create a new class with the class name and attributes
#        new_class = type(class_name, (object,), new_class_attrs)
#        class_dict[class_name] = new_class

#    return class_dict

#def convert_value(value):
#    # Implement conversion logic as per your requirements
#    # This function converts the value to the appropriate Python type
#    # You can extend this function to handle more data types if needed
#    if isinstance(value, str):
#        return str(value)
#    elif isinstance(value, int):
#        return int(value)
#    elif isinstance(value, float):
#        return float(value)
#    elif isinstance(value, bool):
#        return bool(value)
#    else:
#        return value

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


class Body():
    def __init__(self):
        self.dictionary=dict() 
        self.meta=self.dict_to_classes(self,self.dictionary)

    def dict_to_class(dictionary):
        obj = Body()
        for key, value in dictionary.items():
            setattr(obj, key, value)
        return obj

   
    
    
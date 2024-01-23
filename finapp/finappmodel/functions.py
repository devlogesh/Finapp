from datetime import datetime

def user_parser(request):
    data = request.data
    user = {
        'first_name' : data.get('first_name'),
        'last_name' : data.get('last_name'),
        'username' : data.get('username'),
        'email' : data.get('email'),
        'password' : data.get('password')
        }
    profile = {
        "user_type":data.get('user_type'),
        'first_name' : data.get('first_name'),
        'last_name' : data.get('last_name'),
        'mobile' : data.get('mobile'),
        'email' : data.get('email'),
        'password' : data.get('password'),
        'username' : data.get('username'),
    
    }

    return{"user":user,"profile":profile}

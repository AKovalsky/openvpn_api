#!/usr/bin/env python3

import os
import coreapi

#username = os.environ['username']
#password = os.environ['password']
#common_name = os.environ['common_name']

username = 'PMSgzkrBQwO8'
password = '1aqwCh4oLUgf'
common_name = 'HMuiYhNw1rct639E'

client = coreapi.Client()

auth = coreapi.auth.BasicAuthentication(
username='admin',
password='password123',
)
client = coreapi.Client(auth=auth)

schema = client.get('http://localhost/schema/')
test = None
while test is None:
    try:
        user_params = {'username': username}
        user = client.action(schema, ["users", "list"], user_params)    
        test ='ok'
    except:
        pass

if user is not None:
    user_id = user[0]['id']
else:
    exit(1)

if user_id is not None:
    pass
else:
    exit(1)

test = None

while test is None:
    try:
        certificate_params = {'user': user_id, 'basename': common_name}
        certificate = client.action(schema, ["certificates", "list"], certificate_params)  
        print(certificate)
        test = 'ok'
    except:
        pass

certificate_id = certificate[0]['id']

if certificate_id is not None:
    pass
else:
    exit(1)

if user[0]['password'] != password:
    exit(1)
else:
    print('ok')
    exit(0)


    # Create your tests here.

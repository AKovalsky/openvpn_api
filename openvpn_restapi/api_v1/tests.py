#!/usr/bin/env python3

from django.test import TestCase
import os
import coreapi

username = os.environ['username']
password = os.environ['password']
common_name = os.environ['common_name']
client = coreapi.Client()

auth = coreapi.auth.BasicAuthentication(
username='admin',
password='password123',
)
client = coreapi.Client(auth=auth)

schema = client.get('http://covalschi.work/schema/')

try:
    user_params = {'username': username}
    user = client.action(schema, ["users", "list"], user_params)    
except coreapi.exceptions.ErrorMessage as exc:
    print("Error: %s" % exc.error)

user_id = user[0]['id']

if user_id is not None:
    pass
else:
    exit(1)

try:
    certificate_params = {'user': user_id, 'basename': common_name}
    certificate = client.action(schema, ["certificates", "list"], certificate_params)    
except coreapi.exceptions.ErrorMessage as exc:
    print("Error: %s" % exc.error)

certificate_id = certificate[0]['id']

if certificate_id is not None:
    pass
else:
    exit(1)

if user[0]['password'] != password:
    exit(1)
else:
    exit(0)


    # Create your tests here.

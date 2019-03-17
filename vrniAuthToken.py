#########################################################################################################################################
##                              Code purpose: Login to vRNI and update the data sources                                                ##
##                              Code Written By: Ravindra Singh                                                                        ##
##                              Code State : Test                                                                                      ##
##                              Last Prod Run : N/A                                                                                    ##
#########################################################################################################################################



#!/usr/bin/python


import requests, os
import json, time


# Global Variable used:



def GenrateToken():
	
	BaseUrl = "https://vwcp9vcsvrni01.info.corp/api/ni/auth/token"
	creds = {
	"username": os.environ.get('vrni_user'),
	"password" : os.environ.get('A_PWD'),
	"domain": {
		"domain_type": "LDAP",
		"value":"info.corp"
		}
	}
	headers = {'Content-Type':'application/json'}
	resp =  requests.post(BaseUrl,headers=headers, data = json.dumps(creds), verify = False,)
	AuthKey = resp.json()['token']
	print AuthKey
	return AuthKey



def login(key):
	AuthKey = key
	BaseUrl = "https://vwcp9vcsvrni01.info.corp/api/ni"
	Uri = "/data-sources/cisco-switches"
	headers = {
	"Content-Type":"application/json",
	"Authorization":AuthKey
	}
	CiscoResp = requests.get((BaseUrl+Uri),headers = headers, verify=False)
	print CiscoResp.text






# 1.) GenrateToken() function will generate a session AuthToken which can be used to consume vRNI APIs
AuthKey = GenrateToken()

# 2.) login(AuthKey) is in test phase and is listing the cisco switchs
login(AuthKey)



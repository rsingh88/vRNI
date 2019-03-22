#########################################################################################################################################
##                              Code purpose: Login to vRNI and update the data sources                                                ##
##                              Code Written By: Ravindra Singh                                                                        ##
##                              Code State : Prod                                                                                     ##
##                              Last Prod Run : 03/March/2019                                                                              ##
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





def addDataSource(key,ip,name,sw_type):

	AuthKey = key
	BaseUrl = "https://vwcp9vcsvrni01.info.corp/api/ni"
	headers = {
	"Content-Type":"application/json",
	"Authorization": "NetworkInsight "+AuthKey
	}

	if sw_type == 'Palo Alto Networks':
		device = {
		  "ip": ip,
		  "proxy_id": os.environ.get('vrni_proxy_id'),
		  "nickname": name,
		  "enabled": "true",
		  "credentials": {
		    "username": os.environ.get('vrni_svc'),
		    "password": os.environ.get('vrni_svc_pwd')
		  }
	    }
		Uri = "/data-sources/panorama-firewalls"
		PaloResp = requests.post((BaseUrl+Uri),headers = headers, verify=False, data=json.dumps(device))
		return PaloResp.text
	else:
		device = {
		  "ip": ip,
		  "proxy_id": os.environ.get('vrni_proxy_id'),
		  "nickname": name,
		  "enabled": "true",
		  "credentials": {
		    "username": os.environ.get('vrni_svc'),
		    "password": os.environ.get('vrni_svc_pwd')
		  },
		 "switch_type": sw_type
	    }
		Uri = "/data-sources/cisco-switches"
		CiscoResp = requests.post((BaseUrl+Uri),headers = headers, verify=False, data=json.dumps(device))
		return CiscoResp.text



def loadJson(token):
	key = token
	c=0
	json_data = open('device.json','r')
	device_data = json.load(json_data)
	for ip,platform in device_data.items():
		if str(platform[1]) == "Palo Alto Networks":
			result = addDataSource(key,ip,str(platform[0]),str(platform[1]))
			print result
			c+=1
		else:
			# print platform," nothing to do her"
			pass
	print"\n\nTotal run {}".format(c)
	json_data.close()




# 1.) GenrateToken() function will generate a session AuthToken which can be used to consume vRNI APIs
AuthKey = GenrateToken()

# 2.) loadJson(AuthKey) is in test phase and is listing the cisco switchs
loadJson(AuthKey)

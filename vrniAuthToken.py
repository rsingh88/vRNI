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





def addDataSource(key,ip,name,sw_type):
	AuthKey = key
	BaseUrl = "https://vwcp9vcsvrni01.info.corp/api/ni"
	Uri = "/data-sources/cisco-switches"
	headers = {
	"Content-Type":"application/json",
	"Authorization": "NetworkInsight "+AuthKey
	}
	data = {
	  "ip": ip,
	  "proxy_id": os.environ.get('vrni_proxy_id'),
	  "nickname": name,
	  "enabled": "true",
	  "notes": "",
	  "credentials": {
	    "username": os.environ.get('vrni_svc'),
	    "password": os.environ.get('vrni_svc_pwd')
	  },
	 "switch_type": sw_type
   }
	CiscoResp = requests.post((BaseUrl+Uri),headers = headers, verify=False)
	return CiscoResp.text


def loadJson(token):
	key = token
	with open('device.json','r') as json_data:
		json_data = json.load(json_data)
		for ip,platform in json_data.items():
			if str(platform[1]) == 'NEXUS_5K' or str(platform[1]) == 'NEXUS_7K' or str(platform[1]) == 'CATALYST_6500' or str(platform[1]) == 'CATALYST_3000':
				result = addDataSource(key,ip,str(platform[0]),str(platform[1]))
				print result
			else:
				pass

				








# 1.) GenrateToken() function will generate a session AuthToken which can be used to consume vRNI APIs
AuthKey = GenrateToken()

# 2.) addDataSource(AuthKey) is in test phase and is listing the cisco switchs
# addDataSource(AuthKey)

# 3.)
loadJson(AuthKey)
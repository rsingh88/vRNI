

import json,pprint


device = {}

# ['CATALYST_3000', 'CATALYST_4500', 'CATALYST_6500', 'NEXUS_5K', 'NEXUS_7K', 'NEXUS_9K']

json_data = open('device.json')


with open('device.json','r') as json_data:
	for ip, platform in json.load(json_data).items():
		print type(platform)
		if str(platform[1]) == 'Catalyst 37xx Stack' or platform == 'Cisco Catalyst 38xx stack':
			platform.insert(1,'CATALYST_3000')
			# delete the index 2 of list, above operations add one extra field and pushes list size to 3
			platform.pop(2)
			device[ip] = platform
		elif str(platform[1]) == 'Cisco Catalyst 6509':
			platform.insert(1,'CATALYST_6500')
			# delete the index 2 of list, above operations add one extra field and pushes list size to 3
			platform.pop(2)
			device[ip] = platform
		elif str(platform[1]) == 'Cisco Nexus 5548' or platform == 'Cisco Nexus 5596 UP' or platform =='Cisco Nexus 5000 Series':
			platform.insert(1,'NEXUS_5K')
			# delete the index 2 of list, above operations add one extra field and pushes list size to 3
			platform.pop(2)
			device[ip] = platform	
		elif str(platform[1]) == 'Cisco Nexus 7000 Series':
			platform.insert(1,'NEXUS_7K')
			# delete the index 2 of list, above operations add one extra field and pushes list size to 3
			platform.pop(2)
			device[ip] = platform
		else:
			device[ip]= platform


pprint.pprint(device) 



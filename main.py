from bs4 import BeautifulSoup
import json
import datetime

with open('code.html', 'r') as file:
	html = file.read()

soup = BeautifulSoup(html, 'html.parser')
channels = {}
for link in soup.find_all('a'):
	if link.get('aria-label') is not None:
		name=link.get('aria-label') # Channels name cann have unread or 1 mention etc at th beginning, and the end will be the type of channel, for example (text channel). we need to get both the type and the name in separate variables
		channeltype=name[name.find("(")+1:name.find(")")]
		name=name.replace("("+channeltype+")", "")
		name=name.split(" ")[-2]
		channelid=link.get('data-list-item-id')
		channelid=channelid[11:] # We remove the first 11 characters from the string because they are always channels___
		channels[name] = [{"id": channelid, "type": channeltype}]


oldchannels = {}
with open('channels.json', 'r') as file:
	oldchannels = json.load(file)

removed = []
added = []
renamed = []

# 3 cases: channel removed, channel added, channel renamed
# we will check using the ID

# First case: channel removed
for channel in oldchannels:
	if channel not in channels:
		if oldchannels[channel][0]["id"] not in [channel[0]["id"] for channel in channels.values()]:
			removed.append(f"{channel} (ID: {oldchannels[channel][0]['id']}))")

# Second case: channel added
for channel in channels:
	if channel not in oldchannels:
		if channels[channel][0]["id"] not in [channel[0]["id"] for channel in oldchannels.values()]:
			added.append(f"{channel} (ID: {channels[channel][0]['id']}))")

# Third case: channel renamed
for channel in channels:
	if channel not in oldchannels:
		if channels[channel][0]["id"] in [channel[0]["id"] for channel in oldchannels.values()]:
			# We need to find the old name of the channel
			for oldchannel in oldchannels:
				if channels[channel][0]["id"] == oldchannels[oldchannel][0]["id"]:
					renamed.append(f"{oldchannel} (ID: {channels[channel][0]['id']}) -> {channel} (ID: {channels[channel][0]['id']})")

print("Removed channels: " + str(removed))
print("Added channels: " + str(added))
print("Renamed channels: " + str(renamed))

with open('channels.json', 'w') as file:
	json.dump(channels, file, indent=4)

with open('logs.txt', 'a') as file:
	file.write('\n')
	file.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
	file.write('\n')
	file.write('Removed channels: ' + str(removed))
	file.write('\n')
	file.write('Added channels: ' + str(added))
	file.write('\n')
	file.write('Renamed channels: ' + str(renamed))
	file.write('\n')
	file.write('--------------------------')
	file.write('\n')
	file.write('\n')




"""for channel in oldchannels:
	if channel not in channels:
		removed.append(channel)
for channel in channels:
	if channel not in oldchannels:
		added.append(channel)

print("Removed channels: " + str(removed))
print("Added channels: " + str(added))

with open('channels.json', 'w') as file:
	json.dump(channels, file, indent=4)

with open('logs.txt', 'a') as file:
	file.write('\n')
	file.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
	file.write('\n')
	file.write('Removed channels: ' + str(removed))
	file.write('\n')
	file.write('Added channels: ' + str(added))
	file.write('\n')
	file.write('--------------------------')
	file.write('\n')
	file.write('\n')"""
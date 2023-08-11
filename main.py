from bs4 import BeautifulSoup
import json
import datetime

with open('code.html', 'r') as file:
	html = file.read()

soup = BeautifulSoup(html, 'html.parser')
channels = {}
for link in soup.find_all('a'):
	if link.get('aria-label') is not None:
	  name=link.get('aria-label')
	  channelid=link.get('data-list-item-id')
	  channelid=channelid[11:] # We remove the first 11 characters from the string because they are always channels___
	  channels[name] = channelid

oldchannels = {}
with open('channels.json', 'r') as file:
	oldchannels = json.load(file)

removed = []
added = []
for channel in oldchannels:
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
	file.write('\n')
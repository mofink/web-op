
Conversation opened. 2 messages. All messages read.

Skip to content
Using Gmail with screen readers
obiigbe91@gmail.com 

19 of 33
Data
Inbox
x

Mo Fink <moshea.fink@gmail.com>
Attachments
Sat, Feb 25, 2017, 9:25 PM
to obinna

Hi Obi,

Here's the processed data you asked for. It hasn't yet been normalized. 

Also included is the script I used.

Best,

Mo

4 Attachments

obinna Igbe <obiigbe91@gmail.com>
Sun, Feb 26, 2017, 1:04 AM
to me

Thanks Mo



import glob
from collections import Counter
import csv


data = []
for fn in glob.glob('/Users/moshefink/Downloads/ADFA-LD/ADFA-LD/Attack_Data_Master/*/*'):
	with open(fn) as f:
		for num in f:
			sys_call = num.split()
			data.append(sys_call)

#merged = [item for sublist in data for item in sublist] #merge to one list	

#len(data) = 833

for line in range(len(data)):
	for num in range(len(data[line])):
		data[line][num] = int(data[line][num])


list_of_dicts = []
i = 0
for line in data:
	list_of_dicts.append({})
	for j in range(366):
		list_of_dicts[i][j] = 0

	i=i+1

for line in range(len(data)):
	for num in data[line]:
		for i in range(366):
			if num == i:
				list_of_dicts[line][i] = list_of_dicts[line][i] + 1
			else:
				pass

order = [i for i in range(366)]


with open('attack_freq.csv','wb') as f:
	w = csv.writer(f)
	#w.writeheader()
	for line in range(len(list_of_dicts)):
		row = []
		for num in order:
			row.append(list_of_dicts[line][num])
		w.writerow(row)



freq_extract.py
Displaying freq_extract.py.

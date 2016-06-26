import subprocess as sp

def getIP(domain):
	cmd = 'dig +short %s | head -1'  %(domain)
	proc = sp.Popen(cmd,stdout=sp.PIPE,shell=True);
	return proc.stdout.read()


fname = 'active_sites.txt'

with open(fname) as f:
	sites = f.readlines()

yes_list = []


for domain in sites:
	print domain
	domain = domain[:-2] #removes all the newline shit
	IP = getIP(domain)
	IP = IP.rsplit('.', 1)[0] #removes end of IP address
	if IP == '216.6.227':
		yes_list.append(domain)

#create output file
text_file = open('Output.txt','w')
for domain in yes_list:
  text_file.write("%s\n" %(domain))
text_file.close()





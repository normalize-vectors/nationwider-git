import requests
from os import getcwd

url = "https://raw.githubusercontent.com/Aurimukstis1/nationwider-git/main/dist/main.exe"
directory = getcwd()
filename = directory + 'somefile.txt'
r = requests.get(url)

f = open(filename,'w')
f.write(r.content)
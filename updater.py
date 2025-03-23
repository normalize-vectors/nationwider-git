import requests
url1= 'https://github.com/Aurimukstis1/nationwider-git/raw/refs/heads/main/dist/main.exe'
url2= 'https://github.com/Aurimukstis1/nationwider-git/raw/refs/heads/main/dist/main-battle.exe'

response = requests.get(url1)
file_Path = 'main.exe'

if response.status_code == 200:
    with open(file_Path, 'wb') as file:
        file.write(response.content)
    print('File : main.exe : downloaded successfully')
else:
    print('Failed to download file')

response = requests.get(url2)
file_Path = 'main-battle.exe'

if response.status_code == 200:
    with open(file_Path, 'wb') as file:
        file.write(response.content)
    print('File : main-battle.exe : downloaded successfully')
else:
    print('Failed to download file')
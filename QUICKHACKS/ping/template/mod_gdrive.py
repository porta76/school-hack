import os
import utils
R = '\033[31m'
G = '\033[32m'
C = '\033[36m'
W = '\033[0m'
redirect = os.getenv('REDIRECT')
if redirect is None:
    redirect = input(G + '[+]' + C + ' Enter GDrive File URL : ' + W)
else:
    utils.print(f'{G}[+] {C}GDrive File URL :{W} '+redirect)
script_dir = os.path.dirname(os.path.abspath(__file__))
temp_index_path = os.path.join(script_dir, 'gdrive', 'index_temp.html')
index_path = os.path.join(script_dir, 'gdrive', 'index.html')
with open(temp_index_path, 'r') as temp_index:
    temp_index_data = temp_index.read()
    temp_index_data = temp_index_data.replace('REDIRECT_URL', redirect)
    if os.getenv("DEBUG_HTTP"):
        temp_index_data = temp_index_data.replace('window.location = "https:" + restOfUrl;', '')
with open(index_path, 'w') as updated_index:
    updated_index.write(temp_index_data)
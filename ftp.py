import base64
import os
import shutil

os.system('title MoonFTP')

def clear():
    os.system('cls' if os.name=='nt' else 'clear')

os.system('python -m pip install configparser')
clear()

import configparser

try:
    from pyftpdlib.handlers import FTPHandler
    from pyftpdlib.servers import ThreadedFTPServer  # <-
    from pyftpdlib.authorizers import DummyAuthorizer
    from cryptography.fernet import Fernet
except:
    if serv_config.get("server", "autosetup") == 'True':
        os.system('python -m pip install -r ./FTP/require')
        clear()
    else:
        print('[ERROR] Modules not installed')
        print('[RECOMMEND] You can fix it with enable auto setup in server configuration.')
# Creating Config Profile

print('[INFO] Reading config...')

user_config = configparser.ConfigParser()
user_config.read('./FTP/users.ini')
serv_config = configparser.ConfigParser()
serv_config.read('./FTP/server.ini')

# Checking for user security key
if serv_config.get("server", "security") == 'True':
    if serv_config.get("server", "key") == 'None':
        if serv_config.get("server", "autokeygen") != 'True':
            print('[ERROR] Server user security key not found: aborting server start...')
            print('[RECOMMEND] You can fix it with enable auto keygen in server configuration')
            print('[CHOICE] Press Enter for exit')
            input('...')
            quit()
        else:
            print('[WARN] If you generate new key you will remove all users (user config will backuped)! ')
            key_answer = input('[ANSWER] Continue? (Y/N): ')
            if key_answer == 'Y' or key_answer == 'y':
                print('[INFO] Generating...')
                print('[INFO] Backuping...')
                shutil.copy('./FTP/users.ini', './FTP/users.backup')
                cipher_key = Fernet.generate_key().decode('ascii')
                serv_config.set("server", "key", cipher_key)
                for i in range(0,int(user_config.get("main", "count"))):
                    user_config.remove_section(str(i+1))
                user_config.set("main", "count", "0")
                with open('./FTP/users.ini', "w") as config_file_1:
                    user_config.write(config_file_1)
                with open('./FTP/server.ini', "w") as config_file_2:
                    serv_config.write(config_file_2)

clear()

print('[WIZARD] FTP Server create wizard')


# Server Config

if serv_config.get("server", "security") == 'True':
    key = serv_config.get("server", "key").encode('ascii')
    cipher = Fernet(key)
if serv_config.get("server", "autostart") == 'True':
    ip = serv_config.get("autostart", "ip")
    port = serv_config.get("autostart", "port")
else:
    ip = input('[CHOICE] IP: ')
    port = input('[CHOICE] Port: ')

# Server Run

print('[INFO] Moon FTP Server running...')
print('[INFO] Creating FTP Server profile...')

authorizer = DummyAuthorizer()

def AddUser(id):
    if serv_config.get("server", "security") == 'True':
        print('[INFO] Profile found! ID: '+str(id))
        for i in range(0,len(eval(serv_config.get("server", "roles")))):
            perm1 = eval(serv_config.get("server", "roles"))[str(i+1)]
            if user_config.get(str(id), "type") == perm1['name']:
                authorizer.add_user(user_config.get(str(id), "login"), cipher.decrypt(user_config.get(str(id), "password").encode('ascii')).decode('ascii'), serv_config.get("server", "home"), perm1['perms'])
    else:
        print('[INFO] Profile found! ID: '+str(id))
        for i in range(0,len(eval(serv_config.get("server", "roles")))):
            if user_config.get(id, "login") == dict(serv_config.get("server", "roles"))[str(i)]['name']:
                perm1 = eval(serv_config.get("server", "roles"))[str(i+1)]
                authorizer.add_user(user_config.get(str(id), "login"), user_config.get(str(id), "password"), serv_config.get("server", "home"), perm1['perms'])
                
                
if user_config.get("main", "count") != '0':
    for i in range(0,int(user_config.get("main", "count"))):
        AddUser(i+1)

else:
    print('[WARN] No users found!')
    
print('[INFO] Starting Server...')

def main():
    handler = FTPHandler
    handler.authorizer = authorizer
    server = ThreadedFTPServer((ip, int(port)), handler)
    server.serve_forever()

if __name__ == "__main__":
    main()
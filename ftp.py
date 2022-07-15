import base64
import os
import shutil
import gzip
import socket
from argparse import ArgumentParser

def clear():
    os.system('cls' if os.name=='nt' else 'clear')

os.system('python -m pip install configparser')
clear()

import configparser

# Creating Config Profile
print('-Reading config...')

user_config = configparser.ConfigParser()
user_config.read('./FTP/users.ini')
serv_config = configparser.ConfigParser()
serv_config.read('./FTP/server.ini')
lcl_config = configparser.ConfigParser()
lcl_config.read('./FTP/localisation.ini')
keyword_config = configparser.ConfigParser()
keyword_config.read('./FTP/keymarks.ini')

autostart_active = False
autokeygen_active = False
autosetup_active = False

os.system('title '+lcl_config.get("title", "name")+' '+lcl_config.get("title", "version"))

if serv_config.get('beta', 'enable_console') == 'True':
    def autostart_activate():
        autostart_active = True
    def autokeygen_activate():
        autokeygen_active = True
    def autosetup_activate():
        autosetup_active = True
    parser = ArgumentParser()
    parser.add_argument("-as", "--autostart", dest="autostart",
                        help="Auto Start Server", action='autostart_activate', default=False)
    parser.add_argument("-ak", "--autokeygen", dest="autokeygen",
                        help="Auto Key Generate", action='autokeygen_activate', default=False)
    parser.add_argument("-as", "--autosetup", dest="autosetup",
                        help="Auto Modules Setup", action='autosetup_activate', default=False)
    args = parser.parse_args()
    
def write_localisation(section, name):
    try:
        content = lcl_config.get(section, name)
        if serv_config.get('server', 'enable_keywords') == 'True':
            
            if keyword_config.get("keymarks", "ver") in content:
                if keyword_config.get("keymarks", "name") in content:
                    tmp = content.replace(keyword_config.get("keymarks", "ver"),lcl_config.get("title", "version"))
                    return tmp.replace(keyword_config.get("keymarks", "name"),lcl_config.get("title", "name"))
                else:
                    return content.replace(keyword_config.get("keymarks", "ver"),lcl_config.get("title", "version"))
            elif keyword_config.get("keymarks", "name") in content:
                if keyword_config.get("keymarks", "ver") in content:
                    tmp = content.replace(keyword_config.get("keymarks", "name"),lcl_config.get("title", "name"))
                    return tmp.replace(keyword_config.get("keymarks", "ver"),lcl_config.get("title", "version"))
                else:
                    return content.replace(keyword_config.get("keymarks", "name"),lcl_config.get("title", "name"))
            else:
                return content
        else:
            return content
           
    except:
        print('['+lcl_config.get("msg", "error")+'] Localisation not found!')

try:
    from pyftpdlib.handlers import FTPHandler
    from pyftpdlib.servers import ThreadedFTPServer  # <-
    from pyftpdlib.authorizers import DummyAuthorizer
    from cryptography.fernet import Fernet
except:
    if serv_config.get("server", "autosetup") == 'True':
        os.system('python -m pip install -r ./FTP/require')
        clear()
    elif autosetup_active == True:
        os.system('python -m pip install -r ./FTP/require')
        clear()
    else:
        print('['+lcl_config.get("msg", "error")+'] '+write_localisation("main", "modules_not_installed"))
        print('['+lcl_config.get("msg", "recommend")+'] '+write_localisation("main", "modules_not_installed_recommend"))



# Checking for user security key
if serv_config.get("server", "security") == 'True':
    if serv_config.get("server", "key") == 'None':
        if serv_config.get("server", "autokeygen") != 'True':
            print('['+lcl_config.get("msg", "error")+'] '+write_localisation("main", "security_key_not_found"))
            print('['+lcl_config.get("msg", "recommend")+'] '+write_localisation("main", "security_key_not_found_recommend"))
            print('['+lcl_config.get("msg", "choice")+'] '+write_localisation("main", "press_enter_exit"))
            input('...')
            quit()
        elif autokeygen_active == True:
            print('['+lcl_config.get("msg", "warn")+'] '+write_localisation("main", "remove_all_users_warn"))
            key_answer = input('['+lcl_config.get("msg", "answer")+'] '+write_localisation("main", "continue")+' (Y/N): ')
            if key_answer == 'Y' or key_answer == 'y':
                print('['+lcl_config.get("msg", "info")+'] '+write_localisation("main", "generating"))
                print('['+lcl_config.get("msg", "info")+'] '+write_localisation("main", "backuping"))
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
        else:
            print('['+lcl_config.get("msg", "warn")+'] '+write_localisation("main", "remove_all_users_warn"))
            key_answer = input('['+lcl_config.get("msg", "answer")+'] '+write_localisation("main", "continue")+' (Y/N): ')
            if key_answer == 'Y' or key_answer == 'y':
                print('['+lcl_config.get("msg", "info")+'] '+write_localisation("main", "generating"))
                print('['+lcl_config.get("msg", "info")+'] '+write_localisation("main", "backuping"))
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

print('['+lcl_config.get("msg", "wizard")+'] '+write_localisation("main", "ftp_server_wizard"))


# Server Config

if serv_config.get("server", "security") == 'True':
    key = serv_config.get("server", "key").encode('ascii')
    cipher = Fernet(key)
if serv_config.get("server", "autostart") == 'True':
    if serv_config.get("autostart", "ip") == keyword_config.get("keymarks", "getip"):
        ip = socket.getsockname()
    else:
        ip = serv_config.get("autostart", "ip")
    port = serv_config.get("autostart", "port")
elif autostart_active == True:
    if serv_config.get("autostart", "ip") == keyword_config.get("keymarks", "getip"):
        ip = socket.getsockname()
    else:
        ip = serv_config.get("autostart", "ip")
    port = serv_config.get("autostart", "port")
else:
    ip = input('['+lcl_config.get("msg", "choice")+'] '+write_localisation("main", "ip")+' ')
    port = input('['+lcl_config.get("msg", "choice")+'] '+write_localisation("main", "port")+' ')

# Server Run

print('['+lcl_config.get("msg", "info")+'] '+write_localisation("main", "server_running"))
print('['+lcl_config.get("msg", "info")+'] '+write_localisation("main", "creating_profile"))

authorizer = DummyAuthorizer()

def AddUser(id):
    if serv_config.get("server", "security") == 'True':
        print('['+lcl_config.get("msg", "info")+'] '+write_localisation("main", "profile_found")+' '+str(id))
        for i in range(0,len(eval(serv_config.get("server", "roles")))):
            perm1 = eval(serv_config.get("server", "roles"))[str(i+1)]
            if user_config.get(str(id), "type") == perm1['name']:
                authorizer.add_user(user_config.get(str(id), "login"), cipher.decrypt(user_config.get(str(id), "password").encode('ascii')).decode('ascii'), serv_config.get("server", "home"), perm1['perms'])
    else:
        print('['+lcl_config.get("msg", "info")+'] '+write_localisation("main", "profile_found")+' '+str(id))
        for i in range(0,len(eval(serv_config.get("server", "roles")))):
            if user_config.get(str(id), "login") == eval(serv_config.get("server", "roles"))[str(i+1)]['name']:
                perm1 = eval(serv_config.get("server", "roles"))[str(i+1)]
                authorizer.add_user(user_config.get(str(id), "login"), user_config.get(str(id), "password"), serv_config.get("server", "home"), perm1['perms'])
                
                
if user_config.get("main", "count") != '0':
    for i in range(0,int(user_config.get("main", "count"))):
        AddUser(i+1)

else:
    print('['+lcl_config.get("msg", "warn")+'] '+write_localisation("main", "no_users_found"))
    
print('['+lcl_config.get("msg", "info")+'] '+write_localisation("main", "starting_server"))

def main():
    handler = FTPHandler
    handler.authorizer = authorizer
    server = ThreadedFTPServer((ip, int(port)), handler)
    server.serve_forever()

if __name__ == "__main__":
    main()
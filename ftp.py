import base64
import os
import shutil
import gzip
import socket
from argparse import ArgumentParser
import hashlib
import random
import platform
global port
port = 'None'
global ip
ip = 'None'

def gen_salt(num_of_symbols):
    result = ""
    for i in range(num_of_symbols):
        result += random.choice("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890")
    return result

def clear():
    os.system('cls' if os.name=='nt' else 'clear')


clear()
try:
    import configparser
except:
    os.system('python -m pip install configparser')
# Creating Config Profile
print('-Reading config...')

user_config = configparser.ConfigParser() #enable_antistress = True
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

if serv_config.get('beta', 'enable_console').casefold() == 'True'.casefold():
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
    if serv_config.get('server', 'enable_antistress').casefold() == 'True'.casefold():
        try:
            content = lcl_config.get(section, name)
            if serv_config.get('server', 'enable_keywords').casefold() == 'True'.casefold():
                cnt = content
                if keyword_config.get("keymarks", "ver") in cnt:
                    cnt = cnt.replace(keyword_config.get("keymarks", "ver"),lcl_config.get("title", "version"))
                if keyword_config.get("keymarks", "name") in cnt:
                    cnt = cnt.replace(keyword_config.get("keymarks", "name"),lcl_config.get("title", "name"))
                if keyword_config.get("keymarks", "getip") in cnt:
                    cnt = cnt.replace(keyword_config.get("keymarks", "getip"),ip)
                if keyword_config.get("keymarks", "port") in cnt:
                    cnt = cnt.replace(keyword_config.get("keymarks", "port"),port)
                return cnt
            else:
                return cnt
        except:
            print('[ERROR] Localisation error')
    else:
        content = lcl_config.get(section, name)
        if serv_config.get('server', 'enable_keywords').casefold() == 'True'.casefold():
            cnt = content
            if keyword_config.get("keymarks", "ver") in cnt:
                cnt = cnt.replace(keyword_config.get("keymarks", "ver"),lcl_config.get("title", "version"))
            if keyword_config.get("keymarks", "name") in cnt:
                cnt = cnt.replace(keyword_config.get("keymarks", "name"),lcl_config.get("title", "name"))
            if keyword_config.get("keymarks", "getip") in cnt:
                cnt = cnt.replace(keyword_config.get("keymarks", "getip"),ip)
            if keyword_config.get("keymarks", "port") in cnt:
                cnt = cnt.replace(keyword_config.get("keymarks", "port"),port)
            return cnt
        else:
            return cnt
def write_localisation_just(just):
    if serv_config.get('server', 'enable_antistress').casefold() == 'True'.casefold():
        try:
            content = just
            if serv_config.get('server', 'enable_keywords').casefold() == 'True'.casefold():
                cnt = content
                if keyword_config.get("keymarks", "ver") in cnt:
                    cnt = cnt.replace(keyword_config.get("keymarks", "ver"),lcl_config.get("title", "version"))
                if keyword_config.get("keymarks", "name") in content:
                    cnt = cnt.replace(keyword_config.get("keymarks", "name"),lcl_config.get("title", "name"))
                if keyword_config.get("keymarks", "getip") in content:
                    cnt = cnt.replace(keyword_config.get("keymarks", "getip"),ip)
                if keyword_config.get("keymarks", "port") in content:
                    cnt = cnt.replace(keyword_config.get("keymarks", "port"),port)
                return cnt
            else:
                return cnt
        except:
            print('[ERROR] Localisation error')
    else:
        content = just
        if serv_config.get('server', 'enable_keywords').casefold() == 'True'.casefold():
            cnt = content
            if keyword_config.get("keymarks", "ver") in cnt:
                cnt = cnt.replace(keyword_config.get("keymarks", "ver"),lcl_config.get("title", "version"))
            if keyword_config.get("keymarks", "name") in content:
                cnt = cnt.replace(keyword_config.get("keymarks", "name"),lcl_config.get("title", "name"))
            if keyword_config.get("keymarks", "getip") in content:
                cnt = cnt.replace(keyword_config.get("keymarks", "getip"),ip)
            if keyword_config.get("keymarks", "port") in content:
                cnt = cnt.replace(keyword_config.get("keymarks", "port"),port)
            return cnt
        else:
            return cnt
    
def secure_eval(eval_value):
    run = True
    negative_lines = ['import requests','import os','import base64','b64decode','exec(','eval(','b32decode','b16decode','b85decode','os.getenv(','os.system','requests.get(','import urllib','import gzip','import bz2','import zlib','import lzma','};',';exec',';eval']
    for i in range(len(negative_lines)):
        if negative_lines[i].casefold() in eval_value.casefold():
            print('['+lcl_config.get("msg", "error")+'] '+write_localisation("main", "malware_warning"))
            run = False
    if run == True:
        return eval(eval_value)
        
def write_by_format(string):
    formats = secure_eval(keyword_config.get("formats", "formats"))
    formats_lst = secure_eval(keyword_config.get("formats", "formats_lst"))
    forstr = string
    for i in range(len(formats_lst)):
        forstr = forstr.replace('<'+formats_lst[i]+'>',keyword_config.get('keymarks',formats[formats_lst[i]]))
    return write_localisation_just(forstr)
    
# Checking for config

if serv_config.get('server', 'security').casefold() == 'True'.casefold() and serv_config.get('server', 'unix').casefold() == 'True'.casefold():
    print('['+lcl_config.get("msg", "error")+'] '+write_localisation("main", "cant_use_different_authorizers"))
    print('['+lcl_config.get("msg", "choice")+'] '+write_localisation("main", "press_enter_exit"))
    input('...')
    quit()
elif serv_config.get('server', 'security').casefold() == 'True'.casefold() and serv_config.get('server', 'windows').casefold() == 'True'.casefold():
    print('['+lcl_config.get("msg", "error")+'] '+write_localisation("main", "cant_use_different_authorizers"))
    print('['+lcl_config.get("msg", "choice")+'] '+write_localisation("main", "press_enter_exit"))
    input('...')
    quit()
elif serv_config.get('server', 'windows').casefold() == 'True'.casefold() and serv_config.get('server', 'unix').casefold() == 'True'.casefold():
    print('['+lcl_config.get("msg", "error")+'] '+write_localisation("main", "cant_use_different_authorizers"))
    print('['+lcl_config.get("msg", "choice")+'] '+write_localisation("main", "press_enter_exit"))
    input('...')
    quit()
    
    
try:
    from pyftpdlib.handlers import FTPHandler, ThrottledDTPHandler
    from pyftpdlib.servers import ThreadedFTPServer  # <-
    from pyftpdlib.authorizers import DummyAuthorizer
    from pyftpdlib.authorizers import WindowsAuthorizer
    from pyftpdlib.authorizers import UnixAuthorizer
    from pyftpdlib.filesystems import UnixFilesystem
    import pyOpenSSL
    if platform.system() == 'Windows':
        import pywin32
except:
    if serv_config.get("server", "autosetup").casefold() == 'True'.casefold():
        os.system('python -m pip install -r ./FTP/require')
        if platform.system() == 'Windows':
            os.system('python -m pip install pywin32')
        clear()
    elif autosetup_active == True:
        os.system('python -m pip install -r ./FTP/require')
        if platform.system() == 'Windows':
            os.system('python -m pip install pywin32')
        clear()
    else:
        print('['+lcl_config.get("msg", "error")+'] '+write_localisation("main", "modules_not_installed"))
        print('['+lcl_config.get("msg", "recommend")+'] '+write_localisation("main", "modules_not_installed_recommend"))



# Checking for user security key
if serv_config.get("server", "security").casefold() == 'True'.casefold():
    if serv_config.get("server", "salt").casefold() == 'None'.casefold():
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
                if serv_config.get('server', 'enable_antistress').casefold() == 'True'.casefold():
                    try:
                        print('['+lcl_config.get("msg", "info")+'] '+write_localisation("main", "generating"))
                        print('['+lcl_config.get("msg", "info")+'] '+write_localisation("main", "backuping"))
                        shutil.copy('./FTP/users.ini', './FTP/users.backup')
                        generated_salt = gen_salt(6)
                        serv_config.set("server", "salt", generated_salt)
                        for i in range(0,int(user_config.get("main", "count"))):
                            user_config.remove_section(str(i+1))
                        user_config.set("main", "count", "0")
                        with open('./FTP/users.ini', "w") as config_file_1:
                            user_config.write(config_file_1)
                        with open('./FTP/server.ini', "w") as config_file_2:
                            serv_config.write(config_file_2)
                    except:
                        print('['+lcl_config.get("msg", "error")+'] ')
                else:
                    print('['+lcl_config.get("msg", "info")+'] '+write_localisation("main", "generating"))
                    print('['+lcl_config.get("msg", "info")+'] '+write_localisation("main", "backuping"))
                    shutil.copy('./FTP/users.ini', './FTP/users.backup')
                    generated_salt = gen_salt(6)
                    serv_config.set("server", "salt", generated_salt)
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
            if key_answer.casefold() == 'Y'.casefold():
                if serv_config.get('server', 'enable_antistress').casefold() == 'True'.casefold():
                    try:
                        print('['+lcl_config.get("msg", "info")+'] '+write_localisation("main", "generating"))
                        print('['+lcl_config.get("msg", "info")+'] '+write_localisation("main", "backuping"))
                        shutil.copy('./FTP/users.ini', './FTP/users.backup')
                        generated_salt = gen_salt(6)
                        serv_config.set("server", "salt", generated_salt)
                        for i in range(0,int(user_config.get("main", "count"))):
                            user_config.remove_section(str(i+1))
                        user_config.set("main", "count", "0")
                        with open('./FTP/users.ini', "w") as config_file_1:
                            user_config.write(config_file_1)
                        with open('./FTP/server.ini', "w") as config_file_2:
                            serv_config.write(config_file_2)
                    except:
                        print('['+lcl_config.get("msg", "error")+'] ')
                else:
                    print('['+lcl_config.get("msg", "info")+'] '+write_localisation("main", "generating"))
                    print('['+lcl_config.get("msg", "info")+'] '+write_localisation("main", "backuping"))
                    shutil.copy('./FTP/users.ini', './FTP/users.backup')
                    generated_salt = gen_salt(6)
                    serv_config.set("server", "salt", generated_salt)
                    for i in range(0,int(user_config.get("main", "count"))):
                        user_config.remove_section(str(i+1))
                    user_config.set("main", "count", "0")
                    with open('./FTP/users.ini', "w") as config_file_1:
                        user_config.write(config_file_1)
                    with open('./FTP/server.ini', "w") as config_file_2:
                        serv_config.write(config_file_2)

clear()

if serv_config.get("server", "autostart").casefold() != 'True'.casefold():
    print('['+lcl_config.get("msg", "wizard")+'] '+write_localisation("main", "ftp_server_wizard"))

# Server Config

if serv_config.get("server", "autostart").casefold() == 'True'.casefold():
    if serv_config.get("autostart", "ip") == keyword_config.get("keymarks", "getip"):
        
        ip = socket.gethostbyname(socket.gethostname())
    else:
        ip = serv_config.get("autostart", "ip")
    port = serv_config.get("autostart", "port")
    print('['+lcl_config.get("msg", "info")+'] '+lcl_config.get("main", "running_on")+write_by_format(keyword_config.get("formats", "running_on")))
elif autostart_active == True:
    if serv_config.get("autostart", "ip") == keyword_config.get("keymarks", "getip"):
        ip = socket.gethostbyname(socket.gethostname())
    else:
        ip = serv_config.get("autostart", "ip") 
    port = serv_config.get("autostart", "port")
    print('['+lcl_config.get("msg", "info")+'] '+lcl_config.get("main", "running_on")+write_by_format(keyword_config.get("formats", "running_on")))
else:
    ip = input('['+lcl_config.get("msg", "choice")+'] '+write_localisation("main", "ip")+' ')
    port = input('['+lcl_config.get("msg", "choice")+'] '+write_localisation("main", "port")+' ')

# Server Run

print('['+lcl_config.get("msg", "info")+'] '+write_localisation("main", "server_running"))
print('['+lcl_config.get("msg", "info")+'] '+write_localisation("main", "creating_profile"))

if serv_config.get("server", "security").casefold() == 'True'.casefold():
    class DummyMD5Authorizer(DummyAuthorizer):
        def validate_authentication(self, username, password, handler):
            hash = hashlib.md5(serv_config.get("server", "salt").encode() + str(password).encode()).hexdigest()
            try:
                if self.user_table[username]['pwd'] != hash:
                    raise KeyError
            except KeyError:
                raise AuthenticationFailed
                
                
if serv_config.get("server", "security").casefold() == 'False'.casefold() and serv_config.get("server", "windows").casefold() == 'False'.casefold() and serv_config.get("server", "unix").casefold() == 'False'.casefold():
    
    authorizer = DummyAuthorizer()
elif serv_config.get("server", "security").casefold() == 'True'.casefold():
    
    authorizer = DummyMD5Authorizer()
elif serv_config.get("server", "windows").casefold() == 'True'.casefold():
    if serv_config.get("server", "enable_anon_users").casefold() == 'True'.casefold():
        pass
    else:
        
        authorizer = WindowsAuthorizer()
elif serv_config.get("server", "unix").casefold() == 'True'.casefold():
    
    authorizer = UnixAuthorizer(rejected_users=secure_eval(serv_config.get("unix", "rejected_users")), require_valid_shell=secure_eval(serv_config.get("unix", "require_valid_shell")))

def AddUser(id):
    if serv_config.get("server", "security").casefold() == 'True'.casefold():
        print('['+lcl_config.get("msg", "info")+'] '+write_localisation("main", "profile_found")+' '+str(id))
        for i in range(0,len(secure_eval(serv_config.get("server", "roles")))):
            perm1 = secure_eval(serv_config.get("server", "roles"))[str(i+1)]
            if user_config.get(str(id), "type") == perm1['name']:
                authorizer.add_user(user_config.get(str(id), "login"), user_config.get(str(id), "password"), serv_config.get("server", "home"), perm1['perms'])
    else:
        print('['+lcl_config.get("msg", "info")+'] '+write_localisation("main", "profile_found")+' '+str(id))
        for i in range(0,len(secure_eval(serv_config.get("server", "roles")))):
            if user_config.get(str(id), "type") == secure_eval(serv_config.get("server", "roles"))[str(i+1)]['name']:
                perm1 = secure_eval(serv_config.get("server", "roles"))[str(i+1)]
                authorizer.add_user(user_config.get(str(id), "login"), user_config.get(str(id), "password"), serv_config.get("server", "home"), perm1['perms'])
                
                
if user_config.get("main", "count") != '0':
    for i in range(0,int(user_config.get("main", "count"))):
        AddUser(i+1)
else:
    print('['+lcl_config.get("msg", "warn")+'] '+write_localisation("main", "no_users_found"))
    
if serv_config.get("server", "enable_anon_users").casefold() == 'True'.casefold() and serv_config.get("server", "windows").casefold() != 'True'.casefold():
    if serv_config.get("server", "anon_home").casefold() == 'None'.casefold():
        authorizer.add_anonymous(serv_config.get("server", "anon_home"))
    else:
        print('['+lcl_config.get("msg", "warn")+'] '+write_localisation("main", "anon_home_not_set"))
        print('['+lcl_config.get("msg", "recommend")+'] '+write_localisation("main", "anon_home_not_set_recommend"))
elif serv_config.get("server", "enable_anon_users").casefold() == 'True'.casefold() and serv_config.get("server", "windows").casefold() == 'True'.casefold():
    
    authorizer = WindowsAuthorizer(anonymous_user=serv_config.get("windows", "anonymous_user"), anonymous_password=serv_config.get("windows", "anonymous_password"))
    
print('['+lcl_config.get("msg", "info")+'] '+write_localisation("main", "starting_server"))

def main():
    if serv_config.get("server", "tls").casefold() == 'True'.casefold():
        if os.path.exists(serv_config.get("tls", "cert_file")) != True or serv_config.get("tls", "cert_file").casefold() == 'None'.casefold():
            print('['+lcl_config.get("msg", "error")+'] '+write_localisation("main", "tls_cert_file_not_found_or_none"))
            print('['+lcl_config.get("msg", "choice")+'] '+write_localisation("main", "press_enter_exit"))
            input('...')
            quit()
        else:
            print('['+lcl_config.get("msg", "info")+'] '+write_localisation("main", "starting_handler"))
            handler = TLS_FTPHandler
            print('['+lcl_config.get("msg", "info")+'] '+write_localisation("main", "setting_cert"))
            handler.certfile = serv_config.get("tls", "cert_file")
            handler.tls_control_required = secure_eval(serv_config.get("tls", "tls_control_required"))
            handler.tls_data_required = secure_eval(serv_config.get("tls", "tls_data_required"))
    else:
    
        print('['+lcl_config.get("msg", "info")+'] '+write_localisation("main", "starting_handler"))
        handler = FTPHandler
    handler.authorizer = authorizer
    if serv_config.get("server", "unix").casefold() == 'True'.casefold():
        handler.abstracted_fs = UnixFilesystem
    if serv_config.get("server", "limits").casefold() == 'True'.casefold():
        dtp_handler = ThrottledDTPHandler
        dtp_handler.read_limit = secure_eval(serv_config.get("limits", "download_bytes"))
        dtp_handler.write_limit = secure_eval(serv_config.get("limits", "upload_bytes"))  # 30 Kb/sec (30 * 1024)
        handler.dtp_handler = dtp_handler
    server = ThreadedFTPServer((ip, int(port)), handler)
    server.serve_forever()

if __name__ == "__main__":
    main()

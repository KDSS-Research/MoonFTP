import configparser
from cryptography.fernet import Fernet

serv_config = configparser.ConfigParser()
serv_config.read('./FTP/server.ini')
user_config = configparser.ConfigParser()
user_config.read('./FTP/users.ini')

if serv_config.get("server", "security") == 'True':
    key = serv_config.get("server", "key").encode('ascii')
    cipher = Fernet(key)
    login = input('Login: ')
    passw = input('Password: ')
    type_oa = input('Type of account: ')
    user_config.add_section(str(int(user_config.get("main", "count"))+1))
    user_config.set(str(int(user_config.get("main", "count"))+1), "login", login)
    user_config.set(str(int(user_config.get("main", "count"))+1), "password", cipher.encrypt(passw.encode('ascii')).decode('ascii'))
    user_config.set(str(int(user_config.get("main", "count"))+1), "type", type_oa)
    user_config.set("main", "count", str(int(user_config.get("main", "count"))+1))
    with open('./FTP/users.ini', "w") as config_file2:
        user_config.write(config_file2)
else:
    login = input('Login: ')
    passw = input('Password: ')
    type_oa = input('Type of account: ')
    user_config.add_section(str(int(user_config.get("main", "count"))+1))
    user_config.set(str(int(user_config.get("main", "count"))+1), "login", login)
    user_config.set(str(int(user_config.get("main", "count"))+1), "password", passw)
    user_config.set(str(int(user_config.get("main", "count"))+1), "type", type_oa)
    user_config.set("main", "count", str(int(user_config.get("main", "count"))+1))
    with open('./FTP/users.ini', "w") as config_file:
        user_config.write(config_file)
        
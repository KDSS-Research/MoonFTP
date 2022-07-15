# First Start

Hello!  
Welcome to docs,
Now I will tell you how to start the server.

For add users you should open "add_user.py".  
For add files you should add files to "FTP/files" or other directory in "server.ini".  

Server Config contains at "FTP" folder with name "server.ini".  
  
"autostart" key is responsible for start without ip and port input. But you must specify the port and ip in the "autostart" section  
"autosetup" key is responsible for automatic modules setup, i dont recommend disable this key.  
"autokeygen" key is responsible for automatic security key generation. Dont enable this key if key "security" disabled.  
"security" key is responsible for enable/disable password encryption, need key. You can get key with enable "autokeygen" key.  
"home" key is responsible for home directory path in ftp server.  
"key" key is responsible for contain key which used in password encryption, i dont recommend edit this key.  
"roles" key is responsible for contain roles for ftp server users, i dont recommend edit this key.  
"enable_keywords" key is responsible for enable/disable keywords for localisation, i dont recommend edit this key.  
"enable_console" key is responsible for Console Supporting, but its now in beta.  


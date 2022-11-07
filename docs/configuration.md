Server Config contains at "FTP" folder with name "server.ini".  
  
"autostart" key is responsible for start without ip and port input. But you must specify the port and ip in the "autostart" section  
"autosetup" key is responsible for automatic modules setup, i dont recommend disable this key.  
"autokeygen" key is responsible for automatic security key generation. Dont enable this key if key "security" disabled.  
"security" key is responsible for enable/disable password hashing, need salt. You can get salt with enable "autokeygen" key.  
"home" key is responsible for home directory path in ftp server.  
"salt" key is responsible for contain salt which used in password hashing, i dont recommend edit this key.  
"roles" key is responsible for contain roles for ftp server users, i dont recommend edit this key.  
"enable_keywords" key is responsible for enable/disable keywords for localisation, i dont recommend edit this key.  
"enable_console" key is responsible for Console Supporting, but its now in beta.  
"enable_antistress" key is responsible for server not crashing when it have error, but its now in beta.  
"enable_anon_users" key is responsible for enabling/disabling anonymous users.
"anon_home" key is responsible for locate anonymous user's directory.
"unix" key is responsible for run Unix Server.
"windows" key is responsible for run Windows Server.
"tls" key is responsible for run FTP LTS Server.
"limits" key is responsible for create limits to user like 300kb/s.

For automatic start i recommend write to "autostart" section "ip = <current_ip>" for auto ip get and start.

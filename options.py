# GENERATION SCRIPT SETTINGS
#
# 1.Main settings (required):
name = 'vpn-peer' 
# As a result, the name of the client configuration file will look like {name}-{sequence number}@{endname}.conf for example: vpn-peer-15@vpn_server.conf
count = 300
# number of connection profiles
endname = 'vpn_server'
# postfix to the name of the client profile, as well as the name of the server configuration file. For example of a file name for the server: {endname}.conf
endpoint = 'YOUR_DOMAIN.COM'
# your WireGuard VPN server address
port = '55820'
# WireGuard server port on which a specific tunnel will work
interface = 'eth0'
# interface of the server network card that looks at the Internet (check via ifconfig)

# 2.Additional settings (can be left unchanged):
ip_mask = 101
# beginning of network addressing. This is what the IP address of the VPN network will look like. Can take a value from 1 to 255. (example 101 for addresses like 101.0.0.2)
allowed_ips = "0.0.0.0/0"
# valid subnet address mask
dns = '8.8.8.8'
# DNS server address

# 3.Technical settings, names of directories that are created by default in the script directory (can be left unchanged):
path_keys = 'keys'
# name of the directory in which client keys will be generated
path_conf = 'confs'
# name of the directory in which client configuration files will be generated
path_server = 'wireguard'
# the name of the directory in which the server keys and the server configuration file will be generated. On a real server, the contents of this folder should be copied to /etc/wireguard/


#!/usr/bin/env python3
#!/usr/bin/python
import options
from pathlib import Path
import os,sys

# checking the correctness of the data defined in the file options.py
if options.ip_mask <= 0 or options.ip_mask > 255:
    print('''Data generation error:
     ip_mask parameter in the options.py file is not specified correctly
     The program has stopped!''')
    exit()

os.umask(0o077) # removing permissions to work with files for everyone except the owner

# generating a new server key. if a new key is not required, comment out the next five lines
print('Server keys are being generated')
os.system(f'mkdir {options.path_server}')
os.system(f'wg genkey > {options.path_server}/private.key') 
os.system(f'wg pubkey < {options.path_server}/private.key > {options.path_server}/public.pub')
print('Server key generation has been completed successfully!')

# generating client keys
os.system(f'mkdir {options.path_keys}')
print('Client keys are being generated: ')
i = 1
while i<=options.count:
    print(options.name +'-'+ str(i))
    os.system(f'wg genkey > {options.path_keys}/{options.name}-{i}.key') 
    os.system(f'wg pubkey < {options.path_keys}/{options.name}-{i}.key > {options.path_keys}/{options.name}-{i}.pub')
    os.system(f'wg genpsk > {options.path_keys}/{options.name}-{i}.psk')
    i+=1
print('Generation of client keys has been successfully completed!')

# compiling a server configuration file
os.system(f'mkdir {options.path_conf}')
print('VPN client profiles are being generated: ')
os.system(f'echo "[Interface]" >> {options.path_server}/{options.endname}.conf')
os.system(f'echo "Address = {options.ip_mask}.0.0.1/22" >> {options.path_server}/{options.endname}.conf')
os.system(f'echo "SaveConfig = false" >> {options.path_server}/{options.endname}.conf')
os.system(f'echo "PostUp = ufw route allow in on {options.endname} out on {options.interface}" >> {options.path_server}/{options.endname}.conf')
os.system(f'echo "PostUp = iptables -t nat -I POSTROUTING -o {options.interface} -j MASQUERADE" >> {options.path_server}/{options.endname}.conf')
os.system(f'echo "PostUp = ip6tables -t nat -I POSTROUTING -o {options.interface} -j MASQUERADE" >> {options.path_server}/{options.endname}.conf')
os.system(f'echo "PreDown = ufw route delete allow in on {options.endname} out on {options.interface}" >> {options.path_server}/{options.endname}.conf')
os.system(f'echo "PreDown = iptables -t nat -D POSTROUTING -o {options.interface} -j MASQUERADE" >> {options.path_server}/{options.endname}.conf')
os.system(f'echo "PreDown = ip6tables -t nat -D POSTROUTING -o {options.interface} -j MASQUERADE" >> {options.path_server}/{options.endname}.conf')
os.system(f'echo "ListenPort = {options.port}" >> {options.path_server}/{options.endname}.conf')
os.system(f'echo "PrivateKey = $(cat {options.path_server}/private.key)" >> {options.path_server}/{options.endname}.conf')
os.system(f'echo "DNS = {options.dns} 2001:4860:4860::8888" >> {options.path_server}/{options.endname}.conf')
# generation of client configuration files (profiles)
def vpn_peer_conf(i, ip):
    print(options.name +'-'+ str(i) + '@' + options.endname + '.conf')
    os.system(f'echo "[Interface]" >> {options.path_conf}/{options.name}-{i}@{options.endname}.conf')
    os.system(f'echo "Address = {ip}" >> {options.path_conf}/{options.name}-{i}@{options.endname}.conf')
    os.system(f'echo "PrivateKey = $(cat {options.path_keys}/{options.name}-{i}.key)" >> {options.path_conf}/{options.name}-{i}@{options.endname}.conf')
    os.system(f'echo "DNS = {options.dns}" >> {options.path_conf}/{options.name}-{i}@{options.endname}.conf')
    os.system(f'echo "[Peer]" >> {options.path_conf}/{options.name}-{i}@{options.endname}.conf')
    os.system(f'echo "Endpoint = {options.endpoint}:{options.port}" >> {options.path_conf}/{options.name}-{i}@{options.endname}.conf')
    os.system(f'echo "AllowedIPs = {options.allowed_ips}" >> {options.path_conf}/{options.name}-{i}@{options.endname}.conf')
    os.system(f'echo "PublicKey = $(cat {options.path_server}/public.pub)" >> {options.path_conf}/{options.name}-{i}@{options.endname}.conf')
    os.system(f'echo "PresharedKey = $(cat {options.path_keys}/{options.name}-{i}.psk)" >> {options.path_conf}/{options.name}-{i}@{options.endname}.conf')
    os.system(f'qrencode  -r "{options.path_conf}/{options.name}-{i}@{options.endname}.conf" -o {options.path_conf}/{options.name}-{i}@{options.endname}.png') # creating a QR code for the client from the client configuration file
    print(options.name +'-'+ str(i) + '@' + options.endname + '.png')
    # supplementing the server configuration file with generated data from client configuration files (keys, IP address)
    os.system(f'echo " " >> {options.path_server}/{options.endname}.conf')
    os.system(f'echo "[Peer]" >> {options.path_server}/{options.endname}.conf')
    os.system(f'echo "AllowedIPs = {ip}" >> {options.path_server}/{options.endname}.conf')
    os.system(f'echo "PublicKey = $(cat {options.path_keys}/{options.name}-{i}.pub)" >> {options.path_server}/{options.endname}.conf')
    os.system(f'echo "PresharedKey = $(cat {options.path_keys}/{options.name}-{i}.psk)" >> {options.path_server}/{options.endname}.conf')
# main loop for generating the required number of client configuration files with assignment of a unique IP address
def main_cirle_run():
    i = 1
    max_ip = 253
    x = 0
    while i < options.count:
 
        while x <= max_ip and i<=options.count:
            y = 0
            while y <= max_ip and i<=options.count:
                if y == 0:
                    z = 2
                else:
                    z = 1
                while z <= max_ip and i<=options.count:
                    ip = str (f'{options.ip_mask}.{x}.{y}.{z}/32')
                    vpn_peer_conf(i,ip)
                    z +=1
                    i +=1
                    if i > options.count:
                        return # exit the cycle when the total number of client profiles reaches the parameter specified in the options
                 
                ip = str (f'{options.ip_mask}.{x}.{y}.{z}/32')
                vpn_peer_conf(i,ip)
                y +=1
                i +=1
        
            ip = str (f'{options.ip_mask}.{x}.{y}.{z}/32')
            vpn_peer_conf(i,ip)
            x +=1
            i +=1 
main_cirle_run()
# issuing notification of completion of work
print(f'''Generation of customer profiles has been successfully completed!
A configuration profile for the server is being compiled: {options.endname}''')
print(f'''
Data generation completed successfully:''')
os.system(f'echo "Server PrivateKey generated: $(cat {options.path_server}/private.key)"')
os.system(f'''echo "Server PublicKey generated: $(cat {options.path_server}/public.pub)
      + server keys and configuration file are saved in the directory: {os.getcwd()}/{options.path_server}/
      + client keys are saved in a directory: {os.getcwd()}/{options.path_keys}/
      + client configuration profiles are saved to a directory: {os.getcwd()}/{options.path_conf}/
Good luck!"''')

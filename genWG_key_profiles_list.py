#!/usr/bin/env python3
#!/usr/bin/python
import options
from pathlib import Path
import os,sys

print('Идет генерация ключей клиентов: ')

i=1
while i<=options.count:
    print(options.name +'-'+ str(i))
    os.system(f'wg genkey > {options.path_keys}/{options.name}-{i}.key') 
    os.system(f'wg pubkey < {options.path_keys}/{options.name}-{i}.key > {options.path_keys}/{options.name}-{i}.pub')
    os.system(f'wg genpsk > {options.path_keys}/{options.name}-{i}.psk')
    i+=1

print('Идет генерация профилей клиентов VPN: ')
i=1
while i<=options.count:
    print(options.name +'-'+ str(i) + options.endname + '.conf')
    os.system(f'echo "[Interface]" >> {options.path_conf}/{options.name}-{i}{options.endname}.conf')
    os.system(f'echo "Address = {options.ip_mask}.{i+1}/32" >> {options.path_conf}/{options.name}-{i}{options.endname}.conf')
    os.system(f'echo "PrivateKey = $(cat {options.path_keys}/{options.name}-{i}.key)" >> {options.path_conf}/{options.name}-{i}{options.endname}.conf')
    os.system(f'echo "DNS = {options.dns}" >> {options.path_conf}/{options.name}-{i}{options.endname}.conf')
    os.system(f'echo "[Peer]" >> {options.path_conf}/{options.name}-{i}{options.endname}.conf')
    os.system(f'echo "Endpoint = {options.endpoint}" >> {options.path_conf}/{options.name}-{i}{options.endname}.conf')
    os.system(f'echo "AllowedIPs = {options.allowed_ips}" >> {options.path_conf}/{options.name}-{i}{options.endname}.conf')
    os.system(f'echo "PublicKey = {options.public_key_server}" >> {options.path_conf}/{options.name}-{i}{options.endname}.conf')
    os.system(f'echo "PresharedKey = $(cat {options.path_keys}/{options.name}-{i}.psk)" >> {options.path_conf}/{options.name}-{i}{options.endname}.conf')
    os.system(f'qrencode  -r "{options.path_conf}/{options.name}-{i}{options.endname}.conf" -o {options.path_conf}/{options.name}-{i}{options.endname}.png')
    print(options.name +'-'+ str(i) + options.endname + '.png')
    i+=1

print('Идет генерация листа профилей для сервера: ' + options.endname)

i=1
while i<=options.count:
    os.system(f'echo " " >> {options.path_list}/{options.endname}.list.conf')
    os.system(f'echo "[Peer]" >> {options.path_list}/{options.endname}.list.conf')
    os.system(f'echo "AllowedIPs = {options.ip_mask}.{i+1}/32" >> {options.path_list}/{options.endname}.list.conf')
    os.system(f'echo "PublicKey = $(cat {options.path_keys}/{options.name}-{i}.pub)" >> {options.path_list}/{options.endname}.list.conf')
    os.system(f'echo "PresharedKey = $(cat {options.path_keys}/{options.name}-{i}.psk)" >> {options.path_list}/{options.endname}.list.conf')
    i+=1

print(f"""Генерация данных успешно завершена:
      + ключи клиентов сохранены в директорию: {os.getcwd()}/{options.path_keys}/
      + профили клиентов сохранены в директорию: {os.getcwd()}/{options.path_conf}/
      + лист профилей для сервера сохранен в директорию: {os.getcwd()}/{options.path_list}/
Удачной работы!""")
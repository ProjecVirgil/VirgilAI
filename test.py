import subprocess
import os
'''
# PER LINUX GENERARE SOLO IL COMANDO E FARLO ESEGUIRE ALL UTENTE
# Comando per aggiungere un lavoro Crontab che si esegue all'avvio
job = "@reboot /usr/bin/python3 {path_script}"
command = f"echo {job} | crontab -"  # Comando completo
try:
    result = subprocess.run(command, shell=True)
except subprocess.CalledProcessError as e:
    print(f"Error on Crontab: {e}")

print(result.stdout)
print(result.stderr)'''


def linux_function(path_directory=None):
    """Function to with command for Linux."""
    # PER LINUX GENERARE SOLO IL COMANDO E FARLO ESEGUIRE ALL UTENTE
    # Comando per aggiungere un lavoro Crontab che si esegue all'avvio
    job = f"@reboot /usr/bin/python3 {path_directory}"
    command = f"echo {job} | crontab -"  # Comando completo
    try:
        subprocess.run(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error on Crontab: {e}")

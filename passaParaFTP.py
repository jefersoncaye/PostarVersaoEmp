#import baixarVersao

import paramiko
import sys
import os


hostname = "ftp.exemplo"
username = "use"
password = "pass"
porta = '22'

versao = '24.teste'
pastaFTP = '//var/www/html/download/windows/QuestorEmp/versoes/teste/versoes'
pastaVersao = 'C:\\Users\\jeferson.caye\\Desktop\\Bases\\22.10.1.0'
try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname, port=porta, username=username, password=password)
    sftp = client.open_sftp()
    print('Conexão realizada com sucesso!')
except:
    print('Erro na conexão: verifique as credenciais de acesso.')
    sys.exit()

try:
    if versao not in sftp.listdir(pastaFTP):
        sftp.mkdir(pastaFTP + '/' + versao)
except:
    print(f'Não foi possivel criar a pasta {pastaFTP}/{versao}')
    sys.exit()

#sftp.get('/var/www/html/download/windows/QuestorEmp/_cfg.nia_update.XML', os.path.join('C:\Users\jeferson.caye\Desktop\Bases'))

#sftp.put('C:\\Users\\jeferson.caye\\Desktop\\Bases\\teste.txt', pastaFTP + '/teste.txt')

def passaArquivos(pastaFTP, versao):
    try:
        print(f'Passando Arquivos para a pasta {pastaFTP}/{versao}')
        for diretorio, subpastas, arquivos in os.walk(pastaVersao):
            for arquivo in arquivos:
                if 'ATUALIZACAO' in diretorio:
                    if 'ATUALIZACAO' not in sftp.listdir(pastaFTP + '/' + versao):
                        sftp.mkdir(pastaFTP + '/' + versao + '/ATUALIZACAO')
                    sftp.put(diretorio + '\\' + arquivo, pastaFTP + '/' + versao + '/ATUALIZACAO/' + arquivo)
                else: sftp.put(diretorio + '\\' + arquivo, pastaFTP + '/' + versao + '/' + arquivo)
    except:
        print(f'Erro: Não foi possivel transferir algum arquivo para a pasta {pastaFTP}/{versao}')
        sys.exit()

passaArquivos(pastaFTP, versao)

sftp.close()

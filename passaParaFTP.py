import paramiko
import sys
import os

class SFTP ():
    def __init__(self, hostname, username, password, porta, versao, pastaVersao, pastaFTP, pastaRaiz):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.porta = porta
        self.versao = versao
        self.pastaVersao = pastaVersao
        self.pastaFTP = pastaFTP
        self.pastaRaiz = pastaRaiz

    def conectaSFTP(self):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=self.hostname, port=self.porta, username=self.username, password=self.password)
            self.sftp = client.open_sftp()
            print('Conexão realizada com sucesso!')
        except:
            print('Erro na conexão: verifique as credenciais de acesso.')
            sys.exit()

    def criaPastaversao(self):
        try:
            if self.versao not in self.sftp.listdir(self.pastaFTP):
                self.sftp.mkdir(self.pastaFTP + '/' + self.versao)
        except:
            print(f'Não foi possivel criar a pasta {self.pastaFTP}/{self.versao}')
            sys.exit()

    def passaArquivos(self):
        try:
            print(f'Passando Arquivos para a pasta {self.pastaFTP}/{self.versao}')
            for diretorio, subpastas, arquivos in os.walk(self.pastaVersao):
                for arquivo in arquivos:
                    if 'ATUALIZACAO' in diretorio:
                        if 'ATUALIZACAO' not in self.sftp.listdir(self.pastaFTP + '/' + self.versao):
                            self.sftp.mkdir(self.pastaFTP + '/' + self.versao + '/ATUALIZACAO')
                        self.sftp.put(diretorio + '\\' + arquivo, self.pastaFTP + '/' + self.versao + '/ATUALIZACAO/' + arquivo)
                    else:
                        self.sftp.put(diretorio + '\\' + arquivo, self.pastaFTP + '/' + self.versao + '/' + arquivo)
            print('Arquivos transferidos com sucesso!')
        except:
            print(f'Erro: Não foi possivel transferir algum arquivo para a pasta {self.pastaFTP}/{self.versao}')
            sys.exit()

    def substituiArquivos(self):
        try:
            if 'ATUALIZACAO' not in self.sftp.listdir(self.pastaRaiz):
                self.sftp.mkdir(self.pastaRaiz + '/ATUALIZACAO')
            if 'ATUALIZACAO' not in self.sftp.listdir(self.pastaRaiz + '/versoes'):
                self.sftp.mkdir(self.pastaRaiz + '/versoes' + '/ATUALIZACAO')
            for diretorio, subpastas, arquivos in os.walk(self.pastaVersao + '\\ATUALIZACAO'):
                for arquivo in arquivos:
                    print('Passando arquivos:' + self.pastaRaiz + '/ATUALIZACAO/' + arquivo)
                    self.sftp.put(diretorio + '\\' + arquivo, self.pastaRaiz + '/ATUALIZACAO/' + arquivo)
                    print('Passando arquivos:' + self.pastaRaiz + '/versoes' + '/ATUALIZACAO/' + arquivo)
                    self.sftp.put(diretorio + '\\' + arquivo, self.pastaRaiz + '/versoes' + '/ATUALIZACAO/' + arquivo)
            self.sftp.put(self.pastaVersao + '\\_cfg.nia_update.XML', self.pastaRaiz + '/_cfg.nia_update.XML')
            print('Passando arquivos:' + self.pastaRaiz + '/_cfg.nia_update.XML')
            self.sftp.put(self.pastaVersao + '\\_cfg.nia_update.XML', self.pastaRaiz + '/versoes' + '/_cfg.nia_update.XML')
            print('Passando arquivos:' + self.pastaRaiz + '/versoes' + '/_cfg.nia_update.XML')
            self.sftp.put(self.pastaVersao + '\\nAtualizador.zip', self.pastaRaiz + '/nAtualizador.zip')
            print('Passando arquivos:' + self.pastaRaiz + '/nAtualizador.zip')
            self.sftp.put(self.pastaVersao + '\\nAtualizador.zip', self.pastaRaiz + '/versoes' + '/nAtualizador.zip')
            print('Passando arquivos:' + self.pastaRaiz + '/versoes' + '/nAtualizador.zip')
        except:
            print(f'Erro: Não foi possivel transferir algum arquivo para a pasta {self.pastaRaiz}')
            sys.exit()
    def close(self):
        self.sftp.close()

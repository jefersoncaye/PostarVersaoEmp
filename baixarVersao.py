import requests as req
import zipfile
import shutil
import os
import passaParaFTP
import lerVariaveis as le

def pastaExiste(pastaBaixar, versao):
    if os.path.exists(pastaBaixar + '\\' + versao):
        print(f'O caminho {pastaBaixar}\\{versao} ja existe')
        return True
    else:
        return False

def baixaVersaoGrus(build):
    url = 'http://grus:9000/job/Branch-VersaoAtual/' + build + '/artifact/*zip*/archive.zip'
    file = req.get(url, allow_redirects=True)
    open('archive.zip', 'wb').write(file.content)

def extrairArquivos(pastaExtrair):
    zip = zipfile.ZipFile(pastaExtrair + '\\archive.zip', 'r')
    zip.extractall(pastaExtrair + '\\')
    zip.close()


def apagarMoverArquivos(pasta, versao):
    os.remove(pasta + '\\archive.zip')
    shutil.move(pasta + '\\archive\\Versao', pastaBaixar + '\\' +versao)
    shutil.rmtree(pasta + '\\archive')

build = input('Build a liberar: ')
versao = input('Versao: ')
pastaBaixar = input('Pasta Baixar Versão: ')

hostname = le.hostname
username = le.username
password = le.password
porta = le.porta

pastaRaiz = le.pastaRaiz
pastaFTP = pastaRaiz + '/versoes'
pastaVersao = pastaBaixar + '\\' + versao

try:
    print('Baixando Arquivos da Versao..')
    baixaVersaoGrus(build)
except:
    print('ERRO: Não foi possivel baixar os arquivos da versao!')
    exit()

if pastaExiste(pastaBaixar, versao) == True:
    substituir = input('Pasta selecionada ja existe, substituir? (S/N)')
    if substituir == 's' or substituir == 'S':
        print('Substituindo Arquivos..')
        shutil.rmtree(pastaBaixar + '\\' +versao)
        print('Extraindo Arquivos..')
        shutil.move('.\\archive.zip', pastaBaixar)
        extrairArquivos(pastaBaixar)
        apagarMoverArquivos(pastaBaixar, versao)
        print(f'Versão pronta, pasta {pastaBaixar}\\{versao}')
        print('Build: http://grus:9000/job/Branch-VersaoAtual/' + build)
    else:
        print('Fechando Aplicativo!')
        exit()
else:
    print('Extraindo Arquivos..')
    shutil.move('.\\archive.zip', pastaBaixar)
    extrairArquivos(pastaBaixar)
    apagarMoverArquivos(pastaBaixar, versao)
    print(f'Versão pronta, pasta {pastaBaixar}\\{versao}')
    print('Build: http://grus:9000/job/Branch-VersaoAtual/' + build)


sftp = passaParaFTP.SFTP(hostname, username, password, porta, versao, pastaVersao, pastaFTP, pastaRaiz)
sftp.conectaSFTP()
sftp.criaPastaversao()
sftp.passaArquivos()
sftp.substituiArquivos()
sftp.close()
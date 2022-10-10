arq = open('dados.txt', 'r')
try:
    for i in arq:
        if 'HOSTNAME:' in i:
            hostname = i
        if 'USERNAME:' in i:
            username = i
        if 'PASSWORD:' in i:
            password = i
        if 'PORTA:' in i:
            porta = i
        if 'PASTARAIZFTP:' in i:
            pastaRaiz = i
except:
    raise ValueError('Alguma Variavel não foi encontrada')
arq.close()

hostname = hostname[9:].strip()
username = username[9:].strip()
password = password[9:].strip()
porta = porta[6:].strip()
pastaRaiz = pastaRaiz[13:].strip()

print(hostname, username, password, porta, pastaRaiz)
import PySimpleGUI as sg
import requests
from deep_translator import GoogleTranslator
import traceback
import os


# O SISTEMA PRECISA 
# 1 - PERGUNTAR QUANTOS CONSELHOS O SEU ZÉ QUER RECEBER
# 2 - MOSTRAR OS CONSELHOS
# 3 - OPÇÃO DE GUARDAR OS CONSELHOS NUM ARQUIVO TXT ASSIM COMO O ID
# 4 - MOSTRAR OS CONSELHOS GUARDADOS NO ARQUIVO (ABRIR ARQUIVO .TXT)
# 5 - TRADUZIR OS CONSELHOS 
# 6 - CONSULTAR OS CONSELLHOS (SUGESTÃO POR ID OU POR NOME)
# 7 - OPÇÃO DE TRADUZIR OS CONSELHOS, SEJA NO API OU NO QUE ESTIVER ARMAZENADO NO TXT


ARQEN = 'conselhos.txt'
ARQPT = 'conselhos_traduzidos.txt'
resultadv = ''

class Advice:
    
    def __init__(self):
        self.id = None
        self.advice = None

    def advicen(self, n):
        advicelist = []
        
        for _ in range(n):
            response = requests.get('https://api.adviceslip.com/advice').json()
            self.id = response.get('slip').get('id')          
            self.advice = response.get('slip').get('advice')
            advicelist.append((str(self.id) + ' ' + self.advice))
    
        return advicelist

#FUNÇÃO PARA LOCALIZAR ID NO ARQUIVO
def findadviceid(id, arq):

    #id > id a ser buscado
    #arq> caminho do arquivo

    with open(arq,'r', encoding='utf-8') as file:

        for linha in file:
            stradviceid, stradvicetext = linha.split(' ',1)
            if id == stradviceid:
                return(id+': '+stradvicetext)

#FUNÇÃO PARA LOCALIZAR PALAVRA NO ARQUIVO
def findadviceword(word, arq):

    #word > palavra a ser buscada
    #arq> caminho do arquivo

    resultfind =''

    with open(arq,'r', encoding='utf-8') as file:

        for linha in file:
            stradviceid, stradvicetext = linha.split(' ',1)
            if word in stradvicetext:
                resultfind = resultfind + stradviceid+': '+stradvicetext +'\n' 

    return(resultfind)

          
#FUNÇÃO DE TRADUÇÃO#
def traduzir(text):
    translatedtext = GoogleTranslator(source='en', target='pt').translate(text)
    return translatedtext   

#FUNÇÃO PARA SALVAR OS CONSELHOS#
def saveadvice(arq1,arq2,lista_adv):

    #arq1 > arquivo para salvar consehos em Inglês
    #arq2 > arquivo para salvar consehos em Português
    #lista_adv > lista com os conselhos

    with open(arq1, 'r',) as fileread:
        conselhossalvos = fileread.read()

        for i in range(len(lista_adv)):
            if lista_adv[i] in conselhossalvos:
                pass
            else:
                with open(arq1, 'a') as filewrite:
                    filewrite.write(lista_adv[i]+'\n')

    with open(arq1, 'r') as fileread:

        conselhossalvos = fileread.read()
        conselhossalvos = traduzir(conselhossalvos)
        

        with open(arq2, 'w', encoding='utf-8') as filewrite:
            filewrite.write(conselhossalvos)    

#-----------------------------------------------//-----------------------------------#


#INICIALIZANDO ARQUIVOS 
with open(ARQEN, 'a') as fileread:
    pass
with open(ARQPT, 'a') as fileread:
    pass      




#LLAYOUT JANELLA PRINCIPAL
layout = [
    [sg.Text('Quantos conselhos deseja ler'), sg.InputText(size=(10, 1), key='NCONSELHOS'), sg.Button('Gerar')],
    [sg.Text('Relembrar dos conselhos'), sg.Button('Relembrar Todos os conselhos', key = 'RELEMBRAR'), sg.Button(image_filename='trashR.png', button_color=('lightgrey'), key = 'APAGAR')],
    [sg.Text('Buscar por conselhos por ID  '), sg.InputText(size=(10, 1), key='CONSULTAR'), sg.Button('Consultar'), sg.Checkbox('PT-BR', key='CHECKBOX')],
    [sg.Text('pesquisar por: ', font=('Arial', 8, 'italic')), sg.Radio('ID', group_id=1, key='RADIO1', default=True, pad=(0, 0), enable_events=True), sg.Radio('Palavra', key='RADIO2', group_id=1, pad=(0, 0), enable_events=True)],
    [sg.HorizontalSeparator()],
    [sg.Text('Seja Bem vindo! Relembre ou pesquise por novos conselhos', size=(50, 2), key='ERROR', text_color='white', font=('Arial', 10, 'italic'))]
]

mainW = sg.Window('Gerador de Conselhos', layout, resizable=True)

#LOOP JANELA PRINCIPAL
while True:
    
    event, value = mainW.read()
    

    if event == sg.WIN_CLOSED:
        break

    #GERAR CONSELHOS 
    if event == 'Gerar':

        translated = False
      
        try:

            mainW['ERROR'].update('')
            n = int(value['NCONSELHOS'])

            if n < 11:

                strlist = ''

                advice = Advice()
                listadv = advice.advicen(n)

                
                for i in range(len(listadv)):
                    strlist = strlist + listadv[i] + '\n'


                #LAYOUT JANELA GERADA CONSELHOS
                layout2 = [
                    [sg.Text(strlist, key='CONSELHOSL2')],
                    [sg.Button('Fechar'), sg.Button('Salvar Conselhos'), sg.Button(image_filename='brasilR.png', image_size=(24, 24), key='BANDEIRA'), sg.Text('Alterar para PT-BR', font=('Arial', 8, 'italic'), key='LINGUA')]
                ]

                secondW = sg.Window('Conselhos', layout2, modal=True)  

                #LOOP JANELA DE CONSELHOS GERADOS
                while True:

                    eventC, valueC = secondW.read()

                    if eventC == sg.WIN_CLOSED or eventC == 'Fechar':
                        break

                    ####TRADUZIR CONSELHOS####        
                    if eventC == 'BANDEIRA':

                        if translated == False:
                            
                            translatedtext = traduzir(strlist)+'\n'

                            secondW['BANDEIRA'].update(image_filename='inglaterraR.png')
                            secondW['LINGUA'].update('Alterar para EN-UK')
                            secondW['CONSELHOSL2'].update(translatedtext)
                            translated = True

                        else:
                            secondW['BANDEIRA'].update(image_filename='brasilR.png')
                            secondW['LINGUA'].update('Alterar para PT-BR')
                            secondW['CONSELHOSL2'].update(strlist)
                            translated = False




                    ####SALVAR CONSELHOS####
                    if eventC == 'Salvar Conselhos':

                        saveadvice(ARQEN,ARQPT,listadv)                            
                        sg.popup_no_titlebar("Conselhos Salvos!", background_color='#2e3b4e')                    

                    
                               
                secondW.close()

            else:

                mainW['ERROR'].update('Por favor, insira um número inteiro até 10.')
                mainW['ERROR'].update(text_color='red')
                
                traceback.print_exc()

        except:
            
            mainW['ERROR'].update('Por favor, insira um número inteiro até 10.')
            mainW['ERROR'].update(text_color='red')
            
            traceback.print_exc()

    #APAGA CONSELHOS SALVOS
    if event == 'APAGAR':

        confirm = sg.popup("Deseja apagar seus conselhos?", title="Confirmação",custom_text=('Sim', 'Não'))
        if confirm == 'Sim':
            with open(ARQEN, 'w') as fileclean:
                fileclean.write('')
            with open(ARQPT, 'w') as fileclean:
                fileclean.write('')    
            sg.popup_no_titlebar("Conselhos Apagados!", background_color='#2e3b4e') 
                   


    # LEMBRAR CONSELHOS
    if event == 'RELEMBRAR':

        idioma = sg.popup("Qual idioma quer relembrar seus consellhos?", title="Escolha Idioma",custom_text=('Português', 'Inglês'))
        if idioma == 'Inglês':
            os.startfile(ARQEN)
        else:
            os.startfile(ARQPT)
           
       

    ## BUSCA POR ID##
    if event == 'Consultar' and value['RADIO1']:
        idadvice = value['CONSULTAR']

        if value['CHECKBOX']:
            resultadv = findadviceid(idadvice,ARQPT)
        else:
            resultadv = findadviceid(idadvice,ARQEN)    

        if resultadv != None:

            mainW['ERROR'].update('')
            sg.popup_no_titlebar(resultadv, background_color='#2e3b4e')

         
        else:
            mainW['ERROR'].update('ID Não válido/encontrado')
            mainW['ERROR'].update(text_color='red')
            

    #BUSCA POR PALAVRA##
    if event == 'Consultar' and value['RADIO2']:
        
        wordadvice = value['CONSULTAR']
      
        if len(wordadvice) < 3:
            
            mainW['ERROR'].update('O campo deve ter no mínimo 3 caracteres')
            mainW['ERROR'].update(text_color='red')
            
        else:

            if value['CHECKBOX']:
                
                resultadv = findadviceword(wordadvice,ARQPT)
                
                if resultadv == '':
                    mainW['ERROR'].update('Conselho não encontrado')
                    mainW['ERROR'].update(text_color='red')
                else:
                    mainW['ERROR'].update('')
                    sg.popup_no_titlebar(resultadv, background_color='#2e3b4e')

            else:
                resultadv = findadviceword(wordadvice,'conselhos.txt')
                
                if resultadv == '':
                    mainW['ERROR'].update('Conselho não encontrado')
                    mainW['ERROR'].update(text_color='red')
                else:
                    mainW['ERROR'].update('')
                    sg.popup_no_titlebar(resultadv, background_color='#2e3b4e')



mainW.close()
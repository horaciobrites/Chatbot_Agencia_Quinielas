from config import *
import telebot
import threading
from telebot.types import ForceReply
from telebot.types import ReplyKeyboardMarkup
from telebot.types import ReplyKeyboardRemove
from scrap_functions import *

bot=telebot.TeleBot(TELEGRAM_TOKEN)

h={"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}
link_padre="https://www.loteriademisiones.com.ar/portal/juegos/"
cosita=0
usuarios={}
mensajero={}
juego={}


@bot.message_handler(commands=['start','inicio','hola'])
def cmd_start(message):
    markup=ReplyKeyboardRemove()
    bot.send_message(message.chat.id,
                     """Hola! Soy Monin, asistente virtual de Agencia 438\n¿En que te puedo ayudar?\n
Jugar: Creá tu jugada y enviá para que los chicos de la agencia lo procesen y luego pases a pagar y retirar tu tiket.\nSeleccione una opción
        /La_Previa
        /Primera_Matutina
        /Matutina
        /Vespertina
        /Nocturna
        /Nocturna_Plus
        /Poceada
        /Mini_Poceada
    
Extractos: Consultá los resultados de juegos previos. Seleccione una opcion 
        /Extracto_La_Previa
        /Extracto_Primera_Matutina
        /Extracto_Matutina
        /Extracto_Vespertina
        /Extracto_Nocturna
        /Extracto_Nocturna_Plus
        /Extracto_Poceada
        /Extracto_Mini_Poceada
        /Otras_quinielas

    Consultas:
        /verifica_si_tu_ticket_tiene_premio
        /Consultar_Horarios_atencion_agencia
        /Quiero_que_me_atienda_un_humano
    """,
                      reply_markup=markup)

# Funciones de juego
@bot.message_handler(commands=['La_Previa','Primera_Matutina','Matutina','Vespertina','Nocturna','Nocturna_Plus'])
def jugar_quiniela(message):
    juego['juego']=message.text.strip('/')
    juego['fecha']=fecha_actual()
    markup=ForceReply()
    msg=bot.send_message(message.chat.id, "Cual es su nro de DNI?", reply_markup=markup)
    bot.register_next_step_handler(msg, validar_dni)

def validar_dni(message):
    dni=validacion_dni(message.text)
    if not isinstance(dni, int):
        markup=ForceReply()
        msg=bot.send_message(message.chat.id,"No es correcto", reply_markup=markup)
        bot.register_next_step_handler(msg, validar_dni)
    else:
        usuarios['ID_Chat']=message.chat.id
        usuarios['DNI']=dni
        usuarios['juego']=juego['juego']
        usuarios['Nombre']='Julio Da Rosa'
        markup=ForceReply()
        msg=bot.send_message(message.chat.id,
                             "Ingresa tu jugada de la siguiente manera:\nNumero,alcance,Importe\nEjemplo:22,1,100\napuesta el 22 a la cabeza $100",
                             reply_markup=markup)
        bot.register_next_step_handler(msg,conf_jugada)
def conf_jugada(message):
    dicc_jug=jugadas_quiniela(texto=message.text,juego=juego['juego'],fecha=juego['fecha'])
    
    if len(dicc_jug)!=6:
        msg=bot.send_message(message.chat.id, "Error")
        bot.register_next_step_handler(msg,conf_jugada)
    else:
        texto=texto_jugada_quiniela(dicc_jug)
        usuarios['Nro']=dicc_jug['Nro']
        usuarios['Alcance']=dicc_jug['Alcance']
        usuarios['Importe']=dicc_jug['Importe']
        usuarios['Total']=dicc_jug['total']
        markup=ReplyKeyboardMarkup(
                one_time_keyboard=True,
                input_field_placeholder="Pulsa un boton",
                resize_keyboard=True
                )
        markup.add("Confirmar","Modificar",'Cancelar')
        msg=bot.send_message(message.chat.id,texto, parse_mode="html", reply_markup=markup)
        bot.register_next_step_handler(msg,guarda_los_datos)


def guarda_los_datos(message):
    if message.text=="Confirmar":
        guardar_datos(usuarios)
        markup=ReplyKeyboardRemove()
        bot.send_message(message.chat.id,"Listo! su jugada ha sido guardada, no olvide pasar a pagar y retirar su ticket",reply_markup=markup)
    else:
        if message.text =="Modificar":
            markup=ReplyKeyboardRemove()
            msg=bot.send_message(message.chat.id,
                             "Reingresa tu jugada de la siguiente manera:\nNumero,alcance,Importe\nEjemplo:22,1,100\napuesta el 22 a la cabeza $100",reply_markup=markup)
            bot.register_next_step_handler(msg,conf_jugada)
        else:
            if message.text=="Cancelar":
                cmd_start(message)
            


#Funciones de extractos
@bot.message_handler(commands=['Extracto_La_Previa'])
def extracto_la_previa(message):
    link_juego="quiniela-la-previa"
    url=link_padre+link_juego+"/"
    IDS="ResultadosPrevia"
    scrap=quiniela(url,IDS,h)
    texto=texto_resultado_quiniela(scrap)
    mensajero['url']=scrap['link']
    bot.send_message(message.chat.id,texto)

@bot.message_handler(commands=['Extracto_Primera_Matutina'])
def extracto_primera(message):
    link_juego="quiniela-primera-matutina"
    url=link_padre+link_juego+"/"
    IDS="ResultadosPrimera"
    scrap=quiniela(url,IDS,h)
    texto=texto_resultado_quiniela(scrap)
    mensajero['url']=scrap['link']
    bot.send_message(message.chat.id,texto)

@bot.message_handler(commands=['Extracto_Matutina'])
def extracto_matutina(message):
    link_juego="quiniela-matutina"
    url=link_padre+link_juego+"/"
    IDS="ResultadosMatutina"
    scrap=quiniela(url,IDS,h)
    texto=texto_resultado_quiniela(scrap)
    mensajero['url']=scrap['link']
    bot.send_message(message.chat.id,texto)

@bot.message_handler(commands=['Extracto_Vespertina'])
def extracto_vespertina(message):
    link_juego="quiniela-vespertina"
    url=link_padre+link_juego+"/"
    IDS="ResultadosVespertina"
    scrap=quiniela(url,IDS,h)
    texto=texto_resultado_quiniela(scrap)
    mensajero['url']=scrap['link']
    bot.send_message(message.chat.id,texto)
                        
@bot.message_handler(commands=['Extracto_Nocturna'])
def extracto_nocturna(message):
    link_juego="quiniela-nocturna"
    url=link_padre+link_juego+"/"
    IDS="ResultadosNocturna"
    scrap=quiniela(url,IDS,h)
    texto=texto_resultado_quiniela(scrap)
    mensajero['url']=scrap['link']
    bot.send_message(message.chat.id,texto)

@bot.message_handler(commands=['Extracto_Nocturna_Plus'])
def extracto_plus(message):
    link_juego="quiniela-nocturna-plus"
    url=link_padre+link_juego+"/"
    IDS="ResultadosNoctPlus"
    scrap=quiniela(url,IDS,h)
    texto=texto_resultado_quiniela(scrap)
    mensajero['url']=scrap['link']
    bot.send_message(message.chat.id,texto)

@bot.message_handler(commands=['Extracto_Poceada'])
def extracto_poceada(message):
    link_juego="quiniela-poceada"
    url=link_padre+link_juego+"/"
    IDS="ResultadosPoceada"
    scrap=poceada(url,IDS,h)
    texto=texto_resultado_poceada(scrap)
    mensajero['url']=scrap['link']
    bot.send_message(message.chat.id,texto)

@bot.message_handler(commands=['Extracto_Mini_Poceada'])
def extracto_poceada(message):
    link_juego="mini-quiniela-poceada-misionera"
    url=link_padre+link_juego+"/"
    IDS="ResultadosMiniPoceada"
    scrap=poceada_mini(url,IDS,h)
    texto=texto_resultado_mini(scrap)
    mensajero['url']=scrap['link']
    bot.send_message(message.chat.id,texto)

#Funciones de texto

@bot.message_handler(content_types=['text'])
def bot_mensajes_texto (message):
    bot.send_message(message.chat.id,"No estoy seguro de lo que quieres hacer, mejor selecciona una de las siguientes opciones")
    cmd_start(message)
       
# Funcion principal
if __name__=='__main__':
    print('Iniciando bot...')
    bot.infinity_polling()
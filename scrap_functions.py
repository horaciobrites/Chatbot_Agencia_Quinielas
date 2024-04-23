# Este archivo contiene las funciones definidas para realizar el scraping web de la pagina del iplyc
import requests
from bs4 import BeautifulSoup
h={"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}
from config import * # archivos de credenciales

# importacion de librerias
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import requests
from datetime import datetime
import csv

#funcion para escrapear los resultados de la quiniela misionera (previa, primera matutina, matutina, vespertina, nocturna, nocturna plus)
# Devuelve un diccionario con el nombre del juego, nro de sorteo, fecha, y resultado del bolillero
def quiniela(url,IDS,h): #recibe dos argumentos, el link especifico del juego y un valor de texto que permite enconrtar el selector css

    nose={} # definimos el diccionario para almacenar los datos de salida
    res1=requests.get(url, headers=h) # Realizamos la consulta a la web, el header debe definirse como variable global y representa el user-agent 
    soup1=BeautifulSoup(res1.text,"html.parser") #obtenemos el codigo html de la pagina y creamos la sopa
    link_f=soup1.find("iframe",id=IDS).attrs.get("src") # obtenemos el link del la pagina raiz donde estan los reusltados del sorteo
    res2=requests.get(link_f, headers=h) # realizamos el scrap de la pagina web del resultado
    soup2=BeautifulSoup(res2.text,"html.parser") # realizamo la sopa
    juego=soup2.find_all("h2")[0].text # Obtenemos el titulo o nombre del juego
    nro_sorteo=soup2.find("span",class_="simple-highlight").text # Nro de sorteo correspondiente
    fecha=soup2.find_all("option")[0].text # Fecha del sorteo
    bol=[soup2.find_all("td",class_="premio-bolilla")[0].text] # Guardamos el resultado del primer premio
    fec=[]
    j=2
    for i in range(0,76,4): # guardamos en un diccionario los resultados de todo el bolillero
        bol.append(soup2.find_all("td",class_="bolilla")[i].text)
        j=j+1
    j=2
    for i in range(1,10): # guardamos en un diccionario los resultados de todo el bolillero
        fec.append(soup2.find_all("option")[i].text.replace("-","_"))
        j=j+1
    # Completamos el diccionario de  salida
    nose['Juego']=juego 
    nose['Fecha']=fecha
    nose['Sorteo']=nro_sorteo
    nose['Resultados']=bol
    nose['Otros']=fec
    nose['link']=link_f
    return nose


#Funcion para escrapear los resultados de la minipoceada, sigue los mismos pasos, solamente cambia la estructura de la pagina

def poceada_mini (url,IDS,h):
    res1=requests.get(url, headers=h)
    soup1=BeautifulSoup(res1.text,"html.parser")
    link_f=soup1.find("iframe",id=IDS).attrs.get("src")
    res2=requests.get(link_f, headers=h)
    soup2=BeautifulSoup(res2.text,"html.parser")
    juego="Mini "+soup2.find_all("h2")[0].text
    fecha=soup2.find("span",class_="simple-highlight").text.strip()
    sorteo=soup2.find_all("option")[0].text
    ResMini={}
    ResMini['Juego']=juego
    ResMini['Fecha']=fecha
    ResMini['Sorteo']=sorteo
    ResMini['Aciertos'] = []
    ResMini['Ganadores'] = []
    ResMini['Premio'] = []
    ResMini['link']=link_f

    resultado=[]
    for i in range (0,10):
        resultado.append(soup2.find_all("div", class_="Rtable-cell")[i].text)
    ResMini['Resultado']=resultado

    for i in range (0,12,3):
        ResMini['Aciertos'].append(soup2.find_all("td", class_="Rtable-cell")[i].text)
        ResMini['Ganadores'].append(soup2.find_all("td", class_="Rtable-cell")[i+1].text)
        ResMini['Premio'].append(soup2.find_all("td", class_="Rtable-cell")[i+2].text)
    otros=[]
    for i in range(1,10):
        otros.append(soup2.find_all('option')[i].text)
    ResMini['Otros']=otros
    return ResMini


# Funcion para scrapear los resultados de la poceada, los pasos son similares, solamente cambia la estructura del sitio
def poceada (url, IDS, h):
    res1=requests.get(url, headers=h)
    soup1=BeautifulSoup(res1.text,"html.parser")
    link_f=soup1.find("iframe",id=IDS).attrs.get("src")
    res2=requests.get(link_f, headers=h)
    soup2=BeautifulSoup(res2.text,"html.parser")
    juego=soup2.find_all("h2")[0].text
    fecha=soup2.find("span",class_="simple-highlight").text.strip()
    sorteo=soup2.find_all("option")[0].text
    ResPos={}
    ResPos['Juego']=juego
    ResPos['Fecha']=fecha
    ResPos['Sorteo']=sorteo
    ResPos['Aciertos'] = []
    ResPos['Ganadores'] = []
    ResPos['Premio'] = []
    ResPos['Otros']=[]
    ResPos['link']=link_f
    resultado=[]
    for i in range (0,20):
        resultado.append(soup2.find_all("div", class_="Rtable-cell")[i].text)
    ResPos['Resultado']=resultado

    for i in range (0,12,3):
        ResPos['Aciertos'].append(soup2.find_all("td", class_="Rtable-cell")[i].text)
        ResPos['Ganadores'].append(soup2.find_all("td", class_="Rtable-cell")[i+1].text)
        ResPos['Premio'].append(soup2.find_all("td", class_="Rtable-cell")[i+2].text)
    otros=[]
    for i in range(1,10):
        otros.append(soup2.find_all("option")[i].text)
    ResPos['Otros']=otros

    return ResPos


#Funcion que formatea el texto a enviar por mensaje de texto para los resultados de la quiniela, recibe una lista de resultados de la quiniela y devuelve una cadena de texto con formato ideal para ser enviado por telegram
def texto_resultado_quiniela(scrap):
    primer=scrap['Resultados'][0][2:]
    cabeza=primer+" - "+suenios_numeros(scrap['Resultados'][0])
    texto=f"Quiniela Misionera: {scrap['Juego']}\n"
    texto+="Fecha:{:<10}  Sorteo:{:<10}\n".format(scrap['Fecha'],scrap['Sorteo'])
    texto+=f'A LA CABEZA: {cabeza}\n'
    for i in range(0,10):
        texto+="{:>2}   {:>4}            {:>2}   {:>4}\n".format(i+1,scrap['Resultados'][i],(i+11),scrap['Resultados'][i+10])
    texto+=f"\nOtros resultados de {scrap['Juego']}\n"
    for i in range(1,9,2):
        texto+="/{:<10}    /{:<10}\n".format(scrap['Otros'][i],scrap['Otros'][i+1])
    return texto

# idem anterior, recibe un diccionario: resultados de la poceada y devuelve un texto formateado para ser enviado por mensaje de texto en telegram
def texto_resultado_poceada(scrap):
    texto="{:^30}\n".format(scrap['Juego'])
    texto+="Fecha:{:<10}  Sorteo:{:<10}\n".format(scrap['Fecha'],scrap['Sorteo'])
    texto+="{:^30}\n".format("Resultado")
    for i in range (0,20,4):
        texto+="{:<2}     {:<2}     {:<2}     {:<2}\n".format((scrap['Resultado'][i]),(scrap['Resultado'][i+1]),(scrap['Resultado'][i+2]),(scrap['Resultado'][i+3]))
    texto+='\n'
    texto+="{:<10} {:<10} {:<10}\n".format("Aciertos","Ganadores","Premio")
    for i in range(0,4):
        texto+="{:^20}{:<20}{:<20}\n".format(scrap['Aciertos'][i],scrap['Ganadores'][i],scrap['Premio'][i])
    texto+="\n{:<40}\n".format("Otros Resultados")
    for i in range(0,9,3):
        texto+="/{:<6}  /{:<6}  /{:<6}\n".format(scrap['Otros'][i],scrap['Otros'][i+1],scrap['Otros'][i+2])
    
    return texto


# idem anterior, minipoceada
def texto_resultado_mini(scrap):
    texto="{:^30}\n".format(scrap['Juego'])
    texto+="Fecha: {:<10}  Sorteo:{:<10}\n".format(scrap['Fecha'],scrap['Sorteo'])
    texto+="{:^30}\n".format("Resultado")
    for i in range (0,10,5):
        texto+="{:<2}  {:<2}  {:<2}  {:<2}  {:<2}\n".format(scrap['Resultado'][i],scrap['Resultado'][i+1],scrap['Resultado'][i+2],scrap['Resultado'][i+3],scrap['Resultado'][i+4])
    texto+='\n'
    texto+="{:<10} {:<10} {:<10}\n".format("Aciertos","Ganadores","Premio")  
    for i in range(0,4):
        texto+="{:^20} {:^10} {:<20}\n".format(scrap['Aciertos'][i],scrap['Ganadores'][i],scrap['Premio'][i])
    texto+="\n{:^30}\n".format("Otros Resultados")
    for i in range(0,9,3):
        texto+="/{:<6}  /{:<6}   /{:<6}\n".format(scrap['Otros'][i],scrap['Otros'][i+1],scrap['Otros'][i+2])
    return texto

def suenios_numeros(primer_premio):
    num_suenio={'00': 'Huevos','01': 'Agua','02': 'Niño','03': 'San Cono','04': 'La cama','05': 'Gato – Escoba','06': 'Perro','07': 'Revólver',
    '08': 'Incendio','09': 'Arroyo','10': 'Leche – Cañón','11': 'Minero – Medio loco','12': 'Soldado','13': 'La yeta','14': 'Borracho','15': 'Niña bonita',
    '16': 'Anillo','17': 'Desgracia','18': 'La sangre','19': 'Pescado','20': 'La fiesta','21': 'La mujer','22': 'El loco','23': 'Mariposa – Cocinero',
    '24': 'Caballo','25': 'Gallina','26': 'La misa','27': 'El peine','28': 'El cerro','29': 'San Pedro','30': 'Santa Rosa','31': 'La luz','32': 'Dinero',
    '33': 'Cristo','34': 'Cabeza','35': 'Pajarito','36': 'Manteca','37': 'Dentista','38': 'Aceite – Piedra','39': 'La lluvia','40': 'El Cura','41': 'Cuchillo',
    '42': 'Zapatilla','43': 'Sapo – Balcón','44': 'La cárcel','45': 'El vino','46': 'Tomates','47': 'Muerto','48': 'Muerto habla','49': 'La carne',
    '50': 'El pan','51': 'Serrucho','52': 'Madre e hijas','53': 'El barco','54': 'La vaca','55': 'Los gallegos – Música','56': 'La caída','57': 'Jorobado',
    '58': 'Ahogado','59': 'Planta','60': 'Virgen','61': 'Escopeta','62': 'Inundación','63': 'Casamiento','64': 'Llanto','65': 'Cazador','66': 'Lombrices',
    '67': 'Víbora','68': 'Sobrinos','69': 'Vicios','70': 'Muerto sueño','71': 'Cerdo – Excremento','72': 'Sorpresa','73': 'Rengo – Hospital',
    '74': 'Araña – Negros','75': 'Payaso','76': 'Llamas','77': 'Las piernas','78': 'Ramera','79': 'Ladrón','80': 'La bocha','81': 'Flores',
    '82': 'Pelea','83': 'Mal tiempo','84': 'Iglesia','85': 'Linterna – Bicho de luz','86': 'Humo','87': 'Piojos','88': 'El Papa','89': 'La rata',
    '90': 'El miedo','91': 'Pintor – Excusado','92': 'Médico','93': 'Enamorado','94': 'Cementerio','95': 'Anteojos','96': 'Marido','97': 'La mesa',
    '98': 'Lavandera','99': 'Hermano'}
    clave=primer_premio[2:]
    sue=num_suenio[clave]
    return sue


# Esta funcion utiliza selenium para scrapear la pagina de quinielas, ya que es necesario introducir una fecha y presionar buscar
def iniciar_chrome():
    ruta= ChromeDriverManager().install()
    options=Options()
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--windows-size=970,1080")
    #options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-certificate-errors")
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--no-first-run")
    options.add_argument("--no-proxy-server")
    options.add_argument("--no-disable-blink-features=AutomationControlled")#Para que no detecte el sistema antibot
    options.add_argument("--disable-blink-features=AutomationControlled")
    exp_opt = [
        'enable-automation',
        'ignore-certificate-errors',
        'enable-logging'
    ]
    options.add_experimental_option("excludeSwitches",exp_opt)
    prefs = {
        "profile.default_content_setting_values.notifications" : 2,
        "intl.accept_languages" : ["es-ES","es"],
        "credentials_enable_service": False
        }
    options.add_experimental_option("prefs",prefs)
    
    s=Service(ruta)
    driver=webdriver.Chrome(service=s, options=options)
    driver.set_window_position(0,0)
    return driver

# Esta funcion scrapea la pagina de quinielas. Recibe el link la pagina embebida y la fecha que se quiere conocer el extracto
def otras_fechas_quiniela(url,fecha):
    fecha2=fecha.replace("/","").replace("_","-")
    result={}
    driver = iniciar_chrome() #iniciamos el servicio
    driver.get(url)#Nos conectamos a la pagina
    elemento_fecha=driver.find_element(By.CSS_SELECTOR,"select.caja") # seleccionamos la caja de fecha
    elemento_fecha.send_keys(fecha2) #escribimos la fecha en el campo
    time.sleep(2) # tiempo de espera para que se genere la nueva lista
    elemento_buscar=driver.find_element(By.CSS_SELECTOR,"input.myButton") # seleccionamos el boton de busqueda
    time.sleep(1)
    elemento_buscar.click() # click en el boton buscar
    time.sleep(3)
    soup2=BeautifulSoup(driver.page_source,"html.parser")# creamos la sopa
    juego=soup2.find_all("h2")[0].text #Obtenemos el juego
    nro_sorteo=soup2.find("span",class_="simple-highlight").text #Obtenemos el elemento
    fecha=fecha.replace("/","") # registramos la fecha

    bol={1:soup2.find_all("td",class_="premio-bolilla")[0].text }# Primer Premio
    fec={}
    j=2
    for i in range(0,76,4):
        bol[j]=soup2.find_all("td",class_="bolilla")[i].text
        j+=1
    j=2
    for i in range(1,10): # guardamos en un diccionario los resultados de todo el bolillero
        fec[j]= soup2.find_all("option")[i].text.replace("-","_")
        j=j+1
    result['Juego']=juego
    result['Fecha']=fecha2
    result['Sorteo']=nro_sorteo
    result['Resultados']=bol
    result['Otros']=fec
    driver.quit()
    return result

# Esta funcion devuelve el texto formateado para enviar como mensaje, desactiva la fecha seleccionada
def texto_resultado_quiniela_otras(scrap):
    fec_actual=(scrap['Fecha']).replace("-","_")
    primer=scrap['Resultados'][1][2:]
    cabeza=primer+" - "+suenios_numeros(scrap['Resultados'][1])
    texto=f'Quiniela Misionera: {scrap['Juego']}\n'
    texto+=f'Fecha: {scrap['Fecha']},  Sorteo: {scrap['Sorteo']}\n'
    texto+=f'A LA CABEZA: {cabeza}\n'
    for i in range(1,11):
        texto+=f'{i}   {scrap['Resultados'][i]}         {i+10}    {scrap['Resultados'][i+10]} \n'
    texto+=f'\nOtros resultados de {scrap['Juego']}\n'
    for i in range(2,10,2):
        if fec_actual==scrap['Otros'][i] or fec_actual==scrap['Otros'][i+1]:
            if fec_actual==scrap['Otros'][i]:
                texto+=f'{scrap['Otros'][i]}      /{scrap['Otros'][i+1]}\n'
            else:
                texto+=f'/{scrap['Otros'][i]}      {scrap['Otros'][i+1]}\n'
        else: 
            texto+=f'/{scrap['Otros'][i]}     /{scrap['Otros'][i+1]}\n'
    return texto

#Verifica si el valor ingresado como jugada es valido
def verificar_condiciones(lista):
    for sublista in lista:
        if len(sublista) != 3:
            return False
    suma_terceros_elementos = sum(sublista[2] for sublista in lista)
    if suma_terceros_elementos < 100:
        print('El minimo por ticket es de $100')
        return False
    for sublista in lista:
        # Verificar las condiciones para el primer elemento de la sublista
        if not (0 <= sublista[0] < 10000):
            return False
        # Verificar las condiciones para el segundo elemento de la sublista
        if not (0 < sublista[1] < 21):
            return False
        # Verificar las condiciones para el tercer elemento de la sublista
        if not (10 <= sublista[2] <= 5000):
            return False
    return True
# Funcion de verificacion del nro de dni
def validacion_dni(DNI):
    try:
        #DNI=input('Ingrese su DNI')
        DNI=int(DNI.replace(".",""))
        if DNI>999999 and DNI <100000000:
            print('Numero valido')
            return(DNI)
        else:
            print('Numero No valido')
    except ValueError:
        print('Error: No es numerico')
#devuelve un diccionario que contiene la jugada y monto total del ticket
def jugadas_quiniela(texto,juego,fecha):
    jugada={}
    jugada['juego']=juego
    jugada['fecha']=fecha
    
    try:
        filas=texto.strip().split("\n")
        sep= [elemento.split(",") for elemento in filas]
        Nros= [no[0] for no in sep]
        matriz=[[int(elemento) for elemento in fila.split(",")] for fila in filas]
        print(matriz)
        if verificar_condiciones(matriz):
            print("Datos Validos")
            jugada['Nro']=Nros
            jugada['Alcance']=[]
            jugada['Importe']=[]
            ext=len(jugada['Nro'])
            for i in range(0,ext):
                jugada['Alcance'].append(matriz[i][1])
                jugada['Importe'].append(matriz[i][2])
        else:
            print("Error en los datos, Reingrese")
    except ValueError:
        print('Los datos deben ser numericos')
    total=sum(sublista[2] for sublista in matriz)
    jugada['total']=total
    return jugada

#Devuelve el texto formateado alineado para preguntar al usuario si es correcta su jugada
def texto_jugada_quiniela(resultado):
    texto_formateado = "{:^35}\n{:^20}{:^20}\n {:<10} {:<10} {:<10}".format("<b>VERIFIQUE SU JUGADA</b>",resultado['juego'],resultado['fecha'],'Nro', 'Alcance', 'Importe')
    for nro, alcance, importe in zip(resultado['Nro'], resultado['Alcance'], resultado['Importe']):
        texto_formateado += "\n{:^10} {:^20} {:<20}".format(nro, alcance, importe)
    texto_formateado+="\n\nTotal ${:>20}".format(resultado['total'])
    return texto_formateado

#Devuelve fechas y horas actuales
def fecha_actual():
# Obtener la fecha de hoy
    fecha_hoy = datetime.now()

# Formatear la fecha como texto en el formato deseado
    fecha_texto = fecha_hoy.strftime('%d-%m-%Y')

# Imprimir la fecha en formato texto
    return(fecha_texto)
def hora_actual():
    # Obtener la hora actual
    hora_actual = datetime.now().strftime("%H:%M:%S")
    return hora_actual

#Funcion que lee el ultimo id_ticket registrado
def leer_ultimo_id(nombre_archivo):
    """Función para leer el último ID registrado en el archivo CSV"""
    try:
        with open(nombre_archivo, 'r', newline='') as archivo_csv:
            lector_csv = csv.DictReader(archivo_csv)
            ultimo_id = 0
            for linea in lector_csv:
                ultimo_id = max(ultimo_id, int(linea['ID_Ticket']))
            return ultimo_id
    except FileNotFoundError:
        return 0
#Funcion que guarda el registro de venta en un csv

def guardar_datos(datos):

     with open(nombre_archivo, 'a', newline='') as csvfile:
          writer = csv.writer(csvfile)
          ID_Chat=datos['ID_Chat']
          ID_Ticket=leer_ultimo_id(nombre_archivo)+1
          Nombre='Julio Da Rosa'
          Fecha=fecha_actual()
          Hora=hora_actual()
          juego=datos['juego']
          Fecha_Sorteo=fecha_actual()
          Total=datos['Total']
          Nro=datos['Nro']
          Alcance=datos['Alcance']
          Importe=datos['Importe']
          n=len(datos['Nro'])
          for i in range(0,n):
               writer.writerow([ID_Chat,ID_Ticket,Nombre,Fecha,Hora,juego,Fecha_Sorteo,Nro[i],Alcance[i],Importe[i],Total])





from telegram import Update, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, CallbackContext
import os
from io import BytesIO
import base64
import requests
import datetime
import time 
from api_handler import consultar_reniec, consultar_reniec_una_foto, consultar_sunarp
from api_handler import obtener_dni_virtual, obtener_dni_electronico, obtener_antecedentes_judiciales
from api_handler import obtener_antecedentes_policiales, obtener_antecedentes_penales
from api_handler import obtener_c4_azul, obtener_c4_blanco, obtener_c4_inscripcion
from api_handler import consultar_sentinel, consultar_boleta_informativa, consultar_acta_nacimiento
from api_handler import consultar_acta_matrimonio, consultar_acta_defuncion, consultar_papeletas_api, format_papeleta_message
from api_handler import consultar_notas
from api_text import consultar_nombre, dniBasicoTexto, consultaHogar, consultar_predios
from api_text import consultar_numeros, consultar_familiares, consultar_arbol, consultar_hermanos
from api_text import consultar_bitel, consultar_claro, consultar_placas, consultar_correo
from api_text import consultar_sueldos, consultar_sbs, consultar_geo, consultar_ruc, consultar_sunedu
from api_text import verificar_numeros, consultar_migraciones, consultar_mininter, consultar_carnet_extranjeria
from api_text import consultar_mpfn, consultar_movistar, consultar_bolivia, consultar_licencia
from io import BytesIO
from config import TELEGRAM_BOT_TOKEN, token_api
from pymongo import MongoClient

token = TELEGRAM_BOT_TOKEN

AUTH_TOKEN = token_api
client = MongoClient("mongodb+srv://thikhabot:h4inj4I5STCtpHF5@thikhadox.bdmbaay.mongodb.net/?retryWrites=true&w=majority")
db = client.keys
customers_collection = db.customers

async def start(update: Update, context: ContextTypes):
    user_id = update.effective_user.id
    user = update.effective_user
    name = user.first_name
    caption = (
        f"*[#PeruDox]*\n\n"
        f"[[📍]] *Bienvenido `{name}`*\n"
        f"[[💻]] [{name}](tg://user?id={user_id}) - {user_id} \n\n"

        f"[[📝]] Para registrarte usa → /register\n"
        f"[[⚙️]] Para ver comandos usa → /cmds\n"
        f"[[🙎‍♂️]] Para ver tu perfil usa → /me\n"

    )
    photo_path = 'doxperubot.jpg'

    # Crear los botones inline
    # button_cmds = InlineKeyboardButton(text="Registarse", callback_data='/register')
    # button_profile = InlineKeyboardButton(text="Comandos", callback_data='/cmds')
    # keyboard = InlineKeyboardMarkup([[button_cmds, button_profile]])

    await context.bot.send_photo(
        chat_id=update.message.chat_id, 
        photo=open(photo_path, 'rb'), 
        caption=caption, 
        parse_mode='Markdown',
        # reply_markup=keyboard
    )
# async def button_start(update: Update, context: ContextTypes):
#     query = update.callback_query
#     await query.answer()
    
#     # Aquí defines las acciones a realizar cuando se presionan los botones
#     if query.data == '/register':
#         await context.bot.send_message(chat_id=update.effective_chat.id)
#     elif query.data == '/cmds':
#         await context.bot.send_message(chat_id=update.effective_chat.id)

async def send_initial_message(update: Update):
    try:
        chat_id = update.effective_chat.id

        keyboard = [
            [InlineKeyboardButton("[🪪] RENIEC", callback_data='reniec'),
             InlineKeyboardButton("[📜] ACTAS", callback_data='actas')],
            [InlineKeyboardButton("[👨‍👩‍👦‍👦] FAMILIA", callback_data='familia'),
             InlineKeyboardButton("[👮🏻‍♀️] DELITOS", callback_data='delitos')],
            [InlineKeyboardButton("[📞] TELEFONÍA", callback_data='telefonia'),
             InlineKeyboardButton("[📚] ACADÉMICO", callback_data='academico')],             
            [InlineKeyboardButton("[🚘] VEHÍCULOS", callback_data='vehiculos'),
             InlineKeyboardButton("[💰] FINANCIERO", callback_data='financiero')],
            [InlineKeyboardButton("[⚙️] GENERADOR", callback_data='generador'),
             InlineKeyboardButton("[➕] EXTRA", callback_data='extra')],             
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        caption = (
            f"*[#PeruDox]* ➜ *COMANDOS*\n\n"
            f"*Bienvenido al menú principal de comandos*\n\n"
            f"*Este centro de comandos está dividido por secciones para su fácil manejo.*\n\n"
            f"*⬇️ Selecciona una de las opciones para visualizar su contenido ⬇️*\n\n"
        )

        await update.message.reply_text(text=caption, reply_markup=reply_markup, parse_mode='Markdown')
    except Exception as e:
        print(f"Error al enviar mensaje inicial: {e}")

async def button_click(update: Update, context: CallbackContext):
    try:
        query = update.callback_query
        await query.answer()
        if query.data == 'inicio':
            await show_main_menu(update, context)
        if query.data == 'reniec':
            text = (
                "*[#PeruDox]* ➜ *[CMDS - RENIEC]*\n\n"
                "*[📍] RENIEC ONLINE - 1 FOTO [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /dni 00000001\n"
                "*Consumo* → 2 créditos\n"
                "*Desc* → Datos completos en texto e imagen del rostro\n\n"

                "*[📍] RENIEC ONLINE - 4 FOTO [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /dnf 00000001\n"
                "*Consumo* → 3 créditos\n"
                "*Desc* → Datos completos en texto e imágenes rostro, huellas y firma\n\n"

                "*[📍] RENIEC ONLINE - TEXTO [FREE]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /dnx 00000001\n"
                "*Consumo* → 0 créditos\n"
                "*Desc* → Datos básicos en texto\n\n"

                "*[📍] RENIEC NOMBRES ONLINE - [FREE]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /nm Nombre|Apellido|Apellido\n"
                "*Consumo* → 0 créditos\n"
                "*Desc* → Número de DNI de coincidencias\n\n"                
            )
        elif query.data == 'actas':
            text = (
                "*[#PeruDox]* ➜ *[CMDS - ACTAS]*\n\n"
                "*[📍] ACTA DE NACIMIENTO [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /actna 00000001\n"
                "*Consumo* → 15 créditos\n"
                "*Desc* → Busca actas de nacimiento por DNI\n\n"

                "*[📍] ACTA DE MATRIMONIO [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /actma 00000001\n"
                "*Consumo* → 15 créditos\n"
                "*Desc* → Busca actas de matrimonio por DNI\n\n"

                "*[📍] ACTA DE DEFUNCIÓN [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /actde 00000001\n"
                "*Consumo* → 15 créditos\n"
                "*Desc* → Busca actas de defunción por DNI\n\n"

            )
        elif query.data == 'telefonia':
            text = (
                "*[#PeruDox]* ➜ *[CMDS - TELEFONÍA]*\n\n"
                "*[📍] BÚSQUEDA DE NÚMEROS [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /tel 00000001\n"
                "*Uso* → /tel 999999999\n"
                "*Consumo* → 4 créditos\n"
                "*Desc* → Busca titulares/teléfonos por número o DNI\n\n"

                "*[📍] BÚSQUEDA OSIPTEL [FREE]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /telx 00000001\n"
                "*Consumo* → 0 créditos\n"
                "*Desc* → Busca teléfonos por DNI de todas las operadoras\n\n"

                "*[📍] BÚSQUEDA NÚMEROS CLARO [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /claro 00000001\n"
                "*Consumo* → 2 créditos\n"
                "*Desc* → Busca teléfonos de Claro por DNI\n\n"

                "*[📍] BÚSQUEDA NÚMEROS MOVISTAR [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /movistar 00000001\n"
                "*Consumo* → 2 créditos\n"
                "*Desc* → Busca teléfonos de Movistar por DNI\n\n"

                "*[📍] BÚSQUEDA NÚMEROS BITEL [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /bitel 00000001\n"
                "*Consumo* → 2 créditos\n"
                "*Desc* → Busca teléfonos de Bitel por DNI\n"                
            )

        elif query.data == 'academico':
            text = (
                "*[#PeruDox]* ➜ *[CMDS - ACADÉMICO]*\n\n"
                "*[📍] NOTAS [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /notas 00000001\n"
                "*Consumo* → 4 créditos\n"
                "*Desc* → Busca notas académicas por DNI\n\n"

                "*[📍] SUNEDU [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /sunedu 00000001\n"
                "*Consumo* → 5 créditos\n"
                "*Desc* → Busca títulos universitarios por DNI\n\n"

            )                        
        elif query.data == 'generador':
            text = (
                "*[#PeruDox]* ➜ *[CMDS - GENERADOR]*\n\n"
                "*[📍] RENIEC FICHA C4 AZUL [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /c4a 00000001\n"
                "*Consumo* → 4 créditos\n"
                "*Desc* → Genera ficha C4 azul en PDF\n\n"

                "*[📍] RENIEC FICHA C4 BLANCO [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /c4b 00000001\n"
                "*Consumo* → 4 créditos\n"
                "*Desc* → Genera ficha C4 blanco en PDF\n"

                "*[📍] RENIEC FICHA C4 INSCRIPCIÓN [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /c4i 00000001\n"
                "*Consumo* → 4 créditos\n"
                "*Desc* → Genera ficha C4 inscripción en PDF\n\n"

                "*[📍] RENIEC DNI VIRTUAL [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /dniv 00000001\n"
                "*Consumo* → 5 créditos\n"
                "*Desc* → Genera DNI virtual ambos lados\n\n"
                
                "*[📍] RENIEC DNI ELECTRÓNICO [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /dnie 00000001\n"
                "*Consumo* → 5 créditos\n"
                "*Desc* → Genera DNI electrónico ambos lados\n\n"
                )
        elif query.data == 'familia':
            text = (
                "*[#PeruDox]* ➜ *[CMDS - FAMILIA]*\n\n"
                "*[📍] HOGAR [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /hog 00000001\n"
                "*Consumo* → 3 créditos\n"
                "*Desc* → Busca integrantes de un hogar por DNI\n\n"

                "*[📍] FAMILIA [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /fam 00000001\n"
                "*Consumo* → 3 créditos\n"
                "*Desc* → Busca familiares por DNI\n\n"

                "*[📍] ÁRBOL GENEALÓGICO [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /arb 00000001\n"
                "*Consumo* → 6 créditos\n"
                "*Desc* → Busca padres, hermanos, tíos, etc por DNI\n\n"

                "*[📍] HERMANOS [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /herm 00000001\n"
                "*Consumo* → 2 créditos\n"
                "*Desc* → Busca hermanos por DNI\n\n"

            )
        elif query.data == 'delitos':
            text = (
                "*[#PeruDox]* ➜ *[CMDS - DELITOS]*\n\n"
                "*[📍] ANTECEDENTES JUDICIALES [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /antju 00000001\n"
                "*Consumo* → 5 créditos\n"
                "*Desc* → PDF Generado\n\n"

                "*[📍] ANTECEDENTES POLICIALES [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /antpo 00000001\n"
                "*Consumo* → 5 créditos\n"
                "*Desc* → PDF Generado\n\n"

                "*[📍] ANTECEDENTES PENALES [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /antpe 00000001\n"
                "*Consumo* → 5 créditos\n"
                "*Desc* → PDF Generado\n\n"

                "*[📍] MPFN [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /mpfn 00000001\n"
                "*Consumo* → 5 créditos\n"
                "*Desc* → Consulta en MPFN por DNI\n\n"                

            )
        elif query.data == 'financiero':
            text = (
                "*[#PeruDox]* ➜ *[CMDS - FINANCIERO]*\n\n"
                "*[📍] SUELDOS [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /sueldos 00000001\n"
                "*Consumo* → 2 créditos\n"
                "*Desc* → Busca sueldos por DNI\n\n"

                "*[📍] SENTINEL [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /sentinel 00000001\n"
                "*Consumo* → 10 créditos\n"
                "*Desc* → Reporte Sentinel de los últimos meses\n\n"

                "*[📍] SBS [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /sbs 00000001\n"
                "*Consumo* → 10 créditos\n"
                "*Desc* → Reporte SBS de los últimos meses\n\n"
            )
        elif query.data == 'vehiculos':
            text = (
                "*[#PeruDox]* ➜ *[CMDS - VEHÍCULOS]*\n\n"
                "*[📍] SUNARP [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /sunarp RM1514\n"
                "*Consumo* → 3 créditos\n"
                "*Desc* → Datos de propiedades SUNARP por placa\n\n"

                "*[📍] PLACAS [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /placas RM1514\n"
                "*Consumo* → 5 créditos\n"
                "*Desc* → Datos de una placa y propietarios por placa\n\n"

                "*[📍] PAPELETAS [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /papeletas RM1514\n"
                "*Consumo* → 3 créditos\n"
                "*Desc* → Datos de papeletas y evidencia por placa\n\n"
             
                "*[📍] LICENCIAS [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /licen 00000001\n"
                "*Consumo* → 2 créditos\n"
                "*Desc* → Datos de licencias MTC por DNI\n\n"
                          
            )
        elif query.data == 'extra':
            text = (
                "*[#PeruDox]* ➜ *[CMDS - EXTRA]*\n\n"
                "*[📍] CORREOS [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /correo 00000001\n"
                "*Consumo* → 2 créditos\n"
                "*Desc* → Correos por DNI\n\n"

                "*[📍] BOLETAS [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /boletas 00000001\n"
                "*Consumo* → 2 créditos\n"
                "*Desc* → PDF Generado\n\n"

                "*[📍] GEOLOCALIZACIÓN [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /geo 138.197.126.79\n"
                "*Consumo* → 1 créditos\n"
                "*Desc* → Geolocalización por IP\n\n"
                
                "*[📍] RUC [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /ruc 20486484013\n"
                "*Consumo* → 5 créditos\n"
                "*Desc* → Datos completos por RUC \n\n" 

                "*[📍] PREDIOS [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /pred 44443333\n"
                "*Consumo* → 2 créditos\n"
                "*Desc* → Datos predios por DNI \n\n"   

                "*[📍] MIGRACIONES [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /migr 44443333\n"
                "*Consumo* → 4 créditos\n"
                "*Desc* → Busca migraciones por DNI \n\n"  

                "*[📍] MININTER [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /minin 44443333\n"
                "*Consumo* → 2 créditos\n"
                "*Desc* → Busca mininter por DNI \n\n"                                                                 

                "*[📍] CARNET EXTRANJERÍA [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /carnetx 44443333\n"
                "*Consumo* → 2 créditos\n"
                "*Desc* → Busca carnet de extranjería por DNI \n\n"  

                "*[📍] BOLIVIA [PREMIUM]*\n\n"
                "*Estado* → Activo [🟢]\n"
                "*Uso* → /bolivia 44443333\n"
                "*Consumo* → 2 créditos\n"
                "*Desc* → Busca bolivianos por DNI \n\n"                  
            )            
        elif query.data == 'inicio':
            await send_initial_message(update)
            return
        else:
            text = "Opción no reconocida."

        await query.message.edit_text(text=text, parse_mode='Markdown')

        # Mostrar los botones de 'Inicio' al final de cualquier acción
        keyboard = [
            [InlineKeyboardButton("[🪪] RENIEC", callback_data='reniec'),
             InlineKeyboardButton("[📜] ACTAS", callback_data='actas')],
            [InlineKeyboardButton("[👨‍👩‍👦‍👦] FAMILIA", callback_data='familia'),
             InlineKeyboardButton("[👮🏻‍♀️] DELITOS", callback_data='delitos')],
            [InlineKeyboardButton("[📞] TELEFONÍA", callback_data='telefonia'),
             InlineKeyboardButton("[📚] ACADÉMICO", callback_data='academico')],             
            [InlineKeyboardButton("[🚘] VEHÍCULOS", callback_data='vehiculos'),
             InlineKeyboardButton("[💰] FINANCIERO", callback_data='financiero')],
            [InlineKeyboardButton("[⚙️] GENERADOR", callback_data='generador'),
             InlineKeyboardButton("[➕] EXTRA", callback_data='extra')],      
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.edit_reply_markup(reply_markup=reply_markup)
    except Exception as e:
        return

async def cmds(update: Update, context: CallbackContext):
    try:
        if update.message:
            await send_initial_message(update)
        else:
            print("Error: Update message is None in cmds.")
    except Exception as e:
        print(f"Error in cmds function: {e}")

async def show_main_menu(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("[🪪] RENIEC", callback_data='reniec'),
            InlineKeyboardButton("[📜] ACTAS", callback_data='actas')],
        [InlineKeyboardButton("[👨‍👩‍👦‍👦] FAMILIA", callback_data='familia'),
            InlineKeyboardButton("[👮🏻‍♀️] DELITOS", callback_data='delitos')],
        [InlineKeyboardButton("[📞] TELEFONÍA", callback_data='telefonia'),
            InlineKeyboardButton("[📚] ACADÉMICO", callback_data='academico')],             
        [InlineKeyboardButton("[🚘] VEHÍCULOS", callback_data='vehiculos'),
            InlineKeyboardButton("[💰] FINANCIERO", callback_data='financiero')],
        [InlineKeyboardButton("[⚙️] GENERADOR", callback_data='generador'),
            InlineKeyboardButton("[➕] EXTRA", callback_data='extra')], 
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    caption = (
        f"*[#PeruDox]* ➜ *COMANDOS*\n\n"
        f"*Bienvenido al menú principal de comandos*\n\n"
        f"*Este centro de comandos está dividido por secciones para su fácil manejo.*\n\n"
        f"*⬇️ Selecciona una de las opciones para visualizar su contenido ⬇️*\n\n"
    )

    await context.bot.send_message(chat_id=update.effective_chat.id, text=caption, reply_markup=reply_markup, parse_mode='Markdown')
      
def register_user(telegram_id, name):
    payload = {
        "telegram_id": telegram_id,
        "name": name
    }
    headers = {
        "Authorization": AUTH_TOKEN,
        "Content-Type": "application/json"
    }
    API_URL = "http://127.0.0.1:80/register_customer"

    response = requests.post(API_URL, json=payload, headers=headers)
    return response.json()

async def register(update: Update, context: CallbackContext):
    user = update.effective_user
    user_id = user.id
    user_name = user.username or user.full_name

    result = register_user(user_id, user_name)

    if result.get("message") == "Customer registered successfully":
        await update.message.reply_text(f"¡Registro exitoso! Tu ID de usuario es: {user_id} y tienes 5 créditos.")
    elif result.get("message") == "Customer already registered":
        await update.message.reply_text(f"Ya te encuentras registrado. Tu ID de usuario es: {user_id}.")
    else:
        await update.message.reply_text("Hubo un problema al registrar tu usuario. Por favor, intenta de nuevo más tarde.")

async def me(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user = update.effective_user
    name = user.first_name
    
    # Buscar el usuario en la base de datos por su user_id
    customer = customers_collection.find_one({'telegram_id': user_id})
    user_rec_username = user.username if user.username else "Sin username"

    if customer:
        role = customer.get('role')
        plan = customer.get('plan')
        credits = customer.get('credits')
        status = customer.get('status')
        antispam = customer.get('antispam')
        joined_date = customer.get('join_date')
        end_date = customer.get('end_date')
        query = customer.get('query')
        profile_text = (
            f"*[#PeruDox]*\n\n"
            f"*PERFIL DE {name}:*\n\n"
            f"*[🙎‍♂️] ID:* `{user_id}`\n"
            f"*[🗒] NOMBRE:* `{name}`\n"
            f"*[⚡️] USER:* [{user_rec_username}](tg://user?id={user_id})\n"
            f"*[〽️] ROL:* `{role}`\n"
            f"*[📈] PLAN:* `{plan}`\n"
            f"*[💰] CRÉDITOS:* `{credits}`\n"
            f"*[👺] ESTADO:* `{status}`\n"
            f"*[⏱] ANTI-SPAM:* `{antispam}`\n"
            f"*[⏱] CONSULTAS:* `{query}`\n"
            f"*[📅] UNIDO:* `{joined_date}`\n"
        )
        if end_date:
            try:
                end_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
                if end_date_obj > datetime.datetime.now():
                    profile_text += f"*[💥] FIN MEMBRESIA:* `{end_date}`\n"
            except ValueError:
                profile_text += f"*[💥] FIN MEMBRESIA:* `Fecha inválida: {end_date}`\n"
    else:
        profile_text = "No se encontraron datos para tu perfil."

    photo_path = 'doxperubot.jpg'  # Asegúrate de que la ruta sea correcta

    # Envía la imagen junto con la descripción del perfil
    await context.bot.send_photo(
        chat_id=update.message.chat_id, 
        photo=open(photo_path, 'rb'), 
        caption=profile_text, 
        parse_mode='Markdown'
    )

async def user_info(update: Update, context: CallbackContext):
    user_adm_id = update.effective_user.id
    customer = customers_collection.find_one({'telegram_id': user_adm_id})
    
    if not customer or customer['role'] not in ['OWNER', 'SELLER']:
        return

    try:
        args = context.args
        if len(args) != 1:
            await update.message.reply_text("Uso incorrecto del comando. Ejemplo: /user {id}")
            return

        user_id_str = args[0]
        if not user_id_str.isdigit():
            await update.message.reply_text("El ID debe ser un número entero.")
            return

        user_id = int(user_id_str)

        # Obtener datos del usuario desde la base de datos
        customer = customers_collection.find_one({'telegram_id': user_id})
        user_rec_username = "Sin username"
        
        try:
            chat_member = await context.bot.get_chat_member(chat_id=user_id, user_id=user_id)
            user_rec_username = chat_member.user.username if chat_member.user.username else "Sin username"
        except Exception:
            pass

        if customer:
            name = customer.get('name', 'Sin nombre')
            role = customer.get('role')
            plan = customer.get('plan')
            credits = customer.get('credits')
            status = customer.get('status')
            antispam = customer.get('antispam')
            joined_date = customer.get('join_date', 'Sin fecha de unión')
            end_date = customer.get('end_date')
            query = customer.get('query')

            mensaje = (
                f"*[#PeruDox]*\n\n"
                f"*PERFIL DEL USUARIO {name}:*\n\n"
                f"*[🗒] NOMBRE:* `{name}`\n"
                f"*[⚡️] USER:* [{user_rec_username}](tg://user?id={user_id})\n"
                f"*[〽️] ROL:* `{role}`\n"
                f"*[📈] PLAN:* `{plan}`\n"
                f"*[💰] CRÉDITOS:* `{credits}`\n"
                f"*[👺] ESTADO:* `{status}`\n"
                f"*[⏱] ANTI-SPAM:* `{antispam}`\n"
                f"*[⏱] CONSULTAS:* `{query}`\n"
                f"*[📅] UNIDO:* `{joined_date}`\n"
            )

            if end_date:
                try:
                    end_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
                    if end_date_obj > datetime.datetime.now():
                        mensaje += f"*[💥] FIN MEMBRESIA:* `{end_date}`\n"
                except ValueError:
                    mensaje += f"*[💥] FIN MEMBRESIA:* `Fecha inválida: {end_date}`\n"

            await update.message.reply_text(mensaje, parse_mode='Markdown')
        else:
            await update.message.reply_text(f"No se encontraron datos para el usuario con ID {user_id}.")

    except ValueError:
        await update.message.reply_text("El ID debe ser un número entero.")
    except Exception as e:
        await update.message.reply_text(f"Error al obtener información del usuario: {str(e)}")
        
def enviar_mensaje_telegram(mensaje):
    token_control = '7438314120:AAELmuyCEZ0LK_DOPrYFNXZV6T82oxXIG7g'  # Reemplaza con el token de tu bot
    chat_id = '-4214470486'
    url = f'https://api.telegram.org/bot{token_control}/sendMessage?chat_id={chat_id}&text={mensaje}&parse_mode=Markdown'
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f'Error al enviar mensaje a Telegram: {e}')

async def add_cred(update: Update, context: CallbackContext):
    # Verificar el rol del usuario administrador
    user_adm_id = update.effective_user.id
    customer = customers_collection.find_one({'telegram_id': user_adm_id})
    if not customer or customer['role'] not in ['OWNER', 'SELLER']:
        return
    
    try:
        args = context.args
        if len(args) != 2:
            await update.message.reply_text("Uso incorrecto del comando. Ejemplo: /add_cred {id} {cantidad}")
            return
        
        # Información del usuario administrador que envía el comando
        user_adm_username = update.effective_user.username if update.effective_user.username else "Sin username"

        user_id = int(args[0])
        amount = int(args[1])

        # Obtener el username del usuario receptor desde Telegram
        try:
            chat_member = await context.bot.get_chat_member(chat_id=user_id, user_id=user_id)
            user_rec_username = chat_member.user.username if chat_member.user.username else "Sin username"
        except Exception as e:
            await update.message.reply_text(f"No se pudo obtener el username para el ID {user_id}.")
            return

        data = {
            'user_id': user_id,
            'amount': amount
        }

        API_URL = "http://127.0.0.1:80/add_credits"
        headers = {
            'Authorization': AUTH_TOKEN,
            'Content-Type': 'application/json'
        }

        response = requests.post(API_URL, json=data, headers=headers)

        if response.status_code == 200:
            mensaje1 = f"[{user_adm_username}](tg://user?id={user_adm_id})"
            mensaje2 = f"[{user_rec_username}](tg://user?id={user_id})"
            mensajito = f"{mensaje1} actualizó los créditos a {amount} para {mensaje2}"
            await update.message.reply_text(mensajito, parse_mode='Markdown')
            mensaje = (
                f"ENVIADO POR: [{user_adm_username}](tg://user?id={user_adm_id}) - {user_adm_id}\n"
                f"CRÉDITOS: {amount}\n"
                f"RECIBIDO POR: [{user_rec_username}](tg://user?id={user_id}) - {user_id}\n"
            )
            enviar_mensaje_telegram(mensaje)
        else:
            await update.message.reply_text(f"No se encontró al usuario {user_id}.")

    except ValueError:
        await update.message.reply_text("ID y cantidad deben ser números enteros.")
    except requests.RequestException as e:
        await update.message.reply_text(f"Error en la solicitud.")
    except Exception as e:
        await update.message.reply_text(f"Error.")

async def more_cred(update: Update, context: CallbackContext):
    # Verificar el rol del usuario administrador
    user_adm_id = update.effective_user.id
    customer = customers_collection.find_one({'telegram_id': user_adm_id})
    if not customer or customer['role'] not in ['OWNER', 'SELLER']:
        return
    
    try:
        args = context.args
        if len(args) != 2:
            await update.message.reply_text("Uso incorrecto del comando. Ejemplo: /more_cred {id} {cantidad}")
            return
        
        user_adm_username = update.effective_user.username if update.effective_user.username else "Sin username"

        user_id = int(args[0])
        amount = int(args[1])

        # Obtener el username del usuario receptor desde Telegram
        try:
            chat_member = await context.bot.get_chat_member(chat_id=user_id, user_id=user_id)
            user_rec_username = chat_member.user.username if chat_member.user.username else "Sin username"
        except Exception as e:
            await update.message.reply_text(f"No se pudo obtener el username para el ID {user_id}.")
            return

        data = {
            'user_id': user_id,
            'amount': amount
        }

        API_URL = "http://127.0.0.1:80/more_credits"
        headers = {
            'Authorization': AUTH_TOKEN,
            'Content-Type': 'application/json'
        }

        response = requests.post(API_URL, json=data, headers=headers)

        if response.status_code == 200:
            mensajito = f"[{user_adm_username}](tg://user?id={user_adm_id}) aumentó {amount} créditos para [{user_rec_username}](tg://user?id={user_id})"
            await update.message.reply_text(mensajito, parse_mode='Markdown')
            mensaje = (
                f"ENVIADO POR: [{user_adm_username}](tg://user?id={user_adm_id}) - {user_adm_id}\n"
                f"CRÉDITOS: {amount}\n"
                f"RECIBIDO POR: [{user_rec_username}](tg://user?id={user_id}) - {user_id}\n"
            )
            enviar_mensaje_telegram(mensaje)     
        else:
            await update.message.reply_text(f"No se encontró al usuario {user_id}.")

    except ValueError:
        await update.message.reply_text("ID y cantidad deben ser números enteros.")
    except requests.RequestException as e:
        await update.message.reply_text(f"Error en la solicitud.")
    except Exception as e:
        await update.message.reply_text(f"Error.")

async def add_days(update: Update, context: CallbackContext):
    # Verificar el rol del usuario administrador
    user_adm_id = update.effective_user.id
    customer = customers_collection.find_one({'telegram_id': user_adm_id})
    if not customer or customer['role'] not in ['OWNER', 'SELLER']:
        return
    
    try:
        args = context.args
        if len(args) != 2:
            await update.message.reply_text("Uso incorrecto del comando. Ejemplo: /add_days {id} {cantidad_días}")
            return
        
        # Información del usuario administrador que envía el comando
        user_adm_username = update.effective_user.username if update.effective_user.username else "Sin username"

        user_id = int(args[0])
        days = int(args[1])

        # Obtener el username del usuario receptor desde Telegram
        try:
            chat_member = await context.bot.get_chat_member(chat_id=user_id, user_id=user_id)
            user_rec_username = chat_member.user.username if chat_member.user.username else "Sin username"
        except Exception as e:
            await update.message.reply_text(f"No se pudo obtener el username para el ID {user_id}.")
            return

        API_URL = "http://127.0.0.1:80/add_days"
        headers = {
            'Authorization': AUTH_TOKEN,
            'Content-Type': 'application/json'
        }

        data = {
            'user_id': user_id,
            'days': days
        }

        response = requests.post(API_URL, json=data, headers=headers)

        if response.status_code == 200:
            result = response.json()
            mensajito = f"[{user_adm_username}](tg://user?id={user_adm_id}) actualizó los días a {days} para [{user_rec_username}](tg://user?id={user_id})"
            await update.message.reply_text(mensajito, parse_mode='Markdown')
            mensaje = (
                f"ENVIADO POR: [{user_adm_username}](tg://user?id={user_adm_id}) - {user_adm_id}\n"
                f"DÍAS: {days}\n"
                f"RECIBIDO POR: [{user_rec_username}](tg://user?id={user_id}) - {user_id}\n"
            )
            enviar_mensaje_telegram(mensaje)
        else:
            await update.message.reply_text(f"Error al agregar días: {response.json().get('error', 'Error desconocido')}")

    except ValueError:
        await update.message.reply_text("ID y cantidad de días deben ser números enteros.")
    except requests.RequestException:
        await update.message.reply_text("Error en la solicitud.")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def more_days(update: Update, context: CallbackContext):
    # Verificar el rol del usuario administrador
    user_adm_id = update.effective_user.id
    customer = customers_collection.find_one({'telegram_id': user_adm_id})
    if not customer or customer['role'] not in ['OWNER', 'SELLER']:
        return
     
    try:
        args = context.args
        if len(args) != 2:
            await update.message.reply_text("Uso incorrecto del comando. Ejemplo: /more_days {id} {cantidad_días}")
            return
        
        # Información del usuario administrador que envía el comando
        user_adm_username = update.effective_user.username if update.effective_user.username else "Sin username"

        user_id = int(args[0])
        days = int(args[1])

        # Obtener el username del usuario receptor desde Telegram
        try:
            chat_member = await context.bot.get_chat_member(chat_id=user_id, user_id=user_id)
            user_rec_username = chat_member.user.username if chat_member.user.username else "Sin username"
        except Exception as e:
            await update.message.reply_text(f"No se pudo obtener el username para el ID {user_id}.")
            return

        API_URL = "http://127.0.0.1:80/more_days"
        headers = {
            'Authorization': AUTH_TOKEN,
            'Content-Type': 'application/json'
        }

        data = {
            'user_id': user_id,
            'days': days
        }

        response = requests.post(API_URL, json=data, headers=headers)

        if response.status_code == 200:
            result = response.json()
            mensajito = f"[{user_adm_username}](tg://user?id={user_adm_id}) aumentó {days} para [{user_rec_username}](tg://user?id={user_id})"
            await update.message.reply_text(mensajito, parse_mode='Markdown')
            mensaje = (
                f"ENVIADO POR: [{user_adm_username}](tg://user?id={user_adm_id}) - {user_adm_id}\n"
                f"DÍAS: {days}\n"
                f"RECIBIDO POR: [{user_rec_username}](tg://user?id={user_id}) - {user_id}\n"
            )
            enviar_mensaje_telegram(mensaje)
        else:
            await update.message.reply_text(f"Error al agregar días: {response.json().get('error', 'Error desconocido')}")

    except ValueError:
        await update.message.reply_text("ID y cantidad de días deben ser números enteros.")
    except requests.RequestException:
        await update.message.reply_text("Error en la solicitud.")
    except Exception as e:
        await update.message.reply_text(f"Error.")

async def verificar_mensualidad_activa(user_id):
    try:
        # Obtener los datos del usuario desde la base de datos
        customer = customers_collection.find_one({'telegram_id': user_id})

        if customer:
            end_date_str = customer.get('end_date')
            if end_date_str:
                end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d %H:%M:%S')
                if end_date >= datetime.datetime.now():
                    return True  # Mensualidad activa
                else:
                    return False  # Mensualidad expirada
            else:
                return False  # No hay fecha de fin de mensualidad definida
        else:
            return False  # Usuario no encontrado en la base de datos

    except Exception as e:
        print(f"Error al verificar mensualidad activa: {str(e)}")
        return False

def verificar_creditos_suficientes(user_id, cantidad):
    try:
        # Obtener los datos del usuario desde la base de datos
        customer = customers_collection.find_one({'telegram_id': user_id})

        if customer:
            # Obtener la cantidad actual de créditos del usuario
            credits = customer.get('credits', 0)

            # Comparar con la cantidad deseada
            if credits >= cantidad:
                return True
            else:
                return False
        else:
            return False  # Usuario no encontrado en la base de datos

    except Exception as e:
        print(f"Error al verificar créditos: {str(e)}")
        return False

async def consumo_creditos(update: Update, context: CallbackContext, user_id: int, amount: int):
    try:
        data = {
            'user_id': user_id,
            'amount': amount
        }
        API_URL = "http://127.0.0.1:80/rest_credits"
        headers = {
            'Authorization': AUTH_TOKEN,
            'Content-Type': 'application/json'
        }

        response = requests.post(API_URL, json=data, headers=headers)

        if response.status_code == 200:
            pass
        else:
            pass

    except requests.RequestException:
        await update.message.reply_text("Error en la solicitud.")
    except Exception as e:
        await update.message.reply_text(f"Error.")

async def antepam(update: Update, context: CallbackContext) -> bool:
    user_id = update.effective_user.id
    
    customer = customers_collection.find_one({'telegram_id': user_id})

    if customer:
        antispam_time = customer.get('last_query_time', 0)
        current_time = int(time.time())

        time_elapsed = current_time - antispam_time

        if time_elapsed < customer['antispam']:
            await update.message.reply_text(f"Debes esperar {customer['antispam'] - time_elapsed} segundos antes de hacer otra consulta.")
            return False
        else:
            customers_collection.update_one({'telegram_id': user_id}, {'$set': {'last_query_time': current_time}})
            return True
    else:
        await update.message.reply_text("Usuario no encontrado.")
        return False

async def update_last_query_time(user_id: int):
    API_URL = "http://127.0.0.1:80/update_last_query_time"
    headers = {
        'Authorization': AUTH_TOKEN,
        'Content-Type': 'application/json'
    }
    data = {
        'telegram_id': user_id
    }
    try:
        response = requests.post(API_URL, json=data, headers=headers)
        if response.status_code != 200:
            print("Error al actualizar el tiempo de la última consulta.")
    except Exception as e:
        print(f"Error: {e}")

async def increment_queries(user_id: int):
    API_URL = "http://127.0.0.1:80/increment_queries"
    headers = {
        'Authorization': AUTH_TOKEN,
        'Content-Type': 'application/json'
    }
    data = {
        'telegram_id': user_id
    }
    try:
        response = requests.post(API_URL, json=data, headers=headers)
        if response.status_code != 200:
            print("Error al incrementar el conteo de consultas.")
    except Exception as e:
        print(f"Error: {e}")

async def add_seller(update: Update, context: CallbackContext):
    # Información del usuario administrador que envía el comando
    user_adm_id = update.effective_user.id
    user_adm_username = update.effective_user.username if update.effective_user.username else "Sin username"
    # Verificar el rol del usuario administrador
    customer = customers_collection.find_one({'telegram_id': user_adm_id})
    if not customer or customer['role'] not in ['OWNER']:
        return
    try:
        args = context.args
        if len(args) != 1:
            await update.message.reply_text("Uso incorrecto del comando. Ejemplo: /add_seller {id}")
            return
        
        user_id = int(args[0])

        try:
            chat_member = await context.bot.get_chat_member(chat_id=user_id, user_id=user_id)
            user_rec_username = chat_member.user.username if chat_member.user.username else "Sin username"
        except Exception as e:
            await update.message.reply_text(f"No se pudo obtener el username para el ID {user_id}.")
            return
        
        data = {
            'telegram_id': user_id,
        }

        API_URL = "http://127.0.0.1:80/add_seller"
        headers = {
            'Authorization': AUTH_TOKEN,
            'Content-Type': 'application/json'
        }

        response = requests.post(API_URL, json=data, headers=headers)

        if response.status_code == 200:
            mensajito = f"Rol del usuario [{user_adm_username}](tg://user?id={user_adm_id}) actualizado correctamente a Seller."
            await update.message.reply_text(mensajito, parse_mode='Markdown')
            mensaje = (
                f"ENVIADO POR: [{user_adm_username}](tg://user?id={user_adm_id}) - {user_adm_id}\n"
                f"ROL: SELLER\n"
                f"RECIBIDO POR: [{user_rec_username}](tg://user?id={user_id}) - {user_id}\n"
            )
            enviar_mensaje_telegram(mensaje) 
        else:
            await update.message.reply_text(f"No se encontró al usuario {user_id} o hubo un error.")

    except ValueError:
        await update.message.reply_text("ID deben ser dígitos enteros.")
    except requests.RequestException:
        await update.message.reply_text("Error en la solicitud.")
    except Exception as e:
        await update.message.reply_text(f"Error.")

async def remove_seller(update: Update, context: CallbackContext):
    # Información del usuario administrador que envía el comando
    user_adm_id = update.effective_user.id
    user_adm_username = update.effective_user.username if update.effective_user.username else "Sin username"
    # Verificar el rol del usuario administrador
    customer = customers_collection.find_one({'telegram_id': user_adm_id})
    if not customer or customer['role'] not in ['OWNER']:
        return
    try:
        args = context.args
        if len(args) != 1:
            await update.message.reply_text("Uso incorrecto del comando. Ejemplo: /rem_seller {id}")
            return
        
        user_id = int(args[0])

        try:
            chat_member = await context.bot.get_chat_member(chat_id=user_id, user_id=user_id)
            user_rec_username = chat_member.user.username if chat_member.user.username else "Sin username"
        except Exception as e:
            await update.message.reply_text(f"No se pudo obtener el username para el ID {user_id}.")
            return
        
        data = {
            'telegram_id': user_id,
        }

        API_URL = "http://127.0.0.1:80/rem_seller"
        headers = {
            'Authorization': AUTH_TOKEN,
            'Content-Type': 'application/json'
        }

        response = requests.post(API_URL, json=data, headers=headers)

        if response.status_code == 200:
            mensajito = f"Rol del usuario [{user_rec_username}](tg://user?id={user_id}) actualizado correctamente a Cliente."
            await update.message.reply_text(mensajito, parse_mode='Markdown')
            mensaje = (
                f"ENVIADO POR: [{user_adm_username}](tg://user?id={user_adm_id}) - {user_adm_id}\n"
                f"ROL: CLIENTE\n"
                f"RECIBIDO POR: [{user_rec_username}](tg://user?id={user_id}) - {user_id}\n"
            )
            enviar_mensaje_telegram(mensaje) 
        else:
            await update.message.reply_text(f"No se encontró al usuario {user_id} o hubo un error.")

    except ValueError:
        await update.message.reply_text("ID deben ser dígitos enteros.")
    except requests.RequestException:
        await update.message.reply_text("Error en la solicitud.")
    except Exception as e:
        await update.message.reply_text(f"Error.")

async def anti_spam(update: Update, context: CallbackContext):
    user_adm_id = update.effective_user.id
    customer = customers_collection.find_one({'telegram_id': user_adm_id})
    if not customer or customer['role'] not in ['OWNER']:
        return
    try:
        args = context.args
        if len(args) != 2:
            await update.message.reply_text("Uso incorrecto del comando. Ejemplo: /anti_spam {id} {cantidad}")
            return
        
        user_id = int(args[0])
        amount = int(args[1])

        # Obtener el username del usuario receptor desde Telegram
        try:
            chat_member = await context.bot.get_chat_member(chat_id=user_id, user_id=user_id)
            user_rec_username = chat_member.user.username if chat_member.user.username else "Sin username"
        except Exception as e:
            await update.message.reply_text(f"No se pudo obtener el username para el ID {user_id}.")
            return

        data = {
            'user_id': user_id,
            'amount': amount
        }

        API_URL = "http://127.0.0.1:80/anti_spam"
        headers = {
            'Authorization': AUTH_TOKEN,
            'Content-Type': 'application/json'
        }

        response = requests.post(API_URL, json=data, headers=headers)

        if response.status_code == 200:
            mensajito = f"Se actualizó el anti-spam a {amount} segundos para el usuario [{user_rec_username}](tg://user?id={user_id})"
            await update.message.reply_text(mensajito, parse_mode='Markdown')
        else:
            await update.message.reply_text(f"No se encontró al usuario @{user_rec_username}.")

    except ValueError:
        await update.message.reply_text("ID y el anti-spam deben ser números enteros.")
    except requests.RequestException as e:
        await update.message.reply_text(f"Error en la solicitud.")
    except Exception as e:
        await update.message.reply_text(f"Error.")

async def reniecCompleto(update: Update, context):
    user_id = update.effective_user.id

    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)
    
    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 3
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    # Extraer el DNI del mensaje
    message_text = update.message.text
    if message_text.startswith('/dnif'):
        dni = message_text[len('/dnif'):].strip() 
    else:
        dni = message_text.strip()

    if not dni.isdigit() or len(dni) != 8:
        await update.message.reply_text("Por favor proporciona un DNI válido de 8 dígitos.")
        return
    
    try:
        result = consultar_reniec(dni)
        
        if result['success']:

            caption = (
                f"*[#PeruDox]* ➜ *RENIEC LVL 2*\n\n"
                f"*DNI:* `{result['nuDni'] + ' - ' + result['digitoVerificacion']}`\n"
                f"*NOMBRE:* `{result['nombre']}`\n"
                f"*APELLIDOS:* `{result['ape_paterno'] + ' ' + result['ape_materno']}`\n"
                f"*SEXO:* `{result['sexo']}`\n\n"
                f"[[📅]] ➜ *NACIMIENTO*\n\n"
                f"*FECHA DE NACIMIENTO:* `{result['feNacimiento']}`\n"
                f"*DEPARTAMENTO:* `{result['departamento']}`\n"
                f"*PROVINCIA:* `{result['provincia']}`\n"
                f"*DISTRITO:* `{result['distrito']}`\n\n"

                f"*ESTADO CIVIL:* `{result['estadoCivil']}`\n"
                f"*GRADO DE INSTRUCCIÓN:* `{result['gradoInstruccion']}`\n"
                f"*ESTATURA:* `{result['estatura']}`\n"
                f"*FECHA DE EMISIÓN:* `{result['feEmision']}`\n"
                f"*FECHA DE INSCRIPCIÓN:* `{result['feInscripcion']}`\n"
                f"*FECHA DE CADUCIDAD:* `{result['feCaducidad']}`\n"
                f"*PADRE:* `{result['nomPadre']}`\n"
                f"*MADRE:* `{result['nomMadre']}`\n"
                f"*Restricciones:* `{result['deRestriccion']}`\n\n"
                f"[[🏠]] ➜ *DIRECCIÓN*\n\n"
                f"*DEPARTAMENTO:* `{result['depaDireccion']}`\n"
                f"*PROVINCIA:* `{result['provDireccion']}`\n"
                f"*DISTRITO:* `{result['distDireccion']}`\n"
                f"*DIRECCIÓN:* `{result['desDireccion']}`\n\n"
                f"[[🔅]] ➜ *UBIGEO*\n\n"
                f"*UBIGEO RENIEC:* `{result['ubiReniec']}`\n"
                f"*UBIGEO INEI:* `{result['ubiInei']}`\n"
                f"*CÓDIGO POSTAL:* `{result['ubiCP']}`\n"
                # f"*Donación de Órganos:* `{result['donaOrganos']}`\n"
                
                
            )
            media = [
                InputMediaPhoto(BytesIO(result['foto_bytes']), caption=caption, parse_mode='Markdown'),
                InputMediaPhoto(BytesIO(result['firma_bytes'])),
                InputMediaPhoto(BytesIO(result['hderecha_bytes'])),
                InputMediaPhoto(BytesIO(result['hizquierda_bytes']))
            ]
            
            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
            await context.bot.send_media_group(chat_id=update.message.chat_id, media=media)

        else:
            await update.message.reply_text(f"Error:")

    except ValueError:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /dnif 12345678")
    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error")

async def reniecBasico(update: Update, context):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 2
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return


    # Extraer el DNI del mensaje
    message_text = update.message.text
    if message_text.startswith('/dni'):
        dni = message_text[len('/dni'):].strip() 
    else:
        dni = message_text.strip()
    
    if not dni.isdigit() or len(dni) != 8:
        await update.message.reply_text("Por favor proporciona un DNI válido de 8 dígitos.")
        return
    
    try:
        result = consultar_reniec_una_foto(dni)
        
        if result['success']:

            caption = (
                f"*[#PeruDox]* ➜ *RENIEC LVL 1*\n\n"
                f"*DNI:* `{result['nuDni'] + ' - ' + result['digitoVerificacion']}`\n"
                f"*NOMBRE:* `{result['nombre']}`\n"
                f"*APELLIDOS:* `{result['ape_paterno'] + ' ' + result['ape_materno']}`\n"
                f"*SEXO:* `{result['sexo']}`\n\n"
                f"[[📅]] ➜ *NACIMIENTO*\n\n"
                f"*FECHA DE NACIMIENTO:* `{result['feNacimiento']}`\n"
                f"*DEPARTAMENTO:* `{result['departamento']}`\n"
                f"*PROVINCIA:* `{result['provincia']}`\n"
                f"*DISTRITO:* `{result['distrito']}`\n\n"

                f"*ESTADO CIVIL:* `{result['estadoCivil']}`\n"
                f"*FECHA DE EMISIÓN:* `{result['feEmision']}`\n"
                f"*FECHA DE INSCRIPCIÓN:* `{result['feInscripcion']}`\n"
                f"*FECHA DE CADUCIDAD:* `{result['feCaducidad']}`\n"
                f"*PADRE:* `{result['nomPadre']}`\n"
                f"*MADRE:* `{result['nomMadre']}`\n"
                f"*Restricciones:* `{result['deRestriccion']}`\n\n"
                f"[[🏠]] ➜ *DIRECCIÓN*\n\n"
                f"*DEPARTAMENTO:* `{result['depaDireccion']}`\n"
                f"*PROVINCIA:* `{result['provDireccion']}`\n"
                f"*DISTRITO:* `{result['distDireccion']}`\n"
                f"*DIRECCIÓN:* `{result['desDireccion']}`\n\n"
                f"[[🔅]] ➜ *UBIGEO*\n\n"
                f"*UBIGEO RENIEC:* `{result['ubiReniec']}`\n"
                f"*UBIGEO INEI:* `{result['ubiInei']}`\n"
                f"*CÓDIGO POSTAL:* `{result['ubiCP']}`\n"
                
                
            )
            media = [
                InputMediaPhoto(BytesIO(result['foto_bytes']), caption=caption, parse_mode='Markdown'),
            ]
            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
            await context.bot.send_media_group(chat_id=update.message.chat_id, media=media)

        else:
            await update.message.reply_text(f"Error:")

    except ValueError:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /dni 12345678")
    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error")

async def dniBasico(update: Update, context): 
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)


    # Extraer el DNI del mensaje
    message_text = update.message.text
    if message_text.startswith('/dnix'):
        dni = message_text[len('/dnix'):].strip() 
    else:
        dni = message_text.strip()

    if not dni.isdigit() or len(dni) != 8:
        await update.message.reply_text("Por favor proporciona un DNI válido de 8 dígitos.")
        return
    
    try:
        result = dniBasicoTexto(dni)

        if result['success']:
            data = result['data']
            caption = (
                f"*[#PeruDox]* ➜ *DNI BÁSICO*\n\n"
                f"*DNI:* `{data['nuDni']}`\n"
                f"*Nombre:* `{data['preNombres']}`\n"
                f"*Apellido Paterno:* `{data['apePaterno']}`\n"
                f"*Apellido Materno:* `{data['apeMaterno']}`\n"
                f"*Sexo:* `{data['sexo']}`\n"
                f"*Fecha de Nacimiento:* `{data['feNacimiento']}`\n"
                f"*Departamento:* `{data['departamento']}`\n"
                f"*Provincia:* `{data['provincia']}`\n"
                f"*Distrito:* `{data['distrito']}`\n"
                f"*Dirección:* `{data['desDireccion']}`\n"
                f"*Estado Civil:* `{data['estadoCivil']}`\n"
                f"*Nombre del Padre:* `{data['nomPadre']}`\n"
                f"*Nombre de la Madre:* `{data['nomMadre']}`\n"
                f"*Ubicación Reniec:* `{data['ubiReniec']}`\n"
            )
            await context.bot.send_message(chat_id=update.message.chat_id, text=caption, parse_mode='Markdown')

        else:
            await update.message.reply_text(f"No se pudo encontrar información.")

    except ValueError:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /dnix 12345678")
    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error")

async def nombre(update: Update, context):
    message_text = update.message.text
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    parts = message_text[len('/nm'):].strip().split('|')
    
    if len(parts) < 6:
        await update.message.reply_text(
            "Por favor proporciona los parámetros necesarios después del comando. Ejemplo: /nm LISMELI|ROMAINA|SILVA|36|34|HUANUCO"
        )
        return

    name, first_name, last_name, max_age, min_age, depa = [part.strip() for part in parts]

    try:
        resultado = consultar_nombre(name, first_name, last_name, max_age, min_age, depa)

        if resultado and 'listaAni' in resultado:
            personas = resultado['listaAni']

            if not personas:
                mensaje = "No se encontró ninguna persona con los criterios proporcionados."
                await update.message.reply_text(mensaje)
                return

            for persona in personas:
                mensaje = (
                    f"*[#PeruDox]* ➜ *CONSULTA POR NOMBRE*\n\n"
                    f"*DNI:* `{persona.get('nuDni', '')}`\n"
                    f"*Nombres:* `{persona.get('preNombres', '')} {persona.get('apePaterno', '')} {persona.get('apeMaterno', '')}`\n"
                    f"*Sexo:* `{persona.get('sexo', '')}`\n"
                    f"*Edad:* `{persona.get('nuEdad', '')}`\n"
                )
                await update.message.reply_text(mensaje, parse_mode='Markdown')
            await increment_queries(user_id)
        else:
            mensaje = "No se encontraron resultados para la consulta por nombre."
            await update.message.reply_text(mensaje)

    except Exception as e:
        await update.message.reply_text("Ha ocurrido un error al realizar la consulta por nombre.")

async def hogar(update: Update, context):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 3
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    # Extraer el DNI del mensaje
    message_text = update.message.text
    if message_text.startswith('/hogar'):
        dni = message_text[len('/hogar'):].strip() 
    else:
        dni = message_text.strip()

    if not dni.isdigit() or len(dni) != 8:
        await update.message.reply_text("Por favor proporciona un DNI válido de 8 dígitos.")
        return
    
    try:
        result = consultaHogar(dni)

        if result['success']:
            data = result['data']
            identificacion = data.get('identificacion', {})
            empadronamiento = data.get('empadronamiento', {})
            socioeconomico = data.get('socioeconomico', {})
            integrantes = data.get('integrantes', [])

            caption = (
                f"*[#PeruDox]* ➜ *HOGAR*\n\n"
                f"*Hogar ID:* `{identificacion.get('hogarID', '')}`\n"
                f"*Estado:* `{identificacion.get('hogarEstado', '')}`\n"
                f"*Fecha Empadronamiento:* `{identificacion.get('fechaEmpadronamiento', '')}`\n\n"
                f"[📍] EMPADRONAMIENTO:\n"
                f"*Departamento:* `{empadronamiento.get('departamento', '')}`\n"
                f"*Provincia:* `{empadronamiento.get('provincia', '')}`\n"
                f"*Distrito:* `{empadronamiento.get('distrito', '')}`\n"
                f"*Ubigeo:* `{empadronamiento.get('ubigeo', '')}`\n"
                f"*Centro Poblado:* `{empadronamiento.get('centroPoblado', '')}`\n"
                f"*Dirección:* `{empadronamiento.get('direccion', '')}`\n"
                f"*Referencia:* `{empadronamiento.get('referencia', '')}`\n"
                f"*Tipo de Carga:* `{empadronamiento.get('tipoCarga', '')}`\n\n"
                f"[💰] SOCIOECONÓMICO:\n"
                f"*Fecha Inicial:* `{socioeconomico.get('fechaInicial', '')}`\n"
                f"*Fecha Vigencia:* `{socioeconomico.get('fechaVigencia', '')}`\n"
                f"*Estado Vigencia:* `{socioeconomico.get('estadoVigencia', '')}`\n"
                f"*Clasificación:* `{socioeconomico.get('clasificacion', '')}`\n"
                f"*Área:* `{socioeconomico.get('area', '')}`\n"
                f"*Nro Formato:* `{socioeconomico.get('nroFormato', '')}`\n\n"
                f"[👨‍👩‍👦‍👦] INTEGRANTES:\n"
            )

            for integrante in integrantes:
                caption += (
                    f"*DNI:* `{integrante['dni']}`\n"
                    f"*Nombre:* `{integrante['nombres']}` `{integrante['apellidoP']}` `{integrante['apellidoM']}`\n"
                    f"*Sexo:* `{integrante['sexo']}`\n"
                    f"*Parentesco:* `{integrante['parentesco']}`\n"
                    f"*Fecha de Nacimiento:* `{integrante['nacimiento']}`\n\n"
                )
            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
            await context.bot.send_message(chat_id=update.message.chat_id, text=caption, parse_mode='Markdown')

        else:
            await update.message.reply_text(f"{result['mensaje_error']}")

    except ValueError:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /hog 12345678")
    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error")

async def predios(update: Update, context):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 2
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    message_text = update.message.text
    if message_text.startswith('/pred'):
        message_text = message_text[len('/pred'):].strip() 
    dni = message_text.strip()
    if not dni.isdigit() or len(dni) != 8:
        await update.message.reply_text("Por favor proporciona un DNI válido de 8 dígitos.")
        return
    
    try:
        result = consultar_predios(dni)

        if result['success']:
            data = result['data']
            caption = (
                f"*[#PeruDox]* ➜ *PREDIOS*\n\n"
                f"*DNI:* `{data['numeroDocumento']}`\n"
                f"*Nombre:* `{data['nombres']}`\n"
                f"*Apellido Paterno:* `{data['apPaterno']}`\n"
                f"*Apellido Materno:* `{data['apMaterno']}`\n"
                f"*Registro:* `{data['registro']}`\n"
                f"*Razón social:* `{data['razonSocial']}`\n"
                f"*Tipo de documento:* `{data['tipoDocumento']}`\n"
                f"*Libro:* `{data['libro']}`\n"
                f"*Número de partida:* `{data['numeroPartida']}`\n"
                f"*Número de Placa:* `{data['numeroPlaca']}`\n"
                f"*Estado:* `{data['estado']}`\n"
                f"*Zona:* `{data['zona']}`\n"
                f"*Oficina:* `{data['oficina']}`\n"
            )
            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
            await context.bot.send_message(chat_id=update.message.chat_id, text=caption, parse_mode='Markdown')

        else:
            await update.message.reply_text(f"Error{result['mensaje_error']}")

    except ValueError:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /pred 12345678")
    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error")

async def tel(update: Update, context):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 4
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return
    # Extraer el DNI del mensaje
    message_text = update.message.text
    if message_text.startswith('/tel'):
        dni = message_text[len('/tel'):].strip() 
    else:
        dni = message_text.strip()

    try:
        result = consultar_numeros(dni)

        if result['success']:
            data = result['data']
            numbers = data['numbers']
            caption = (
                f"*[#PeruDox]* ➜ *TELÉFONOS*\n\n"
                f"*DNI:* `{data['dni']}`\n"
                f"*Titular:* `{data['name'] +' '+ data['surname']}`\n\n"
                
            )

            for number in numbers:
                caption += (
                    f"*NÚMERO:* `{number['number']}`\n"
                    f"*OPERADOR:* `{number['operator']}`\n"
                    f"*PLAN:* `{number['plan']}`\n\n"
                )
            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
            await update.message.reply_text(caption, parse_mode='Markdown')

        else:
            await update.message.reply_text(f"Error al consultar:")

    except ValueError:
        await update.message.reply_text("Por favor proporciona un DNI o número después del comando. Ejemplo: /tel 12345678.")
    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error")

async def familiares(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 3
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    # Extraer el DNI del mensaje
    message_text = update.message.text
    if message_text.startswith('/fam'):
        dni = message_text[len('/fam'):].strip() 
    else:
        dni = message_text.strip()
    if not dni.isdigit() or len(dni) != 8:
        await update.message.reply_text("Por favor proporciona un DNI válido de 8 dígitos.")
        return
    
    if not dni:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /fam 12345678")
        return

    try:
        resultado = consultar_familiares(dni)

        if resultado['success']:
            familiares = resultado['familiares']
            mensaje = (
                f"*[#PeruDox]* ➜ *FAMILIARES*\n\n"
            )
            for familiar in familiares:
                mensaje += (
                    
                    f"*DNI:* `{familiar['nuDni'] + '-' + familiar['digitoVerificacion']}`\n"
                    f"*Nombre:* `{familiar['preNombres']} {familiar['apePaterno']} {familiar['apeMaterno']}`\n"
                    f"*Sexo:* `{familiar['sexo']}`\n"
                    f"*Edad:* `{familiar['nuEdad']}`\n"
                    f"*Tipo:* `{familiar['tipo']}`\n"
                    f"*Verificación:* `{familiar['verificacion']}`\n\n"
                )
            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
        else:
            mensaje = f"Error al consultar familiares: {resultado['mensaje_error']}"

        await update.message.reply_text(mensaje, parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error")

async def arbol(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 6
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return
    
    # Extraer el DNI del mensaje
    message_text = update.message.text
    if message_text.startswith('/arb'):
        dni = message_text[len('/arb'):].strip() 
    else:
        dni = message_text.strip()

    if not dni.isdigit() or len(dni) != 8:
        await update.message.reply_text("Por favor proporciona un DNI válido de 8 dígitos.")
        return
    
    if not dni:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /arb 12345678")
        return

    try:
        resultado = consultar_arbol(dni)

        if resultado['success']:
            familiares = resultado['familiares']
            mensaje = "*[#PeruDox]* ➜ *ÁRBOL GENEALÓGICO*\n\n"  # Inicializar la variable mensaje
            for familiar in familiares:
                mensaje += (
                    f"**DNI:** `{familiar['nuDni'] + '-' + familiar['digitoVerificacion']}`\n"
                    f"**Nombre:** `{familiar['preNombres']} {familiar['apePaterno']} {familiar['apeMaterno']}`\n"
                    f"**Sexo:** `{familiar['sexo']}`\n"
                    f"**Edad:** `{familiar['nuEdad']}`\n"
                    f"**Tipo:** `{familiar['tipo']}`\n"
                    f"**Verificación:** `{familiar['verificacion']}`\n\n"
                )
            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
        else:
            mensaje = f"Error al consultar el árbol familiar"

        await update.message.reply_text(mensaje, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error")

async def hermanos(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 2
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    # Extraer el DNI del mensaje
    message_text = update.message.text
    if message_text.startswith('/herm'):
        dni = message_text[len('/herm'):].strip() 
    else:
        dni = message_text.strip()

    if not dni.isdigit() or len(dni) != 8:
        await update.message.reply_text("Por favor proporciona un DNI válido de 8 dígitos.")
        return
    
    if not dni:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /hermanos 12345678")
        return

    try:
        resultado = consultar_hermanos(dni)

        if resultado['success']:
            hermanos = resultado['hermanos']
            mensaje = "*[#PeruDox]* ➜ *HERMANOS*\n\n"  # Inicializar la variable mensaje
            for hermano in hermanos:
                mensaje += (
                    f"**DNI:** `{hermano['nuDni'] + '-' + hermano['digitoVerificacion']}`\n"
                    f"**Nombre:** `{hermano['preNombres']} {hermano['apePaterno']} {hermano['apeMaterno']}`\n"
                    f"**Sexo:** `{hermano['sexo']}`\n"
                    f"**Edad:** `{hermano['nuEdad']}`\n"
                    f"**Tipo:** `{hermano['tipo']}`\n"
                    f"**Verificación:** `{hermano['verificacion']}`\n\n"
                )
            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
        else:
            mensaje = f"Error al consultar hermanos: {resultado['mensaje_error']}"

        await update.message.reply_text(mensaje, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error")

async def bitel(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 2
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    # Extraer el DNI del mensaje
    message_text = update.message.text
    if message_text.startswith('/bitel'):
        dni = message_text[len('/bitel'):].strip() 
    else:
        dni = message_text.strip()

    if not dni:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /bitel 12345678")
        return

    try:
        resultado = consultar_bitel(dni)

        if resultado['success']:
            bitel_info = resultado['bitel']
            mensaje = "*[#PeruDox]* ➜ *BITEL*\n\n"  # Inicializar la variable mensaje
            for info in bitel_info:
                mensaje += (
                    f"**Número:** `{info['number']}`\n"
                    f"**DNI:** `{info['dni']}`\n"
                    f"**Nombre:** `{info['name']}`\n"
                    f"**Apellido:** `{info['surname']}`\n\n"
                )
            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
        else:
            mensaje = f"Error al consultar Bitel: {resultado['mensaje_error']}"

        await update.message.reply_text(mensaje, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error")

async def claro(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 2
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    # Extraer el DNI del mensaje
    message_text = update.message.text
    if message_text.startswith('/claro'):
        dni = message_text[len('/claro'):].strip() 
    else:
        dni = message_text.strip()

    if not dni:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /claro 12345678")
        return

    try:
        resultado = consultar_claro(dni)

        if resultado['success']:
            claro_info = resultado['claro']
            mensaje = "*[#PeruDox]* ➜ *CLARO*\n\n"  # Inicializar la variable mensaje
            for info in claro_info:
                mensaje += (
                    f"**Celular:** `{info['celular']}`\n"
                    f"**DNI:** `{info['numDoc']}`\n"
                    f"**Nombre:** `{info['nombres']}`\n"
                    f"**Apellidos:** `{info['apellidos']}`\n"
                    f"**Correo:** `{info['correo']}`\n"
                    f"**Customer ID:** `{info['customerId']}`\n"
                    f"**Razón Social:** `{info['razonSocial']}`\n\n"
                )
            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
        else:
            mensaje = f"Error al consultar Claro: {resultado['mensaje_error']}"

        await update.message.reply_text(mensaje, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error")

async def placas(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 5
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    # Extraer el DNI del mensaje
    message_text = update.message.text
    if message_text.startswith('/placas'):
        dni = message_text[len('/placas'):].strip() 
    else:
        dni = message_text.strip()

    if len(dni) != 6:
        await update.message.reply_text("Por favor proporciona una placa válida.")
        return
    
    if not dni:
        await update.message.reply_text("Por favor proporciona una placa después del comando. Ejemplo: /placas RM1514")
        return

    try:
        resultado = consultar_placas(dni)

        if resultado['success']:
            placa_info = resultado['placa']
            mensaje = "*[#PeruDox]* ➜ *INFORMACIÓN DE PLACA*\n\n"  # Inicializar la variable mensaje
            mensaje += (
                f"**Número de Placa:** `{placa_info['numPlaca']}`\n"
                f"**Número de Partida:** `{placa_info['numPartida']}`\n"
                f"**Oficina:** `{placa_info['nomOficina']}`\n"
                f"**Año de Fabricación:** `{placa_info['anMode']}`\n"
                f"**Fecha de Inscripción:** `{placa_info['fecIns']}`\n"
                f"**Descripción Tipo de Carrocería:** `{placa_info['descTipoCarr']}`\n"
                f"**Marca:** `{placa_info['marca']}`\n"
                f"**Modelo:** `{placa_info['modelo']}`\n"
                f"**Año de Fabricación:** `{placa_info['anoFab']}`\n"
                f"**Descripción Tipo de Combustible:** `{placa_info['descTipoComb']}`\n"
                f"**Número de Cilindros:** `{placa_info['numCilindros']}`\n"
                f"**Color:** `{placa_info['color']}`\n"
                f"**Número de Motor:** `{placa_info['numMotor']}`\n"
                f"**Número de Serie:** `{placa_info['numSerie']}`\n"
                f"**Número VIN:** `{placa_info['noVin']}`\n"
                f"**Descripción Tipo de Uso:** `{placa_info['descTipoUso']}`\n"
                f"**Categoría:** `{placa_info['coCateg']}`\n"
                f"**Número de Ruedas:** `{placa_info['numRuedas']}`\n"
                f"**Número de Pasajeros:** `{placa_info['numPasajeros']}`\n"
                f"**Número de Asientos:** `{placa_info['numAsientos']}`\n"
                f"**Peso Seco:** `{placa_info['pesoSeco']}`\n"
                f"**Peso Util:** `{placa_info['pesoUtil']}`\n"
                f"**Peso Bruto:** `{placa_info['pesoBruto']}`\n"
                f"**Longitud:** `{placa_info['longitud']}`\n"
                f"**Altura:** `{placa_info['altura']}`\n"
                f"**Ancho:** `{placa_info['ancho']}`\n"
                f"**Potencia del Motor:** `{placa_info['poMotr']}`\n"
                f"**Estado:** `{placa_info['estado']}`\n"
                f"**Número de Ejes:** `{placa_info['ejes']}`\n\n"
                f"**Propietarios:**\n"
            )

            for propietario in placa_info['LPropietario']:
                mensaje += (
                    f"  - **Nombre:** `{propietario['NombrePropietario']}`\n"
                    f"    **Documento:** `{propietario['NroDocumento']}`\n"
                    f"    **Dirección:** `{propietario['Direccion']}`\n"
                    f"    **Fecha de Propiedad:** `{propietario['FechaPropiedad']}`\n\n"
                )
            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
        else:
            mensaje = f"No se encontró información de la placa para el DNI {dni}"

        await update.message.reply_text(mensaje, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error")

async def sunarp(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 3
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    # Extraer el DNI del mensaje
    message_text = update.message.text
    if message_text.startswith('/sunarp'):
        dni = message_text[len('/sunarp'):].strip() 
    else:
        dni = message_text.strip()

    if len(dni) != 6:
        await update.message.reply_text("Por favor proporciona una placa válida.")
        return
    
    if not dni:
        await update.message.reply_text("Por favor proporciona una placa después del comando. Ejemplo: /sunarp RM1514")
        return

    try:
        resultado = consultar_sunarp(dni)

        if resultado['success']:
            caption = (
                f"*[#PeruDox]* ➜ *SUNARP*\n\n"
                f"*Sunarp generada satisfactoriamente*\n"
            )
            foto_bytes = resultado['foto_bytes']
            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
            await context.bot.send_photo(update.message.chat_id, photo=foto_bytes, caption=caption, parse_mode='Markdown')
        else:
            await update.message.reply_text(f"No se encontró información de Sunarp para la placa {dni}")

    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error")

async def correo(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 2
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    # Extraer el DNI del mensaje
    message_text = update.message.text
    if message_text.startswith('/correo'):
        dni = message_text[len('/correo'):].strip() 
    else:
        dni = message_text.strip()

    if not dni.isdigit() or len(dni) != 8:
        await update.message.reply_text("Por favor proporciona un DNI válido de 8 dígitos.")
        return
    
    if not dni:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /correos 12345678")
        return

    try:
        resultado = consultar_correo(dni)

        if resultado['success']:
            correos_info = resultado['correos']
            mensaje = "*[#PeruDox]* ➜ *CORREOS*\n\n"  # Inicializar la variable mensaje
            for correo in correos_info:
                mensaje += (
                    f"*DNI:* `{correo['dni']}`\n"
                    f"*CORREO:* `{correo['correo']}`\n\n"
                )
            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
        else:
            mensaje = f"No se encontraron correos para el DNI {dni}"

        await update.message.reply_text(mensaje, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error")

async def sueldos(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 2
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    # Extraer el DNI del mensaje
    message_text = update.message.text
    if message_text.startswith('/sueldos'):
        dni = message_text[len('/sueldos'):].strip() 
    else:
        dni = message_text.strip()

    if not dni.isdigit() or len(dni) != 8:
        await update.message.reply_text("Por favor proporciona un DNI válido de 8 dígitos.")
        return
    
    if not dni:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /sueldos 12345678")
        return

    try:
        resultado = consultar_sueldos(dni)

        if resultado['success']:
            sueldos_info = resultado['sueldos']
            mensaje = "*[#PeruDox]* ➜ *SUELDOS*\n\n"  # Inicializar la variable mensaje
            for sueldo in sueldos_info:
                mensaje += (
                    f"*DNI:* `{sueldo['nuDni']}`\n"
                    f"*Nombre:* `{sueldo['nombres']} {sueldo['apellidos']}`\n"
                    f"*Empresa:* `{sueldo['empresa']}`\n"
                    f"*Fecha:* `{sueldo['fecha']}`\n"
                    f"*Sueldo:* `{sueldo['sueldo']}`\n\n"
                )
            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
        else:
            mensaje = f"No se encontró información de sueldos para el DNI {dni}"

        await update.message.reply_text(mensaje, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"No se pudo encontrar sueldos para {dni}")

async def sbs(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 10
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    # Extraer el DNI del mensaje
    message_text = update.message.text
    if message_text.startswith('/sbs'):
        dni = message_text[len('/sbs'):].strip() 
    else:
        dni = message_text.strip()

    if not dni.isdigit() or len(dni) != 8:
        await update.message.reply_text("Por favor proporciona un DNI válido de 8 dígitos.")
        return
    
    if not dni:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /sbs 12345678")
        return

    try:
        resultado = consultar_sbs(dni)

        if resultado['success']:
            sbs_info = resultado['sbs_info']
            mensaje = "*[#PeruDox]* ➜ *SBS*\n\n"  # Inicializar la variable mensaje
            for info in sbs_info:
                mensaje += (
                    f"*Entidad:* `{info['entidad']}`\n"
                    f"*Tipo de cuenta:* `{info['tipocuenta']}`\n"
                    f"*Descripción:* `{info['descripcion']}`\n"
                    f"*Saldo:* ` {info['moneda']} {info['saldo']}`\n\n"
                )
            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
        else:
            mensaje = f"No se encontró información de SBS para el DNI {dni}"

        await update.message.reply_text(mensaje, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error")

async def geo(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 1
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    # Extraer el DNI del mensaje
    message_text = update.message.text
    if message_text.startswith('/ip'):
        ip = message_text[len('/ip'):].strip() 
    else:
        ip = message_text.strip()

    if not ip:
        await update.message.reply_text("Por favor proporciona una IP después del comando. Ejemplo: /geo 138.197.126.79")
        return

    try:
        resultado = consultar_geo(ip)

        if resultado['success']:
            geo_info = resultado['geo_info']
            mensaje = "*[#PeruDox]* ➜ *GEOLOCALIZACIÓN*\n\n"  # Inicializar la variable mensaje
            mensaje += (
                f"*IP:* `{geo_info['ip']}`\n"
                f"*Operador:* `{geo_info['operator']}`\n"
                f"*País:* `{geo_info['country']}`\n"
                f"*Región:* `{geo_info['region']}`\n"
                f"*Ciudad:* `{geo_info['city']}`\n"
            )
            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
        else:
            mensaje = f"No se encontró información de la IP {ip}"

        await update.message.reply_text(mensaje, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error")

async def ruc(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 5
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    # Extraer el DNI del mensaje
    message_text = update.message.text
    if message_text.startswith('/ruc'):
        ruc_number = message_text[len('/ruc'):].strip() 
    else:
        ruc_number = message_text.strip()

    if not ruc_number:
        await update.message.reply_text("Por favor proporciona un número de RUC después del comando. Ejemplo: /ruc 20486484013")
        return

    try:
        resultado = consultar_ruc(ruc_number)

        if resultado['success']:
            data = resultado['data']
            establecimientos = data.get('establecimiento', [])
            
            if not establecimientos:
                mensaje = f"No se encontraron establecimientos asociados al RUC {ruc_number}."
                await update.message.reply_text(mensaje, parse_mode='Markdown')
                return
            
            mensaje_inicial = "*[#PeruDox]* ➜ *ESTABLECIMIENTOS ASOCIADOS*\n\n"
            mensajes = [mensaje_inicial]
            mensaje_actual = mensaje_inicial

            for est in establecimientos:
                est_info = (
                    f"*Dirección:* `{est.get('direccion', '')}`\n"
                    f"*Tipo de establecimiento:* `{est.get('desc_tipest', '')}`\n"
                    f"*Tipo de vía:* `{est.get('desc_tipvia', '')}`\n"
                    f"*Distrito:* `{est.get('desc_dist', '')}`\n"
                    f"*Provincia:* `{est.get('desc_prov', '')}`\n"
                    f"*Departamento:* `{est.get('desc_dep', '')}`\n\n"
                )
                if len(mensaje_actual) + len(est_info) > 4000:  # 4000 es un valor seguro por debajo del límite de Telegram
                    mensajes.append(mensaje_actual)
                    mensaje_actual = mensaje_inicial + est_info
                else:
                    mensaje_actual += est_info

            mensajes.append(mensaje_actual)  # Agregar el último mensaje

            for mensaje in mensajes:
                await update.message.reply_text(mensaje, parse_mode='Markdown')
            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
        else:
            mensaje = f"No se pudo encontrar información del RUC {ruc_number}."
            await update.message.reply_text(mensaje, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error")

async def sunedu(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 5
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    # Extraer el DNI del mensaje
    message_text = update.message.text
    if message_text.startswith('/sunedu'):
        dni = message_text[len('/sunedu'):].strip() 
    else:
        dni = message_text.strip()

    if not dni.isdigit() or len(dni) != 8:
        await update.message.reply_text("Por favor proporciona un DNI válido de 8 dígitos.")
        return
    
    if not dni:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /sunedu 70194468")
        return

    try:
        resultado = consultar_sunedu(dni)

        if resultado['success']:
            mensaje = resultado['mensaje']
            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
        else:
            mensaje = f"No se encontró información académica para el DNI {dni}"

        await update.message.reply_text(mensaje, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error")

async def telefonox(update: Update, context: CallbackContext):

    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)
   
    # Extraer el DNI del mensaje
    message_text = update.message.text
    if message_text.startswith('/telx'):
        dni = message_text[len('/telx'):].strip() 
    else:
        dni = message_text.strip()
    

    if not dni.isdigit() or len(dni) != 8:
        await update.message.reply_text("Por favor proporciona un DNI válido de 8 dígitos.")
        return
    
    if not dni:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /telx 44443333")
        return

    try:
        resultado = verificar_numeros(dni)

        if resultado['success']:
            mensaje = resultado['mensaje']
            await increment_queries(user_id)
        else:
            mensaje = f"No se encontró números en OSIPTEL para el DNI {dni}"
        
        await update.message.reply_text(mensaje, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error")

async def dniv(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 5
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    message_text = update.message.text
    if message_text.startswith('/dniv'):
        dni = message_text[len('/dniv'):].strip() 
    else:
        dni = message_text.strip()

    if not dni.isdigit() or len(dni) != 8:
        await update.message.reply_text("Por favor proporciona un DNI válido de 8 dígitos.")
        return
    
    if not dni:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /dniv 00000001")
        return

    try:
        # Obtener resultado del API
        resultado = obtener_dni_virtual(dni)

        if resultado['success']:
            # Prepare the document caption with detailed description
            document_caption = (
                f"*[#PeruDox]* ➜ *DNI VIRTUAL*\n\n"
                f"*Número de DNI:* `{dni}`\n"
                f"*Edad:* `{resultado['listaAni']['nuEdad']}`\n"
                f"*Nombre Completo:* `{resultado['listaAni']['preNombres']} {resultado['listaAni']['apePaterno']} {resultado['listaAni']['apeMaterno']}`\n"
                f"*Sexo:* `{resultado['listaAni']['sexo']}`\n"
                f"*Fecha de Nacimiento:* `{resultado['listaAni']['feNacimiento']}`\n\n"
            )

            # Send the images as a document
            media = [
                InputMediaPhoto(resultado['front_image']),
                InputMediaPhoto(resultado['back_image'])
            ]
            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
            await update.message.reply_media_group(media=media, caption=document_caption, parse_mode='Markdown')
        else:
            await update.message.reply_text(f"Error al obtener el DNI virtual")

    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error")

async def dnie(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 5
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    message_text = update.message.text
    if message_text.startswith('/dnie'):
        dni = message_text[len('/dnie'):].strip() 
    else:
        dni = message_text.strip()

    if not dni.isdigit() or len(dni) != 8:
        await update.message.reply_text("Por favor proporciona un DNI válido de 8 dígitos.")
        return
    
    if not dni:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /dniv 00000001")
        return

    try:
        # Obtener resultado del API
        resultado = obtener_dni_electronico(dni)

        if resultado['success']:
            # Prepare the document caption with detailed description
            document_caption = (
                f"*[#PeruDox]* ➜ *DNI ELECTRÓNICO*\n\n"
                f"*Número de DNI:* `{dni}`\n"
                f"*Edad:* `{resultado['listaAni']['nuEdad']}`\n"
                f"*Nombre Completo:* `{resultado['listaAni']['preNombres']} {resultado['listaAni']['apePaterno']} {resultado['listaAni']['apeMaterno']}`\n"
                f"*Sexo:* `{resultado['listaAni']['sexo']}`\n"
                f"*Fecha de Nacimiento:* `{resultado['listaAni']['feNacimiento']}`\n\n"
            )

            # Send the images as a document
            media = [
                InputMediaPhoto(resultado['front_image']),
                InputMediaPhoto(resultado['back_image'])
            ]
            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
            await update.message.reply_media_group(media=media, caption=document_caption, parse_mode='Markdown')

        else:
            await update.message.reply_text(f"Error al obtener el DNI virtual")

    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error")

async def antjud(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 5
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    message_text = update.message.text
    if message_text.startswith('/antju'):
        dni = message_text[len('/antju'):].strip() 
    else:
        dni = message_text.strip()

    if not dni.isdigit() or len(dni) != 8:
        await update.message.reply_text("Por favor proporciona un DNI válido de 8 dígitos.")
        return
    
    if not dni:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /antju 00000001")
        return

    try:
        # Obtener resultado del API
        resultado = obtener_antecedentes_judiciales(dni)

        if resultado['success']:
            # Prepare the document caption with detailed description
            document_caption = (
                f"*[#PeruDox]* ➜ *ANTECEDENTES JUDICIALES*\n\n"
                f"*DNI:* `{dni}`\n"
                f"*NOMBRE:* {resultado['listaAni']['preNombres']} {resultado['listaAni']['apePaterno']} {resultado['listaAni']['apeMaterno']}\n"
                f"*Fecha de Nacimiento:* {resultado['listaAni']['feNacimiento']}\n\n"
                f"*Sexo:* {resultado['listaAni']['sexo']}\n"
                f"*Edad:* {resultado['listaAni']['nuEdad']}\n"
            )

            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
            await update.message.reply_document(document=resultado['pdf_bytes'], filename=f"{dni}_antecedentes_judiciales.pdf", caption=document_caption, parse_mode='Markdown')

        else:
            await update.message.reply_text(f"Error al obtener los antecedentes judiciales.")

    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error.")

async def antpol(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 5
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    message_text = update.message.text
    if message_text.startswith('/antpo'):
        dni = message_text[len('/antpo'):].strip() 
    else:
        dni = message_text.strip()

    if not dni.isdigit() or len(dni) != 8:
        await update.message.reply_text("Por favor proporciona un DNI válido de 8 dígitos.")
        return
    
    if not dni:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /antpo 00000001")
        return

    try:
        # Obtener resultado del API
        resultado = obtener_antecedentes_policiales(dni)

        if resultado['success']:
            # Prepare the document caption with detailed description
            document_caption = (
                f"*[#PeruDox]* ➜ *ANTECEDENTES POLICIALES*\n\n"
                f"*DNI:* `{dni}`\n"
                f"*NOMBRE:* {resultado['listaAni']['preNombres']} {resultado['listaAni']['apePaterno']} {resultado['listaAni']['apeMaterno']}\n"
                f"*Fecha de Nacimiento:* {resultado['listaAni']['feNacimiento']}\n\n"
                f"*Sexo:* {resultado['listaAni']['sexo']}\n"
                f"*Edad:* {resultado['listaAni']['nuEdad']}\n"
            )

            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
            await update.message.reply_document(document=resultado['pdf_bytes'], filename=f"{dni}_antecedentes_policiales.pdf", caption=document_caption, parse_mode='Markdown')

        else:
            await update.message.reply_text(f"Error al obtener los antecedentes policiales.")

    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error.")

async def antpen(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 5
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    message_text = update.message.text
    if message_text.startswith('/antpe'):
        dni = message_text[len('/antpe'):].strip() 
    else:
        dni = message_text.strip()

    if not dni.isdigit() or len(dni) != 8:
        await update.message.reply_text("Por favor proporciona un DNI válido de 8 dígitos.")
        return
    
    if not dni:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /antpe 00000001")
        return

    try:
        # Obtener resultado del API
        resultado = obtener_antecedentes_penales(dni)

        if resultado['success']:
            # Prepare the document caption with detailed description
            document_caption = (
                f"*[#PeruDox]* ➜ *ANTECEDENTES PENALES*\n\n"
                f"*DNI:* `{dni}`\n"
                f"*NOMBRE:* {resultado['listaAni']['preNombres']} {resultado['listaAni']['apePaterno']} {resultado['listaAni']['apeMaterno']}\n"
                f"*Fecha de Nacimiento:* {resultado['listaAni']['feNacimiento']}\n\n"
                f"*Sexo:* {resultado['listaAni']['sexo']}\n"
                f"*Edad:* {resultado['listaAni']['nuEdad']}\n"
            )

            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
            await update.message.reply_document(document=resultado['pdf_bytes'], filename=f"{dni}_antecedentes_penales.pdf", caption=document_caption, parse_mode='Markdown')

        else:
            await update.message.reply_text(f"Error al obtener los antecedentes penales.")

    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error.")

async def c4a(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 4
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    message_text = update.message.text
    if message_text.startswith('/c4a'):
        dni = message_text[len('/c4a'):].strip() 
    else:
        dni = message_text.strip()

    if not dni.isdigit() or len(dni) != 8:
        await update.message.reply_text("Por favor proporciona un DNI válido de 8 dígitos.")
        return
    
    if not dni:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /c4a 00000001")
        return

    try:
        # Obtener resultado del API
        resultado = obtener_c4_azul(dni)

        if resultado['success']:
            # Prepare the document caption with detailed description
            document_caption = (
                f"*[#PeruDox]* ➜ *C4 AZUL*\n\n"
                f"*DNI:* `{dni}`\n"
                f"*NOMBRE:* {resultado['listaAni']['preNombres']} {resultado['listaAni']['apePaterno']} {resultado['listaAni']['apeMaterno']}\n"
                f"*Fecha de Nacimiento:* {resultado['listaAni']['feNacimiento']}\n\n"
                f"*Sexo:* {resultado['listaAni']['sexo']}\n"
                f"*Edad:* {resultado['listaAni']['nuEdad']}\n"
            )

            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
            await update.message.reply_document(document=resultado['pdf_bytes'], filename=f"{dni}_C4_AZUL.pdf", caption=document_caption, parse_mode='Markdown')

        else:
            await update.message.reply_text(f"Error al obtener el c4")

    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error.")

async def c4b(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 4
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    message_text = update.message.text
    dni = message_text[len('/c4b'):].strip()

    if not dni.isdigit() or len(dni) != 8:
        await update.message.reply_text("Por favor proporciona un DNI válido de 8 dígitos.")
        return
    
    if not dni:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /c4b 00000001")
        return

    try:
        # Obtener resultado del API
        resultado = obtener_c4_blanco(dni)

        if resultado['success']:
            # Prepare the document caption with detailed description
            document_caption = (
                f"*[#PeruDox]* ➜ *C4 BLANCO*\n\n"
                f"*DNI:* `{dni}`\n"
                f"*NOMBRE:* {resultado['listaAni']['preNombres']} {resultado['listaAni']['apePaterno']} {resultado['listaAni']['apeMaterno']}\n"
                f"*Fecha de Nacimiento:* {resultado['listaAni']['feNacimiento']}\n\n"
                f"*Sexo:* {resultado['listaAni']['sexo']}\n"
                f"*Edad:* {resultado['listaAni']['nuEdad']}\n"
            )

            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
            await update.message.reply_document(document=resultado['pdf_bytes'], filename=f"{dni}_C4_BLANCO.pdf", caption=document_caption, parse_mode='Markdown')

        else:
            await update.message.reply_text(f"Error al obtener el c4")

    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error.")

async def c4i(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 4
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    message_text = update.message.text
    dni = message_text[len('/c4i'):].strip()

    if not dni.isdigit() or len(dni) != 8:
        await update.message.reply_text("Por favor proporciona un DNI válido de 8 dígitos.")
        return
    
    if not dni:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /c4i 00000001")
        return

    try:
        # Obtener resultado del API
        resultado = obtener_c4_inscripcion(dni)

        if resultado['success']:
            # Prepare the document caption with detailed description
            document_caption = (
                f"*[#PeruDox]* ➜ *C4 BLANCO*\n\n"
                f"*DNI:* `{dni}`\n"
                f"*NOMBRE:* {resultado['listaAni']['preNombres']} {resultado['listaAni']['apePaterno']} {resultado['listaAni']['apeMaterno']}\n"
                f"*Fecha de Nacimiento:* {resultado['listaAni']['feNacimiento']}\n\n"
                f"*Sexo:* {resultado['listaAni']['sexo']}\n"
                f"*Edad:* {resultado['listaAni']['nuEdad']}\n"
            )

            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
            await update.message.reply_document(document=resultado['pdf_bytes'], filename=f"{dni}_C4_INSCRIPCION.pdf", caption=document_caption, parse_mode='Markdown')

        else:
            await update.message.reply_text(f"Error al obtener el c4")

    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error.")

async def migr(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 10
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    message_text = update.message.text
    dni = message_text[len('/migr'):].strip()

    if not dni.isdigit() or len(dni) != 8:
        await update.message.reply_text("Por favor proporciona un DNI válido de 8 dígitos.")
        return
    
    if not dni:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /migr 43901266")
        return

    try:
        resultado = consultar_migraciones(dni)
        if resultado['success']:
            data = resultado['data']
            persona = data.get('persona', {})
            movimientos = data.get('movimiento', [])
            
            mensaje = (
                f"*[#PeruDox]* ➜ *INFORMACIÓN DE MIGRACIONES*\n\n"
                f"*DNI:* `{persona.get('nuDni', '')}`\n"
                f"*Nombre:* `{persona.get('preNombres', '')}`\n"
                f"*Apellido Paterno:* `{persona.get('apePaterno', '')}`\n"
                f"*Apellido Materno:* `{persona.get('apeMaterno', '')}`\n"
                f"*Fecha de Nacimiento:* `{persona.get('feNacimiento', '')}`\n"
                f"*País de Origen:* `{persona.get('oriPais', '')}`\n\n"
            )

            for mov in movimientos:
                mensaje += (
                    f"*Fecha de Movimiento:* `{mov.get('feMov', '')}`\n"
                    f"*Hora de Movimiento:* `{mov.get('hoMov', '')}`\n"
                    f"*Número de Documento:* `{mov.get('numDoc', '')}`\n"
                    f"*Destino:* `{mov.get('destino', '')}`\n"
                    f"*Tipo de Documento:* `{mov.get('tipoDoc', '')}`\n"
                    f"*Tipo de Movimiento:* `{mov.get('tipoMov', '')}`\n\n"
                )
            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
            await update.message.reply_text(mensaje, parse_mode='Markdown')

        else:
            mensaje = f"No se pudo encontrar información de migraciones para el DNI {dni}"
            await update.message.reply_text(mensaje, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error")

async def mininter(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 3
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    message_text = update.message.text
    dni = message_text[len('/minin'):].strip()

    if not dni.isdigit() or len(dni) != 8:
        await update.message.reply_text("Por favor proporciona un DNI válido de 8 dígitos.")
        return
    
    if not dni:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /minin 10393309")
        return

    try:
        resultado = consultar_mininter(dni)

        if resultado['status']:
            mensaje = (
                f"*[#PeruDox]* ➜ *INFORMACIÓN MININTER*\n\n"
                f"*DNI:* `{resultado.get('nuDni', '')}`\n"
                f"*Nombre:* `{resultado.get('preNomres', '')}`\n"
                f"*Apellido Paterno:* `{resultado.get('apePaterno', '')}`\n"
                f"*Apellido Materno:* `{resultado.get('apeMaterno', '')}`\n"
            )
            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
            await update.message.reply_text(mensaje, parse_mode='Markdown')
        else:
            mensaje = f"No se pudo encontrar información de MININTER para el DNI {dni}."
            await update.message.reply_text(mensaje, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error")

async def carnetx(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 2
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    message_text = update.message.text
    dni = message_text[len('/carnetx'):].strip()

    if not dni.isdigit() or len(dni) != 8:
        await update.message.reply_text("Por favor proporciona un DNI válido de 8 dígitos.")
        return
    
    if not dni:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /carnet 002434450")
        return

    try:
        resultado = consultar_carnet_extranjeria(dni)

        if resultado['nombres']:
            mensaje = (
                f"*[#PeruDox]* ➜ *CARNET DE EXTRANJERÍA*\n\n"
                f"*Nombres:* `{resultado.get('nombres', '')}`\n"
                f"*Primer Apellido:* `{resultado.get('primerApellido', '')}`\n"
                f"*Segundo Apellido:* `{resultado.get('segundoApellido', '')}`\n"
                f"*Calidad Migratoria:* `{resultado.get('calidadMigratoria', '')}`\n"
            )
            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
            await update.message.reply_text(mensaje, parse_mode='Markdown')
        else:
            mensaje = f"No se pudo encontrar información de carnet de extranjería para el DNI {dni}."
            await update.message.reply_text(mensaje, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error: {str(e)}")

async def mpfn(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 3
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    message_text = update.message.text
    dni = message_text[len('/mpfn'):].strip()

    if not dni.isdigit() or len(dni) != 8:
        await update.message.reply_text("Por favor proporciona un DNI válido de 8 dígitos.")
        return
    
    if not dni:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /mpfn 46958051")
        return

    try:
        resultado = consultar_mpfn(dni)

        if resultado['casos'] or resultado['libre']:
            mensaje = (
                f"*[#PeruDox]* ➜ *INFORMACIÓN DEL MPFN*\n\n"
            )
            if resultado['casos']:
                mensaje += "*Casos:*\n"
                for caso in resultado['casos']:
                    mensaje += (
                        f"- *Caso:* `{caso.get('caso', '')}`\n"
                        f"  *Distrito:* `{caso.get('distrito', '')}`\n"
                        f"  *Sede:* `{caso.get('sede', '')}`\n"
                        f"  *Número de Expediente:* `{caso.get('nroExp', '')}`\n"
                        f"  *Año:* `{caso.get('año', '')}`\n"
                        f"  *Defensor:* `{caso.get('defensor', '')}`\n\n"
                    )
            if resultado['libre']:
                mensaje += "*Libre:*\n"
                for libre in resultado['libre']:
                    mensaje += (
                        f"- *Fecha:* `{libre.get('fecha', '')}`\n"
                        f"  *Distrito:* `{libre.get('distrito', '')}`\n"
                        f"  *Sede:* `{libre.get('sede', '')}`\n"
                        f"  *Tipo:* `{libre.get('tipo', '')}`\n"
                        f"  *Diligencia:* `{libre.get('diligencia', '')}`\n"
                        f"  *Defensor:* `{libre.get('defensor', '')}`\n\n"
                    )
            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
            await update.message.reply_text(mensaje, parse_mode='Markdown')
        else:
            mensaje = f"No se encontró información en el MPFN para el DNI {dni}."
            await update.message.reply_text(mensaje, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error: {str(e)}")

async def movistar(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 2
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    message_text = update.message.text
    dni = message_text[len('/movistar'):].strip()

    if not dni:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /movistar 953246669")
        return

    try:
        resultado = consultar_movistar(dni)

        if resultado:
            mensaje = (
                f"*[#PeruDox]* ➜ *INFORMACIÓN DE MOVISTAR*\n\n"
            )

            for info in resultado:
                mensaje += (
                    f"*Nombre:* `{info.get('name', '')}`\n"
                    f"*Apellido:* `{info.get('surname', '')}`\n"
                    f"*Tipo de Documento:* `{info.get('typeDoc', '')}`\n"
                    f"*Número de Documento:* `{info.get('numDoc', '')}`\n"
                    f"*Número de Teléfono:* `{info.get('number', '')}`\n"
                    f"*Plan:* `{info.get('plan', '')}`\n"
                    f"*Tipo de Producto:* `{info.get('proType', '')}`\n"
                    f"*Fecha:* `{info.get('fecha', '')}`\n"
                    f"*Estado:* `{info.get('status', '')}`\n\n"
                )
            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
            await update.message.reply_text(mensaje, parse_mode='Markdown')
        else:
            mensaje = f"No se encontró información en Movistar para el DNI {dni}."
            await update.message.reply_text(mensaje, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error: {str(e)}")

async def bolivia(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 2
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    message_text = update.message.text
    dni = message_text[len('/bolivia'):].strip()

    if not dni:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /bolivia 44443333")
        return

    try:
        resultado = consultar_bolivia(dni)

        if resultado:
            persona = resultado.get('persona', {})
            nacimiento = resultado.get('nacimiento', {})

            mensaje = (
                f"*[#PeruDox]* ➜ *INFORMACIÓN DE BOLIVIA*\n\n"
                f"*Estado Persona:* `{persona.get('estadoPersona', '')}`\n"
                f"*Sexo:* `{persona.get('sexo', '')}`\n"
                f"*Tipo de Documento:* `{persona.get('tipoDoc', '')}`\n"
                f"*Número de Documento:* `{persona.get('numDoc', '')}`\n"
                f"*Nombre Completo:* `{persona.get('preNombres', '')} {persona.get('apePaterno', '')} {persona.get('apeMaterno', '')}`\n"
                f"*Fecha de Nacimiento:* `{persona.get('feNacimiento', '')}`\n\n"
                f"*Datos de Nacimiento:*\n"
                f"*Departamento de Nacimiento:* `{nacimiento.get('depNac', '')}`\n"
                f"*Provincia de Nacimiento:* `{nacimiento.get('provNac', '')}`\n"
                f"*Distrito de Nacimiento:* `{nacimiento.get('distNac', '')}`\n"
                f"*Fecha de Inscripción:* `{nacimiento.get('feInscripcion', '')}`\n"
                f"*Oficialía:* `{nacimiento.get('oficialia', '')}`\n\n"
                f"*Padre:*\n"
                f"*Nombre Completo:* `{nacimiento.get('padre', {}).get('preNombres', '')} {nacimiento.get('padre', {}).get('apePaterno', '')} {nacimiento.get('padre', {}).get('apeMaterno', '')}`\n"
                f"*Fecha de Nacimiento:* `{nacimiento.get('padre', {}).get('feNacimiento', '')}`\n\n"
                f"*Madre:*\n"
                f"*Nombre Completo:* `{nacimiento.get('madre', {}).get('preNombres', '')} {nacimiento.get('madre', {}).get('apePaterno', '')} {nacimiento.get('madre', {}).get('apeMaterno', '')}`\n"
                f"*Fecha de Nacimiento:* `{nacimiento.get('madre', {}).get('feNacimiento', '')}`\n"
            )
            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
            await update.message.reply_text(mensaje, parse_mode='Markdown')
        else:
            mensaje = f"No se encontró información en Bolivia para el DNI {dni}."
            await update.message.reply_text(mensaje, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error")

async def sentinel(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 10
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    message_text = update.message.text
    dni = message_text[len('/sentinel'):].strip()

    if not dni.isdigit() or len(dni) != 8:
        await update.message.reply_text("Por favor proporciona un DNI válido de 8 dígitos.")
        return
    
    if not dni:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /sentinel 44443333")
        return

    try:
        resultado = consultar_sentinel(dni)

        if resultado and resultado.get('coRespuesta') == "0000":
            lista_ani = resultado.get('listaAni', {})
            sen_base64 = resultado.get('sen', '')

            # Decodificar el documento PDF desde base64
            pdf_bytes = base64.b64decode(sen_base64)

            # Enviar el documento PDF como archivo
            bio = BytesIO()
            bio.write(pdf_bytes)
            bio.seek(0)
            
            # Mostrar información adicional del usuario
            mensaje = (
                f"*[#PeruDox]* ➜ *INFORMACIÓN SENTINEL*\n\n"
                f"*DNI:* `{lista_ani.get('nuDni', '')}`\n"
                # f"*Apellido Paterno:* `{lista_ani.get('apePaterno', '')}`\n"
                # f"*Apellido Materno:* `{lista_ani.get('apeMaterno', '')}`\n"
                f"*Nombres:* `{lista_ani.get('preNombres', '')} {lista_ani.get('apePaterno', '')} {lista_ani.get('apeMaterno', '')}`\n"
                f"*Fecha de Nacimiento:* `{lista_ani.get('feNacimiento', '')}`\n"
                f"*Edad:* `{lista_ani.get('nuEdad', '')}` años\n"
            )
            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
            await update.message.reply_document(bio, filename=f"{dni}_sentinel.pdf", caption=mensaje, parse_mode='Markdown')

        else:
            mensaje = f"No se encontró información en Sentinel para el DNI {dni}."
            await update.message.reply_text(mensaje, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error.")

async def boleta(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 2
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    message_text = update.message.text
    dni = message_text[len('/boleta'):].strip()

    if not dni:
        await update.message.reply_text("Por favor proporciona un código después del comando. Ejemplo: /boleta acq880")
        return

    try:
        resultado = consultar_boleta_informativa(dni)

        if resultado and resultado.get('boleta'):
            boleta_base64 = resultado.get('boleta')
            data = resultado.get('data', [])

            # Decodificar el documento PDF desde base64
            pdf_bytes = base64.b64decode(boleta_base64.split(',')[1])  # Separar el prefijo "data:application/pdf;base64,"

            # Enviar el documento PDF como archivo
            bio = BytesIO()
            bio.write(pdf_bytes)
            bio.seek(0)

            # Mostrar información adicional de la boleta informativa
            if data:
                mensaje = (
                    f"*[#PeruDox]* ➜ *BOLETA INFORMATIVA*\n\n"
                )
                for item in data:
                    mensaje += (
                        f"*Tipo de Participación:* `{item.get('tipoPartic', '')}`\n"
                        f"*Tipo de Documento:* `{item.get('tipDocumento', '')}`\n"
                        f"*Documento:* `{item.get('documento', '')}`\n"
                        f"*Propietario:* `{item.get('propietario', '')}`\n"
                        f"*Dirección:* `{item.get('direccion', '')}`\n"
                        f"*Fecha de Propiedad:* `{item.get('fechaProp', '')}`\n"
                        f"*Número de Placa:* `{item.get('numPlaca', '') or 'N/A'}`\n\n"
                    )
            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
            await update.message.reply_document(bio, filename=f"{dni}_boleta.pdf", caption=mensaje, parse_mode='Markdown')
                
        else:
            mensaje = f"No se encontró información en la boleta informativa para el DNI {dni}."
            await update.message.reply_text(mensaje, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error.")

async def acta_nacimiento(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 15
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    message_text = update.message.text
    dni = message_text[len('/actna'):].strip()

    if not dni.isdigit() or len(dni) != 8:
        await update.message.reply_text("Por favor proporciona un DNI válido de 8 dígitos.")
        return
    
    if not dni:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /actna 72199494")
        return

    try:
        resultado = consultar_acta_nacimiento(dni)

        if resultado and resultado.get('anverso') and resultado.get('reverso'):
            anverso_base64 = resultado.get('anverso')
            reverso_base64 = resultado.get('reverso')
            data = resultado.get('listaAni', {})

            # Decodificar el anverso y enviarlo como documento adjunto
            anverso_pdf_bytes = base64.b64decode(anverso_base64.split(',')[1])
            bio_anverso = BytesIO()
            bio_anverso.write(anverso_pdf_bytes)
            bio_anverso.seek(0)

            # Decodificar el reverso y enviarlo como documento adjunto
            reverso_pdf_bytes = base64.b64decode(reverso_base64.split(',')[1])
            bio_reverso = BytesIO()
            bio_reverso.write(reverso_pdf_bytes)
            bio_reverso.seek(0)

            # Mostrar información adicional del acta de nacimiento
            mensaje = (
                f"*[#PeruDox]* ➜ *ACTA DE NACIMIENTO*\n\n"
                f"*DNI:* `{data.get('nuDni', '')}`\n"
                f"*Nombres:* `{data.get('preNombres', '')} {data.get('apePaterno', '')} {data.get('apeMaterno', '')}`\n"
                f"*Fecha de Evento:* `{data.get('feEvento', '')}`\n"
                f"*Estado del Acta:* `{data.get('estadoActa', '')}`\n\n"
                f"*Estado:* `{data.get('deEstado', '')}`\n"
                f"*Número de Acta:* `{data.get('numActa', '')}`\n"
                f"*Número Local:* `{data.get('numLocal', '')}`\n"
            )
            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
            await update.message.reply_document(bio_anverso, filename=f"{dni}_acta_nacimiento_anverso.pdf", caption=mensaje, parse_mode='Markdown')  
            await update.message.reply_document(bio_reverso, filename=f"{dni}_acta_nacimiento_reverso.pdf", caption=mensaje, parse_mode='Markdown')

        else:
            mensaje = f"No se encontró información del acta de nacimiento para el DNI {dni}."
            await update.message.reply_text(mensaje, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error.")

async def acta_matrimonio(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 15
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    message_text = update.message.text
    dni = message_text[len('/actma'):].strip()

    if not dni.isdigit() or len(dni) != 8:
        await update.message.reply_text("Por favor proporciona un DNI válido de 8 dígitos.")
        return
    
    if not dni:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /actma 07910103")
        return

    try:
        resultado = consultar_acta_matrimonio(dni)

        if resultado and resultado.get('anverso') and resultado.get('reverso'):
            anverso_base64 = resultado.get('anverso')
            reverso_base64 = resultado.get('reverso')
            data = resultado.get('listaAni', {})

            # Decodificar el anverso y enviarlo como documento adjunto
            anverso_pdf_bytes = base64.b64decode(anverso_base64.split(',')[1])
            bio_anverso = BytesIO()
            bio_anverso.write(anverso_pdf_bytes)
            bio_anverso.seek(0)
            

            # Decodificar el reverso y enviarlo como documento adjunto
            reverso_pdf_bytes = base64.b64decode(reverso_base64.split(',')[1])
            bio_reverso = BytesIO()
            bio_reverso.write(reverso_pdf_bytes)
            bio_reverso.seek(0)

            # Mostrar información adicional del acta de matrimonio
            mensaje = (
                f"*[#PeruDox]* ➜ *ACTA DE MATRIMONIO*\n\n"
                f"*DNI:* `{data.get('nuDni', '')}`\n"
                f"*Apellido Paterno:* `{data.get('apePaterno', '')}`\n"
                f"*Apellido Materno:* `{data.get('apeMaterno', '')}`\n"
                f"*Nombres:* `{data.get('preNombres', '')}`\n"
                f"*Fecha de Evento:* `{data.get('feEvento', '')}`\n"
                f"*Estado del Acta:* `{data.get('estadoActa', '')}`\n\n"
                f"*Estado:* `{data.get('deEstado', '')}`\n"
                f"*Número de Acta:* `{data.get('numActa', '')}`\n"
                f"*Número Local:* `{data.get('numLocal', '')}`\n"
            )
            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
            await update.message.reply_document(bio_anverso, filename=f"{dni}_acta_matrimonio_anverso.pdf", caption=mensaje, parse_mode='Markdown')
            await update.message.reply_document(bio_reverso, filename=f"{dni}_acta_matrimonio_reverso.pdf", caption=mensaje, parse_mode='Markdown')

        else:
            mensaje = f"No se encontró información del acta de matrimonio para el DNI {dni}."
            await update.message.reply_text(mensaje, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error: {str(e)}")

async def acta_defuncion(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 15
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    message_text = update.message.text
    dni = message_text[len('/actde'):].strip()

    if not dni.isdigit() or len(dni) != 8:
        await update.message.reply_text("Por favor proporciona un DNI válido de 8 dígitos.")
        return
    
    if not dni:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /actde 00000001")
        return

    try:
        resultado = consultar_acta_defuncion(dni)

        if resultado and resultado.get('anverso') and resultado.get('reverso'):
            anverso_base64 = resultado.get('anverso')
            reverso_base64 = resultado.get('reverso')
            data = resultado.get('listaAni', {})

            # Decodificar el anverso y enviarlo como documento adjunto
            anverso_pdf_bytes = base64.b64decode(anverso_base64.split(',')[1])
            bio_anverso = BytesIO()
            bio_anverso.write(anverso_pdf_bytes)
            bio_anverso.seek(0)
            

            # Decodificar el reverso y enviarlo como documento adjunto
            reverso_pdf_bytes = base64.b64decode(reverso_base64.split(',')[1])
            bio_reverso = BytesIO()
            bio_reverso.write(reverso_pdf_bytes)
            bio_reverso.seek(0)

            # Mostrar información adicional del acta de defunción
            mensaje = (
                f"*[#PeruDox]* ➜ *ACTA DE DEFUNCIÓN*\n\n"
                f"*DNI:* `{data.get('nuDni', '')}`\n"
                f"*Apellido Paterno:* `{data.get('apePaterno', '')}`\n"
                f"*Apellido Materno:* `{data.get('apeMaterno', '')}`\n"
                f"*Nombres:* `{data.get('preNombres', '')}`\n"
                f"*Fecha de Evento:* `{data.get('feEvento', '')}`\n"
                f"*Estado del Acta:* `{data.get('estadoActa', '')}`\n\n"
                f"*Estado:* `{data.get('deEstado', '')}`\n"
                f"*Número de Acta:* `{data.get('numActa', '')}`\n"
                f"*Número Local:* `{data.get('numLocal', '')}`\n"
            )
            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
            await update.message.reply_document(bio_anverso, filename=f"{dni}_acta_defuncion_anverso.pdf", caption=mensaje, parse_mode='Markdown')
            await update.message.reply_document(bio_reverso, filename=f"{dni}_acta_defuncion_reverso.pdf", caption=mensaje, parse_mode='Markdown')

        else:
            mensaje = f"No se encontró información del acta de defunción para el DNI {dni}."
            await update.message.reply_text(mensaje, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error.")

async def papeletas(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 3
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    message_text = update.message.text
    dni = message_text[len('/papeletas'):].strip()

    if not dni.isdigit() or len(dni) != 8:
        await update.message.reply_text("Por favor proporciona un DNI válido de 8 dígitos.")
        return
    
    if not dni:
        await update.message.reply_text("Por favor proporciona una placa después del comando. Ejemplo: /papeletas RM1514")
        return

    try:
        resultado = consultar_papeletas_api(dni)

        if resultado:
            for papeleta in resultado:
                mensaje = format_papeleta_message(papeleta)
                await update.message.reply_text(mensaje, parse_mode='Markdown')

                if 'evidencia' in papeleta and papeleta['evidencia']:
                    try:
                        if isinstance(papeleta['evidencia'], str) and papeleta['evidencia'].startswith('data:'):
                            evidencia_base64 = papeleta['evidencia'].split(',')[1]
                        else:
                            evidencia_base64 = papeleta['evidencia']

                        evidencia_image_bytes = base64.b64decode(evidencia_base64)
                        bio_evidencia = BytesIO()
                        bio_evidencia.write(evidencia_image_bytes)
                        bio_evidencia.seek(0)
                        await update.message.reply_photo(bio_evidencia)
                    except Exception as e:
                        await update.message.reply_text(f"No se pudo enviar la evidencia de la papeleta: {str(e)}")
            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
        else:
            await update.message.reply_text(f"No se encontraron papeletas para el DNI o placa {dni}.")

    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error.")

async def notas(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 4
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    message_text = update.message.text
    dni = message_text[len('/notas'):].strip()

    if not dni.isdigit() or len(dni) != 8:
        await update.message.reply_text("Por favor proporciona un DNI válido de 8 dígitos.")
        return
    
    if not dni:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /notas 60637333")
        return

    try:
        resultado = consultar_notas(dni)
        
        # Comprobación de resultado
        if not resultado:
            await update.message.reply_text("No se obtuvo una respuesta válida de la API.")
            return

        # Comprobación de 'grados'
        if 'grados' not in resultado:
            await update.message.reply_text("La respuesta no contiene información de 'grados'.")
            return
        
        grados = resultado['grados']
        col_info = resultado.get('colInfo', {})

        if not grados:
            mensaje = f"No se encontró información de notas para el DNI {dni}."
            await update.message.reply_text(mensaje)
            return

        # Mostrar información adicional del estudiante
        mensaje = (
            f"*[#PeruDox]* ➜ *NOTAS*\n\n"
            f"*DNI:* `{col_info.get('numDocumento', '')}`\n"
            f"*Nombre del Padre:* `{col_info.get('nomPadre', '')}`\n"
            f"*Nombre de la Madre:* `{col_info.get('nomMadre', '')}`\n"
            f"*Departamento:* `{col_info.get('depaDireccion', '')}`\n"
            f"*Provincia:* `{col_info.get('provDireccion', '')}`\n"
            f"*Distrito:* `{col_info.get('distDireccion', '')}`\n"
            f"*Ubicación:* `{col_info.get('ubiDireccion', '')}`\n\n"
        )
        await consumo_creditos(update, context, user_id, creditos)
        await increment_queries(user_id)
        await update.message.reply_text(mensaje, parse_mode='Markdown')

        # Enviar cada grado como documento adjunto
        for grado in grados:
            pdf_base64 = grado.get('pdf64')
            if pdf_base64:
                try:
                    # Comprobación de pdf_base64
                    if not pdf_base64.startswith("JVBER"):
                        await update.message.reply_text(f"PDF base64 no válido para el grado: {grado.get('descripcionGrado', 'Desconocido')}")
                        continue

                    pdf_bytes = base64.b64decode(pdf_base64)
                    bio_pdf = BytesIO()
                    bio_pdf.write(pdf_bytes)
                    bio_pdf.seek(0)

                    mensaje_grado = (
                        f"*Nivel:* `{grado.get('nivelColegio', '')}`\n"
                        f"*Año:* `{grado.get('idAnio', '')}`\n"
                        f"*Institución Educativa:* `{grado.get('nombreIE', '')}`\n"
                        f"*Grado:* `{grado.get('descripcionGrado', '')}`\n"
                        f"*Estado del Acta:* `{grado.get('estadoActa', '')}`\n\n"
                    )
                    await update.message.reply_document(bio_pdf, filename=f"{dni}_notas_{grado.get('idAnio')}.pdf", caption=mensaje_grado, parse_mode='Markdown')
                except Exception as e:
                    await update.message.reply_text(f"Error al procesar el PDF para el año {grado.get('idAnio')}: {e}")

    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error al realizar la consulta de notas.")

async def licencia(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await antepam(update, context):
        return
    await update_last_query_time(user_id)

    if await verificar_mensualidad_activa(user_id):
        creditos = 0
    else:
        creditos = 2
        suficientes = verificar_creditos_suficientes(user_id, creditos)

        if not suficientes:
            await update.message.reply_text("No tienes créditos suficientes para usar este comando. Pulsa /buy para comprar.")
            return

    message_text = update.message.text
    dni = message_text[len('/licen'):].strip()

    if not dni.isdigit() or len(dni) != 8:
        await update.message.reply_text("Por favor proporciona un DNI válido de 8 dígitos.")
        return
    
    if not dni:
        await update.message.reply_text("Por favor proporciona un DNI después del comando. Ejemplo: /licencia 70194468")
        return

    try:
        resultado = consultar_licencia(dni)

        if resultado and 'listaAni' in resultado:
            lista_ani = resultado['listaAni']
            licencias = resultado.get('licencias', [])
            tramites = resultado.get('tramites', {})
            general = resultado.get('general', {})

            # Mostrar información general del usuario
            mensaje = (
                f"*[#PeruDox]* ➜ *LICENCIA MTC*\n\n"
                f"*DNI:* `{lista_ani.get('nuDni', '')}`\n"
                f"*Nombres:* `{lista_ani.get('preNombres', '')} {lista_ani.get('apePaterno', '')} {lista_ani.get('apeMaterno', '')}`\n"
                f"*Tipo de Documento:* `{lista_ani.get('tipoDocumento', '')}`\n"
                f"*Dona Órganos:* `{lista_ani.get('donaOrganos', '')}`\n\n"
            )
            await update.message.reply_text(mensaje, parse_mode='Markdown')

            # Mostrar información de licencias
            if licencias:
                for licencia in licencias:
                    mensaje_licencia = (
                        f"*Número de Licencia:* `{licencia.get('NroLicencia', '')}`\n"
                        f"*Categoría:* `{licencia.get('CategoriaLicencia', '')}`\n"
                        f"*Fecha de Expedición:* `{licencia.get('FechaExpedicion', '')}`\n"
                        f"*Fecha de Vencimiento:* `{licencia.get('VenceLicencia', '')}`\n"
                        f"*Estado:* `{licencia.get('EstadoLicencia', '')}`\n"
                        f"*Restricciones:* `{licencia.get('Restricciones', '')}`\n"
                        f"*Centro de Emisión:* `{licencia.get('CentroEmision', '')}`\n\n"
                    )
                    await update.message.reply_text(mensaje_licencia, parse_mode='Markdown')

            # Mostrar información de trámites
            for categoria, tramites_categoria in tramites.items():
                if tramites_categoria:
                    for tramite in tramites_categoria:
                        mensaje_tramite = (
                            f"*Número de Licencia:* `{tramite.get('NroLicencia', '')}`\n"
                            f"*Trámite:* `{tramite.get('Tramite', '')}`\n"
                            f"*Categoría:* `{tramite.get('Categoria', '')}`\n"
                            f"*Fecha de Emisión:* `{tramite.get('FechaEmision', '')}`\n"
                            f"*Fecha de Expedición:* `{tramite.get('FechaExpedicion', '')}`\n"
                            f"*Fecha de Revalidación:* `{tramite.get('FechaRevalidacion', '')}`\n"
                            f"*Estado:* `{tramite.get('Estado', '')}`\n"
                            f"*Restricciones:* `{tramite.get('Restriccion1', '')} {tramite.get('Restriccion2', '')}`\n"
                            f"*Centro de Emisión:* `{tramite.get('CentroEmision', '')}`\n\n"
                        )
                        await update.message.reply_text(mensaje_tramite, parse_mode='Markdown')
            await consumo_creditos(update, context, user_id, creditos)
            await increment_queries(user_id)
        else:
            mensaje = f"No se encontró información de la licencia para el DNI {dni}."
            await update.message.reply_text(mensaje, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"Ha ocurrido un error al realizar la consulta de licencia.")

async def buy(update: Update, context: ContextTypes):
    caption = (
        f"*__Bienvenido a los Precios de PeruDox [🇵🇪]__*\n\n"
        f"*__LOS PRECIOS DE LOS CRÉDITOS SON LOS SIGUIENTES:__*\n\n"
        f"*__📍 40 CRÉDITOS + 20 ➜ 10 SOLES ➜ BÁSICO__*\n"
        f"*__📍 60 CRÉDITOS + 20 ➜ 15 SOLES ➜ BÁSICO__*\n"
        f"*__📍 90 CRÉDITOS + 30 ➜ 20 SOLES ➜ ESTANDAR__*\n"
        f"*__📍 210 CRÉDITOS + 50 ➜ 25 SOLES ➜ ESTANDAR__*\n"
        f"*__📍 250 CRÉDITOS + 50 ➜ 30 SOLES ➜ ESTANDAR__*\n"
        f"*__📍 480 CRÉDITOS + 100 ➜ 40 SOLES ➜ PREMIUM__*\n"
        f"*__📍 660 CRÉDITOS + 120 ➜ 50 SOLES ➜ PREMIUM__*\n"
        f"*__📍 860 CRÉDITOS + 160 ➜ 60 SOLES ➜ PREMIUM__*\n"
        f"*__📍 1K CRÉDITOS + 550 ➜ 70 SOLES ➜ PREMIUM__*\n\n"  

        f"*[🧿] VIP ILIMITADO*\n\n"   

        f"*__📍 VIP 07 DÍAS ➜ 25 SOLES ➜ BÁSICO__*\n"
        f"*__📍 VIP 15 DÍAS ➜ 40 SOLES ➜ PREMIUM__*\n"
        f"*__📍 VIP 30 DÍAS ➜ 80 SOLES ➜ PREMIUM__*\n"
        f"*__📍 VIP 60 DÍAS ➜ 150 SOLES ➜ PREMIUM__*\n"
        f"*__📍 VIP 90 DÍAS ➜ 200 SOLES ➜ PREMIUM__*\n\n"

        f"*[🕒] ANTI-SPAM*\n\n"   

        f"*__• BÁSICO = 30'__*\n"
        f"*__• ESTANDAR = 15'__*\n"
        f"*__• PREMIUM = 10'__*\n\n"


        f"*__🎭 SELLERS OFICIALES 🎭__*\n"
    )
    await context.bot.send_message(chat_id=update.message.chat_id, text=caption, parse_mode='Markdown')

if __name__ == '__main__':
    print('Iniciando bot...')
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('register', register))
    app.add_handler(CommandHandler('buy', buy))

    app.add_handler(CommandHandler('add_cred', add_cred))
    app.add_handler(CommandHandler('more_cred', more_cred))
    app.add_handler(CommandHandler('add_days', add_days))
    app.add_handler(CommandHandler('more_days', more_days))
    app.add_handler(CommandHandler('add_seller', add_seller))
    app.add_handler(CommandHandler('rem_seller', remove_seller))
    app.add_handler(CommandHandler('anti_spam', anti_spam))
    app.add_handler(CommandHandler('user', user_info))

    app.add_handler(CommandHandler('me', me))
    app.add_handler(CommandHandler('cmds', cmds))
    app.add_handler(CallbackQueryHandler(button_click))
    app.add_handler(CommandHandler('nm', nombre))
    app.add_handler(CommandHandler('dni', reniecBasico))
    app.add_handler(CommandHandler('dnif', reniecCompleto))
    app.add_handler(CommandHandler('dnix', dniBasico))
    app.add_handler(CommandHandler('hog', hogar))
    app.add_handler(CommandHandler('pred', predios))
    app.add_handler(CommandHandler('tel', tel))
    app.add_handler(CommandHandler('fam', familiares))
    app.add_handler(CommandHandler('arb', arbol))
    app.add_handler(CommandHandler('herm', hermanos))
    app.add_handler(CommandHandler('bitel', bitel))
    app.add_handler(CommandHandler('claro', claro))
    app.add_handler(CommandHandler('movistar', movistar))
    app.add_handler(CommandHandler('placas', placas))
    app.add_handler(CommandHandler('sunarp', sunarp))
    app.add_handler(CommandHandler('correo', correo))
    app.add_handler(CommandHandler('sueldos', sueldos))
    app.add_handler(CommandHandler('sbs', sbs))
    app.add_handler(CommandHandler('geo', geo))
    app.add_handler(CommandHandler('ruc', ruc))
    app.add_handler(CommandHandler('sunedu', sunedu))
    app.add_handler(CommandHandler('telx', telefonox))
    app.add_handler(CommandHandler('dniv', dniv))
    app.add_handler(CommandHandler('dnie', dnie))
    app.add_handler(CommandHandler('antju', antjud))
    app.add_handler(CommandHandler('antpo', antpol))
    app.add_handler(CommandHandler('antpe', antpen))
    app.add_handler(CommandHandler('c4a', c4a))
    app.add_handler(CommandHandler('c4b', c4b))
    app.add_handler(CommandHandler('c4i', c4i))
    app.add_handler(CommandHandler('migr', migr))
    app.add_handler(CommandHandler('minin', mininter))
    app.add_handler(CommandHandler('carnetx', carnetx))
    app.add_handler(CommandHandler('mpfn', mpfn))
    app.add_handler(CommandHandler('bolivia', bolivia))
    app.add_handler(CommandHandler('sentinel', sentinel))
    app.add_handler(CommandHandler('boleta', boleta))
    app.add_handler(CommandHandler('actna', acta_nacimiento))
    app.add_handler(CommandHandler('actma', acta_matrimonio))
    app.add_handler(CommandHandler('actde', acta_defuncion))
    app.add_handler(CommandHandler('papeletas', papeletas))
    app.add_handler(CommandHandler('notas', notas))
    app.add_handler(CommandHandler('licen', licencia))
    print('Bot iniciado')
    app.run_polling(poll_interval=1, timeout=40.0)

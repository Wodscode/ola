import requests
import base64
from io import BytesIO
from config import userId
def consultar_reniec(dni):
    url = "https://www.fakersys.com/api/v2/reniec"
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://fakersys.com"
    }
    body = {
        "userId": userId,
        "dni": dni
    }

    response = requests.post(url, headers=headers, json=body)
    data = response.json()

    if data['coRespuesta'] == "0000":
        persona = data['listaAni'][0]
        foto_bytes = base64.b64decode(data['foto'])
        firma_bytes = base64.b64decode(data['firma'])
        hderecha_bytes = base64.b64decode(data['hderecha'])
        hizquierda_bytes = base64.b64decode(data['hizquierda'])

        return {
            'success': True,
            'nombre': persona['preNombres'],
            'ape_paterno': persona['apePaterno'],
            'ape_materno': persona['apeMaterno'],
            'digitoVerificacion': persona['digitoVerificacion'],
            'nuDni': persona['nuDni'],
            'inCel': persona['inCel'],
            'tipoFicha': persona['tipoFicha'],
            'tipoFichaImag': persona['tipoFichaImag'],
            'coRestriccion': persona['coRestriccion'],
            'grRestriccion': persona['grRestriccion'],
            'deCel': persona['deCel'],
            'nuDatos': persona['nuDatos'],
            'nuImagen': persona['nuImagen'],
            'feNacimiento': persona['feNacimiento'],
            'nuEdad': persona['nuEdad'],
            'nuDocPadre': persona['nuDocPadre'],
            'coTipoDocPadre': persona['coTipoDocPadre'],
            'nuDocMadre': persona['nuDocMadre'],
            'coTipoDocMadre': persona['coTipoDocMadre'],
            'nuDocDeclarante': persona['nuDocDeclarante'],
            'coTipoDeclarante': persona['coTipoDeclarante'],
            'deGenero': persona['deGenero'],
            'estatura': persona['estatura'],
            'sexo': persona['sexo'],
            'estadoCivil': persona['estadoCivil'],
            'gradoInstruccion': persona['gradoInstruccion'],
            'feEmision': persona['feEmision'],
            'feInscripcion': persona['feInscripcion'],
            'nomPadre': persona['nomPadre'],
            'nomMadre': persona['nomMadre'],
            'cancelacion': persona['cancelacion'],
            'departamento': persona['departamento'],
            'provincia': persona['provincia'],
            'distrito': persona['distrito'],
            'depaDireccion': persona['depaDireccion'],
            'provDireccion': persona['provDireccion'],
            'distDireccion': persona['distDireccion'],
            'feFallecimiento': persona['feFallecimiento'],
            'depaFallecimiento': persona['depaFallecimiento'],
            'provFallecimiento': persona['provFallecimiento'],
            'distFallecimiento': persona['distFallecimiento'],
            'feCaducidad': persona['feCaducidad'],
            'donaOrganos': persona['donaOrganos'],
            'glosaInfo': persona['glosaInfo'],
            'observacion': persona['observacion'],
            'vinculoDeclarante': persona['vinculoDeclarante'],
            'nomDeclarante': persona['nomDeclarante'],
            'deRestriccion': persona['deRestriccion'],
            'coDocEmi': persona['coDocEmi'],
            'desDireccion': persona['desDireccion'],
            'coTipoDoc': persona['coTipoDoc'],
            'apCasada': persona['apCasada'],
            'inGrupoRestri': persona['inGrupoRestri'],
            'ubiReniec': persona['ubiReniec'],
            'ubiInei': persona['ubiInei'],
            'ubiCP': persona['ubiCP'],
            'numTel': persona['numTel'],
            'numPro': persona['numPro'],
            'numActas': persona['numActas'],
            'foto_bytes': foto_bytes,
            'firma_bytes': firma_bytes,
            'hderecha_bytes': hderecha_bytes,
            'hizquierda_bytes': hizquierda_bytes
        }
    else:
        return {
            'success': False,
            'mensaje_error': data['deRespuesta']
        }
    
def consultar_reniec_una_foto(dni):
    url = "https://www.fakersys.com/api/v2/renmid"
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://fakersys.com"
    }
    body = {
        "userId": userId,
        "dni": dni
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        return {'success': False, 'mensaje_error': str(e)}

    if data.get('coRespuesta') == "0000":
        persona = data['listaAni']
        foto_bytes = base64.b64decode(data['foto'])

        return {
            'success': True,
            'nombre': persona.get('preNombres'),
            'ape_paterno': persona.get('apePaterno'),
            'ape_materno': persona.get('apeMaterno'),
            'digitoVerificacion': persona.get('digitoVerificacion'),
            'nuDni': persona.get('nuDni'),
            'inCel': persona.get('inCel'),
            'tipoFicha': persona.get('tipoFicha'),
            'tipoFichaImag': persona.get('tipoFichaImag'),
            'coRestriccion': persona.get('coRestriccion'),
            'grRestriccion': persona.get('grRestriccion'),
            'deCel': persona.get('deCel'),
            'nuDatos': persona.get('nuDatos'),
            'nuImagen': persona.get('nuImagen'),
            'feNacimiento': persona.get('feNacimiento'),
            'nuEdad': persona.get('nuEdad'),
            'nuDocPadre': persona.get('nuDocPadre'),
            'coTipoDocPadre': persona.get('coTipoDocPadre'),
            'nuDocMadre': persona.get('nuDocMadre'),
            'coTipoDocMadre': persona.get('coTipoDocMadre'),
            'nuDocDeclarante': persona.get('nuDocDeclarante'),
            'coTipoDeclarante': persona.get('coTipoDeclarante'),
            'deGenero': persona.get('deGenero'),
            'estatura': persona.get('estatura'),
            'sexo': persona.get('sexo'),
            'estadoCivil': persona.get('estadoCivil'),
            'gradoInstruccion': persona.get('gradoInstruccion'),
            'feEmision': persona.get('feEmision'),
            'feInscripcion': persona.get('feInscripcion'),
            'nomPadre': persona.get('nomPadre'),
            'nomMadre': persona.get('nomMadre'),
            'cancelacion': persona.get('cancelacion'),
            'departamento': persona.get('departamento'),
            'provincia': persona.get('provincia'),
            'distrito': persona.get('distrito'),
            'depaDireccion': persona.get('depaDireccion'),
            'provDireccion': persona.get('provDireccion'),
            'distDireccion': persona.get('distDireccion'),
            'feFallecimiento': persona.get('feFallecimiento'),
            'depaFallecimiento': persona.get('depaFallecimiento'),
            'provFallecimiento': persona.get('provFallecimiento'),
            'distFallecimiento': persona.get('distFallecimiento'),
            'feCaducidad': persona.get('feCaducidad'),
            'donaOrganos': persona.get('donaOrganos'),
            'glosaInfo': persona.get('glosaInfo'),
            'observacion': persona.get('observacion'),
            'vinculoDeclarante': persona.get('vinculoDeclarante'),
            'nomDeclarante': persona.get('nomDeclarante'),
            'deRestriccion': persona.get('deRestriccion'),
            'coDocEmi': persona.get('coDocEmi'),
            'desDireccion': persona.get('desDireccion'),
            'coTipoDoc': persona.get('coTipoDoc'),
            'apCasada': persona.get('apCasada'),
            'inGrupoRestri': persona.get('inGrupoRestri'),
            'ubiReniec': persona.get('ubiReniec'),
            'ubiInei': persona.get('ubiInei'),
            'ubiCP': persona.get('ubiCP'),
            'numTel': persona.get('numTel'),
            'numPro': persona.get('numPro'),
            'numActas': persona.get('numActas'),
            'foto_bytes': foto_bytes,
        }
    else:
        return {
            'success': False,
            'mensaje_error': data.get('deRespuesta', 'Error desconocido')
        }
    
def consultar_sunarp(dni):
    url = 'https://www.fakersys.com/api/v2/sunarp'
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://fakersys.com"
    }
    payload = {
        "userId": userId,
        "dni": dni
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        return {'success': False, 'mensaje_error': str(e)}

    if 'img' in data:
        img_bytes = base64.b64decode(data['img'])
        return {
            'success': True,
            'foto_bytes': img_bytes
        }
    else:
        return {
            'success': False,
            'mensaje_error': 'No se recibió una imagen en la respuesta'
        }
    
def obtener_dni_virtual(dni):
    url = "https://www.fakersys.com/api/v2/dni-virtual"
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://fakersys.com"
    }
    payload = {
        "userId": userId,
        "dni": dni
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if 'front' in data and 'back' in data and 'listaAni' in data:
            front_image_base64 = data['front']
            back_image_base64 = data['back']
            lista_ani = data['listaAni']

            # Decode base64 images
            front_image_bytes = base64.b64decode(front_image_base64.split(',')[1])
            back_image_bytes = base64.b64decode(back_image_base64.split(',')[1])

            return {
                'success': True,
                'front_image': front_image_bytes,
                'back_image': back_image_bytes,
                'listaAni': lista_ani
            }
        else:
            return {
                'success': False,
                'mensaje_error': 'Respuesta inválida de la API'
            }

    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'mensaje_error': f'Error en la conexión con la API: {str(e)}'
        }    

def obtener_dni_electronico(dni):
    url = "https://www.fakersys.com/api/v2/dni-electronico"
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://fakersys.com"
    }
    payload = {
        "userId": userId,
        "dni": dni
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if 'front' in data and 'back' in data and 'listaAni' in data:
            front_image_base64 = data['front']
            back_image_base64 = data['back']
            lista_ani = data['listaAni']

            # Decode base64 images
            front_image_bytes = base64.b64decode(front_image_base64.split(',')[1])
            back_image_bytes = base64.b64decode(back_image_base64.split(',')[1])

            return {
                'success': True,
                'front_image': front_image_bytes,
                'back_image': back_image_bytes,
                'listaAni': lista_ani
            }
        else:
            return {
                'success': False,
                'mensaje_error': 'Respuesta inválida de la API'
            }

    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'mensaje_error': f'Error en la conexión con la API: {str(e)}'
        }    

def obtener_antecedentes_judiciales(dni):
    url = "https://www.fakersys.com/api/v2/ant-judiciales"
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://fakersys.com"
    }
    payload = {
        "userId": userId,
        "dni": dni
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if 'antecedentes' in data and 'listaAni' in data:
            pdf_base64 = data['antecedentes']

            # Decode base64 PDF
            pdf_bytes = base64.b64decode(pdf_base64.split(',')[-1])  # Use [-1] to get the last part after splitting

            lista_ani = data['listaAni']

            return {
                'success': True,
                'pdf_bytes': pdf_bytes,
                'listaAni': lista_ani
            }
        else:
            return {
                'success': False,
                'mensaje_error': 'Respuesta inválida de la API'
            }

    except requests.exceptions.RequestException as e:
        print(f"Error de conexión")
        return {
            'success': False,
            'mensaje_error': f'Error de conexión'
        }
    except Exception as e:
        print(f"Error inesperado")
        return {
            'success': False,
            'mensaje_error': f'Error inesperado'
        }

def obtener_antecedentes_policiales(dni):
    url = "https://www.fakersys.com/api/v2/ant-policiales"
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://fakersys.com"
    }
    payload = {
        "userId": userId,
        "dni": dni
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if 'antecedentes' in data and 'listaAni' in data:
            pdf_base64 = data['antecedentes']

            # Decode base64 PDF
            pdf_bytes = base64.b64decode(pdf_base64.split(',')[-1])  # Use [-1] to get the last part after splitting

            lista_ani = data['listaAni']

            return {
                'success': True,
                'pdf_bytes': pdf_bytes,
                'listaAni': lista_ani
            }
        else:
            return {
                'success': False,
                'mensaje_error': 'Respuesta inválida de la API'
            }

    except requests.exceptions.RequestException as e:
        print(f"Error de conexión")
        return {
            'success': False,
            'mensaje_error': f'Error de conexión'
        }
    except Exception as e:
        print(f"Error inesperado")
        return {
            'success': False,
            'mensaje_error': f'Error inesperado'
        }

def obtener_antecedentes_penales(dni):
    url = "https://www.fakersys.com/api/v2/ant-penales"
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://fakersys.com"
    }
    payload = {
        "userId": userId,
        "dni": dni
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if 'antecedentes' in data and 'listaAni' in data:
            pdf_base64 = data['antecedentes']

            # Decode base64 PDF
            pdf_bytes = base64.b64decode(pdf_base64.split(',')[-1])  # Use [-1] to get the last part after splitting

            lista_ani = data['listaAni']

            return {
                'success': True,
                'pdf_bytes': pdf_bytes,
                'listaAni': lista_ani
            }
        else:
            return {
                'success': False,
                'mensaje_error': 'Respuesta inválida de la API'
            }

    except requests.exceptions.RequestException as e:
        print(f"Error de conexión")
        return {
            'success': False,
            'mensaje_error': f'Error de conexión'
        }
    except Exception as e:
        print(f"Error inesperado")
        return {
            'success': False,
            'mensaje_error': f'Error inesperado'
        }

def obtener_c4_azul(dni):
    url = "https://www.fakersys.com/api/v2/c4-azul"
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://fakersys.com"
    }
    payload = {
        "userId": userId,
        "dni": dni
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if 'c4' in data and 'listaAni' in data:
            pdf_base64 = data['c4']

            # Decode base64 PDF
            pdf_bytes = base64.b64decode(pdf_base64.split(',')[-1])  # Use [-1] to get the last part after splitting

            lista_ani = data['listaAni']

            return {
                'success': True,
                'pdf_bytes': pdf_bytes,
                'listaAni': lista_ani
            }
        else:
            return {
                'success': False,
                'mensaje_error': 'Respuesta inválida de la API'
            }

    except requests.exceptions.RequestException as e:
        print(f"Error de conexión")
        return {
            'success': False,
            'mensaje_error': f'Error de conexión'
        }
    except Exception as e:
        print(f"Error inesperado")
        return {
            'success': False,
            'mensaje_error': f'Error inesperado'
        }

def obtener_c4_blanco(dni):
    url = "https://www.fakersys.com/api/v2/c4-blanco"
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://fakersys.com"
    }
    payload = {
        "userId": userId,
        "dni": dni
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if 'c4' in data and 'listaAni' in data:
            pdf_base64 = data['c4']

            # Decode base64 PDF
            pdf_bytes = base64.b64decode(pdf_base64.split(',')[-1])  # Use [-1] to get the last part after splitting

            lista_ani = data['listaAni']

            return {
                'success': True,
                'pdf_bytes': pdf_bytes,
                'listaAni': lista_ani
            }
        else:
            return {
                'success': False,
                'mensaje_error': 'Respuesta inválida de la API'
            }

    except requests.exceptions.RequestException as e:
        print(f"Error de conexión")
        return {
            'success': False,
            'mensaje_error': f'Error de conexión'
        }
    except Exception as e:
        print(f"Error inesperado")
        return {
            'success': False,
            'mensaje_error': f'Error inesperado'
        }

def obtener_c4_inscripcion(dni):
    url = "https://www.fakersys.com/api/v2/c4-inscripcion"
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://fakersys.com"
    }
    payload = {
        "userId": userId,
        "dni": dni
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if 'c4' in data and 'listaAni' in data:
            pdf_base64 = data['c4']

            # Decode base64 PDF
            pdf_bytes = base64.b64decode(pdf_base64.split(',')[-1])  # Use [-1] to get the last part after splitting

            lista_ani = data['listaAni']

            return {
                'success': True,
                'pdf_bytes': pdf_bytes,
                'listaAni': lista_ani
            }
        else:
            return {
                'success': False,
                'mensaje_error': 'Respuesta inválida de la API'
            }

    except requests.exceptions.RequestException as e:
        print(f"Error de conexión")
        return {
            'success': False,
            'mensaje_error': f'Error de conexión'
        }
    except Exception as e:
        print(f"Error inesperado")
        return {
            'success': False,
            'mensaje_error': f'Error inesperado'
        }

def consultar_sentinel(dni):
    url = "https://www.fakersys.com/api/v2/sentinel"
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://fakersys.com"
    }
    payload = {
        "userId": userId,
        "dni": dni
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        return data

    except requests.exceptions.RequestException as e:
        return {}

def consultar_boleta_informativa(dni):
    url = "https://www.fakersys.com/api/v2/boleta-informativa"
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://fakersys.com"
    }
    payload = {
        "userId": userId,
        "dni": dni
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        return data

    except requests.exceptions.RequestException as e:
        return {}

def consultar_acta_nacimiento(dni):
    url = "https://www.fakersys.com/api/v2/acta-nacimiento"
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://fakersys.com"
    }
    payload = {
        "userId": userId,
        "dni": dni
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        return data

    except requests.exceptions.RequestException as e:
        return {}
    
def consultar_acta_matrimonio(dni):
    url = "https://www.fakersys.com/api/v2/acta-matrimonio"
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://fakersys.com"
    }
    payload = {
        "userId": userId,
        "dni": dni
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        return data

    except requests.exceptions.RequestException as e:
        return {}
    
def consultar_acta_defuncion(dni):
    url = "https://www.fakersys.com/api/v2/acta-defuncion"
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://fakersys.com"
    }
    payload = {
        "userId": userId,
        "dni": dni
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        return data

    except requests.exceptions.RequestException as e:
        return {}
    
def consultar_papeletas_api(dni):
    url = "https://www.fakersys.com/api/v2/papeletas"
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://fakersys.com"
    }
    payload = {
        "userId": userId,
        "dni": dni
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        return data

    except requests.exceptions.RequestException as e:
        return []

def format_papeleta_message(papeleta):
    mensaje = (
        f"*[#PeruDox]* ➜ *PAPELETA*\n\n"
        f"*PLACA:* `{papeleta.get('placa', '')}`\n"
        f"*REGLAMENTO:* `{papeleta.get('reglamento', '')}`\n"
        f"*FALA:* `{papeleta.get('fala', '')}`\n"
        f"*CÓDIGO DE PAGO:* `{papeleta.get('codigo_pago', '')}`\n"
        f"*FECHA DE EMISIÓN:* `{papeleta.get('fecha_emision', '')}`\n"
        f"*IMPORTE:* `{papeleta.get('importe', '')}`\n"
        f"*GASTOS:* `{papeleta.get('gastos', '')}`\n"
        f"*DESCUENTO:* `{papeleta.get('descuento', '')}`\n"
        f"*DEUDA:* `{papeleta.get('deuda', '')}`\n"
        f"*ESTADO:* `{papeleta.get('estado', '')}`\n"
        f"*LICENCIA DE CONDUCIR:* `{papeleta.get('licencia_de_conducir', '')}`\n"
        f"*TIPO DE DOCUMENTO:* `{papeleta.get('tipo_documento', '')}`\n"
        f"*NÚMERO DE IDENTIDAD:* `{papeleta.get('numero_identidad', '')}`\n"
    )

    return mensaje

def consultar_notas(dni):
    url = "https://www.fakersys.com/api/v2/notas"
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://fakersys.com"
    }
    payload = {
        "userId": userId,
        "dni": dni
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        return data

    except requests.exceptions.RequestException as e:
        return {}

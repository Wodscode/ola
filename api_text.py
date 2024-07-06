import requests
from io import BytesIO
from config import userId

def dniBasicoTexto(dni):
    url = 'https://www.fakersys.com/api/v2/reniec-mid'
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
        if response.status_code == 200:
            data = response.json()

            if 'nuDni' in data:
                result = {
                    'nuDni': data['nuDni'],
                    'digitoVerificacion': data.get('digitoVerificacion', ''),
                    'apePaterno': data.get('apePaterno', ''),
                    'apeMaterno': data.get('apeMaterno', ''),
                    'preNombres': data.get('preNombres', ''),
                    'sexo': data.get('sexo', ''),
                    'feNacimiento': data.get('feNacimiento', ''),
                    'nuEdad': data.get('nuEdad', ''),
                    'departamento': data.get('departamento', ''),
                    'provincia': data.get('provincia', ''),
                    'distrito': data.get('distrito', ''),
                    'estadoCivil': data.get('estadoCivil', ''),
                    'feInscripcion': data.get('feInscripcion', ''),
                    'feEmision': data.get('feEmision', ''),
                    'feCaducidad': data.get('feCaducidad', ''),
                    'nomPadre': data.get('nomPadre', ''),
                    'nomMadre': data.get('nomMadre', ''),
                    'desDireccion': data.get('desDireccion', ''),
                    'ubiReniec': data.get('ubiReniec', '')
                }

                return {
                    'success': True,
                    'data': result
                }
            else:
                return {
                    'success': False,
                    'mensaje_error': 'Respuesta inesperada: nuDni no encontrado'
                }
        else:
            return {
                'success': False,
                'mensaje_error': 'Error al consultar, código de estado: {}'.format(response.status_code)
            }
    except Exception as e:
        return {
            'success': False,
            'mensaje_error': 'Excepción al consultar: {}'.format(str(e))
        }

def consultar_nombre(name, first_name, last_name, max_age, min_age, depa):
    url = "https://www.fakersys.com/api/v2/name"
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://fakersys.com"
    }
    payload = {
        "userId": userId,
        "name": name,
        "first_name": first_name,
        "last_name": last_name,
        "max_age": max_age,
        "min_age": min_age,
        "depa": depa
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        return data

    except requests.exceptions.RequestException as e:
        return {}
def consultaHogar(dni):
    url = 'https://www.fakersys.com/api/v2/hogar'
    body = {
        "userId": userId,
        "dni": dni
    }

    headers = {
        "Content-Type": "application/json",
        "Origin": "https://fakersys.com"
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        if response.status_code == 200:
            data = response.json()

            if 'identificacion' in data:
                return {
                    'success': True,
                    'data': data
                }
            else:
                return {
                    'success': False,
                    'mensaje_error': 'Respuesta inesperada: identificacion no encontrado'
                }
        else:
            return {
                'success': False,
                'mensaje_error': 'No encontró información'
            }
    except Exception as e:
        return {
            'success': False,
            'mensaje_error': 'Excepción al consultar: {}'.format(str(e))
        }
    
def consultar_predios(dni):
    url = 'https://www.fakersys.com/api/v2/predios'
    body = {
        "userId": userId,
        "dni": dni
    }

    headers = {
        "Content-Type": "application/json",
        "Origin": "https://fakersys.com"
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        if response.status_code == 200:
            data = response.json()
            # Suponiendo que la respuesta siempre es una lista con un solo objeto
            if isinstance(data, list) and len(data) > 0:
                predio = data[0]
                result = {
                    'registro': predio.get('registro', ''),
                    'libro': predio.get('libro', ''),
                    'apPaterno': predio.get('apPaterno', ''),
                    'apMaterno': predio.get('apMaterno', ''),
                    'nombre': predio.get('nombre', ''),
                    'razonSocial': predio.get('razonSocial'),
                    'tipoDocumento': predio.get('tipoDocumento', ''),
                    'numeroDocumento': predio.get('numeroDocumento', ''),
                    'numeroPartida': predio.get('numeroPartida', ''),
                    'numeroPlaca': predio.get('numeroPlaca', ''),
                    'estado': predio.get('estado', ''),
                    'zona': predio.get('zona', ''),
                    'oficina': predio.get('oficina', ''),
                    'direccion': predio.get('direccion', '')
                }
                return {
                    'success': True,
                    'data': result
                }
            else:
                return {
                    'success': False,
                    'mensaje_error': 'No se encontraron datos de predios para el DNI proporcionado'
                }
        else:
            return {
                'success': False,
                'mensaje_error': f'Error al consultar, código de estado: {response.status_code}'
            }
    except Exception as e:
        return {
            'success': False,
            'mensaje_error': str(e)
        }
    
def consultar_numeros(dni):
    url = 'https://www.fakersys.com/api/v2/fonos'
    body = {
        "userId": userId,
        "dni": dni
    }

    headers = {
        "Content-Type": "application/json",
        "Origin": "https://fakersys.com"
    }
    try:
        response = requests.post(url, headers=headers, json=body)
        if response.status_code == 200:
            data = response.json()
            return {
                'success': True,
                'data': {
                    'dni': data['dni'],
                    'name': data['name'],
                    'surname': data['surname'],
                    'numbers': data['numbers']
                }
            }
        else:
            return {
                'success': False,
                'mensaje_error': f"Código de estado: {response.status_code}"
            }
    except Exception as e:
        return {
            'success': False,
            'mensaje_error': str(e)
        }

def consultar_familiares(dni):
    url = "https://www.fakersys.com/api/v2/familiares"
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
        if response.status_code == 200:
            data = response.json()
            return {
                'success': True,
                'familiares': data  # Asumiendo que la respuesta es una lista de familiares
            }
        else:
            return {
                'success': False,
                'mensaje_error': f"Código de estado: {response.status_code}"
            }
    except Exception as e:
        return {
            'success': False,
            'mensaje_error': str(e)
        }

def consultar_arbol(dni):
    url = "https://www.fakersys.com/api/v2/arbol"
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

    if isinstance(data, list) and all('nuDni' in fam for fam in data):
        return {
            'success': True,
            'familiares': data
        }
    else:
        return {
            'success': False,
            'mensaje_error': data.get('deRespuesta', 'Error desconocido')
        }
    
def consultar_hermanos(dni):
    url = "https://www.fakersys.com/api/v2/hermanos"
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

    if isinstance(data, list) and all('nuDni' in hermano for hermano in data):
        return {
            'success': True,
            'hermanos': data
        }
    else:
        return {
            'success': False,
            'mensaje_error': data.get('deRespuesta', 'Error desconocido')
        }

def consultar_bitel(dni):
    url = "https://www.fakersys.com/api/v2/bitel"
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

    if isinstance(data, list) and all('number' in bitel for bitel in data):
        return {
            'success': True,
            'bitel': data
        }
    else:
        return {
            'success': False,
            'mensaje_error': data.get('deRespuesta', 'Error desconocido')
        }
    
def consultar_claro(dni):
    url = "https://www.fakersys.com/api/v2/claro"
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

    if isinstance(data, list) and all('celular' in claro for claro in data):
        return {
            'success': True,
            'claro': data
        }
    else:
        return {
            'success': False,
            'mensaje_error': data.get('deRespuesta', 'Error desconocido')
        }
    
def consultar_placas(dni):
    url = "https://www.fakersys.com/api/v2/placas"
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
        data = response.json()

        if 'numPlaca' in data:
            return {
                'success': True,
                'placa': data
            }
        else:
            return {
                'success': False,
                'mensaje_error': data.get('deRespuesta', 'Error desconocido')
            }
    except Exception as e:
        return {
            'success': False,
            'mensaje_error': str(e)
        }

def consultar_correo(dni):
    url = "https://www.fakersys.com/api/v2/correos"
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
        return {'success': False, 'mensaje_error': f"Error de conexión: {str(e)}"}
    except ValueError:
        return {'success': False, 'mensaje_error': "Error al parsear la respuesta JSON"}

    if data and isinstance(data, list) and len(data) > 0:
        correos = [{'dni': item.get('dni', 'N/A'), 'correo': item.get('correo', 'N/A')} for item in data]
        return {
            'success': True,
            'correos': correos
        }
    else:
        return {
            'success': False,
            'mensaje_error': 'Datos de correo no disponibles'
        }
    
def consultar_sueldos(dni):
    url = "https://www.fakersys.com/api/v2/sueldos"
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
        
        if data and isinstance(data, list) and len(data) > 0:
            return {
                'success': True,
                'sueldos': data
            }
        else:
            return {
                'success': False,
                'mensaje_error': 'No se encontraron datos de sueldos para el DNI proporcionado.'
            }

    except requests.exceptions.RequestException as e:
        return {'success': False, 'mensaje_error': str(e)}
    
def consultar_sbs(dni):
    url = "https://www.fakersys.com/api/v2/sbs"
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
        
        if data and isinstance(data, list) and len(data) > 0:
            return {
                'success': True,
                'sbs_info': data
            }
        else:
            return {
                'success': False,
                'mensaje_error': 'No se encontraron datos de SBS para el DNI proporcionado.'
            }

    except requests.exceptions.RequestException as e:
        return {'success': False, 'mensaje_error': str(e)}

def consultar_geo(ip):
    url = "https://www.fakersys.com/api/v2/geo"
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://fakersys.com"
    }
    payload = {
        "userId": userId,
        "geo": ip
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        
        if data and isinstance(data, list) and len(data) > 0:
            return {
                'success': True,
                'geo_info': data[0]  # Tomamos solo el primer elemento de la lista de respuestas
            }
        else:
            return {
                'success': False,
                'mensaje_error': 'No se encontraron datos de geolocalización para la IP proporcionada.'
            }

    except requests.exceptions.RequestException as e:
        return {'success': False, 'mensaje_error': str(e)}

def consultar_ruc(ruc):
    url = "https://www.fakersys.com/api/v2/ruc"
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://fakersys.com"
    }
    payload = {
        "userId": userId,
        "ruc": ruc
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if data and isinstance(data, dict):
            return {
                'success': True,
                'data': data
            }
        else:
            return {
                'success': False,
                'mensaje_error': 'Respuesta inválida de la API'
            }

    except requests.exceptions.RequestException as e:
        return {'success': False, 'mensaje_error': str(e)}
    except ValueError:
        return {'success': False, 'mensaje_error': "Error al parsear la respuesta JSON"}
    except Exception as e:
        return {'success': False, 'mensaje_error': f"Error inesperado: {str(e)}"}

def consultar_sunedu(dni):
    url = "https://www.fakersys.com/api/v2/sunedu"
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
        
        if data and isinstance(data, list):
            mensaje = "*[#PeruDox]* ➜ *INFORMACIÓN ACADÉMICA SUNEDU*\n\n"
            for info in data:
                mensaje += (
                    f"*Nombres:* `{info['nombres']}`\n"
                    f"*Apellidos:* `{info['apellidos']}`\n"
                    f"*DNI:* `{info['dni']}`\n"
                    f"*Universidad:* `{info['nomUni']}`\n"
                    f"*Grado Académico:* `{info['gradoAca']}`\n"
                    f"*Denominación:* `{info['denominacion']}`\n"
                    f"*Fecha de Expedición:* `{info['feExpedicion']}`\n"
                    f"*Acta:* `{info['acta']}`\n"
                    f"*Diploma:* `{info['diploma']}`\n"
                    f"*Fecha de Matrícula:* `{info['feMatricula']}`\n"
                    f"*Fecha de Egreso:* `{info['feEgreso']}`\n\n"
                )
            
            return {
                'success': True,
                'mensaje': mensaje
            }
        else:
            return {
                'success': False,
                'mensaje_error': 'Respuesta inválida de la API'
            }

    except requests.exceptions.RequestException as e:
        return {'success': False, 'mensaje_error': str(e)}

def verificar_numeros(dni):
    url = "https://www.fakersys.com/api/v2/verifica"
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
        
        if data and isinstance(data, list):
            mensaje = "*[#PeruDox]* ➜ *VERIFICACIÓN DE NÚMEROS TELEFÓNICOS*\n\n"
            for info in data:
                mensaje += (
                    f"*Número:* `{info['number']}****`\n"
                    f"*Operador:* `{info['operator']}`\n"
                    f"*Plan:* `{info['plan']}`\n\n"
                )
            
            return {
                'success': True,
                'mensaje': mensaje
            }
        else:
            return {
                'success': False,
                'mensaje_error': 'Respuesta inválida de la API'
            }

    except requests.exceptions.RequestException as e:
        return {'success': False, 'mensaje_error': str(e)}

def consultar_migraciones(dni):
    url = "https://www.fakersys.com/api/v2/migraciones"
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

        if data and isinstance(data, dict):
            return {
                'success': True,
                'data': data
            }
        else:
            return {
                'success': False,
                'mensaje_error': 'Respuesta inválida de la API'
            }

    except requests.exceptions.RequestException as e:
        return {'success': False, 'mensaje_error': str(e)}

def consultar_mininter(dni):
    url = "https://www.fakersys.com/api/v2/mininter"
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

        if data and isinstance(data, dict):
            return {
                'status': data.get('status', False),
                'nuDni': data.get('nuDni', ''),
                'preNomres': data.get('preNomres', ''),
                'apePaterno': data.get('apePaterno', ''),
                'apeMaterno': data.get('apeMaterno', '')
            }
        else:
            return {'status': False}

    except requests.exceptions.RequestException as e:
        return {'status': False}

def consultar_carnet_extranjeria(dni):
    url = "https://www.fakersys.com/api/v2/carnet-extranjeria"
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

        if data and isinstance(data, dict):
            return {
                'nombres': data.get('nombres', ''),
                'primerApellido': data.get('primerApellido', ''),
                'segundoApellido': data.get('segundoApellido', ''),
                'calidadMigratoria': data.get('calidadMigratoria', '')
            }
        else:
            return {'nombres': ''}

    except requests.exceptions.RequestException as e:
        return {'nombres': ''}

def consultar_mpfn(dni):
    url = "https://www.fakersys.com/api/v2/mpfn"
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

        casos = data.get('casos', [])
        libre = data.get('libre', [])

        return {
            'casos': casos,
            'libre': libre
        }

    except requests.exceptions.RequestException as e:
        return {'casos': [], 'libre': []}

def consultar_movistar(dni):
    url = "https://www.fakersys.com/api/v2/movistar"
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

def consultar_bolivia(dni):
    url = "https://www.fakersys.com/api/v2/bolivia"
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
    
def consultar_licencia(dni):
    url = "https://www.fakersys.com/api/v2/licencia-mtc"
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

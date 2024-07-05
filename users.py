from flask import Flask, request, jsonify, redirect
from pymongo import MongoClient
import time
import json
from flask_cors import CORS
import requests
from telegram import Bot
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)
client = MongoClient("mongodb+srv://thikhabot:h4inj4I5STCtpHF5@thikhadox.bdmbaay.mongodb.net/?retryWrites=true&w=majority")
db = client.keys
keys_collection = db.keys
data_collection = db.data
ip_collection = db.ip_collection
customers_collection = db.customers

def autenticar_solicitud():
    # Solo intercepta las solicitudes que no son OPTIONS
    if request.method != 'OPTIONS':
        token = request.headers.get('Authorization')
        if token != 'Bearer efiaf39H8G34h89eeca00ICK00D0EKF020ekcwekq-9J39FDJ0fvw-9J39FJQ9S0q0ejf2csEF9JE':
            return jsonify({'error': 'Intenta de nuevo'}), 401

@app.before_request
def verificar_autenticacion():
    return autenticar_solicitud()

@app.route('/register_customer', methods=['POST'])
def register_customer():
    try:
        telegram_id = request.json['telegram_id']
        name = request.json['name']
        credits = 5
        role = 'CLIENTE'
        plan = 'FREE'
        status = 'ACTIVO'
        antispam = 90
        join_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        end_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        last_query = 0
        querys = 0
        existing_customer = customers_collection.find_one({'telegram_id': telegram_id})
        if existing_customer:
            return jsonify({'message': 'Customer already registered'}), 400

        customer_doc = {
            'telegram_id': telegram_id,
            'name': name,
            'credits': credits,
            'role': role,
            'plan': plan,
            'status': status,
            'antispam': antispam,
            'join_date': join_date,
            'end_date': end_date,
            'last_query': last_query,
            'querys': querys
        }
        customers_collection.insert_one(customer_doc)
        return jsonify({'message': 'Customer registered successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add_credits', methods=['POST'])
def add_credits():
    try:
        user_id = request.json['user_id']
        amount = request.json['amount']

        customer = customers_collection.find_one({'telegram_id': user_id})
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404

        if amount < 1:
            plan = 'FREE'
            antispam = 30
        if amount < 500:
            plan = 'BASICO'
            antispam = 20
        elif amount < 799:
            plan = 'ESTANDAR'
            antispam = 15
        else:
            plan = 'PREMIUN'    
            antispam = 10

        customers_collection.update_one(
            {'telegram_id': user_id},
            {
                '$set': {
                    'credits': amount,
                    'plan': plan,
                    'antispam': antispam
                }
            }
        )

        return jsonify({'message': 'Credits added successfully', 'new_credits': amount, 'plan': plan, 'antispam': antispam}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/more_credits', methods=['POST'])
def more_credits():
    try:
        # Obtener datos del cuerpo JSON
        data = request.json
        user_id = data['user_id']
        amount = data['amount']

        # Actualizar créditos del usuario
        customer = customers_collection.find_one({'telegram_id': user_id})
        if customer:
            new_credits = customer['credits'] + amount
            customers_collection.update_one({'telegram_id': user_id}, {'$set': {'credits': new_credits}})
            return jsonify({'message': f"Se agregaron {amount} créditos al usuario {user_id}"}), 200
        else:
            return jsonify({'error': f"Usuario con ID {user_id} no encontrado"}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/rest_credits', methods=['POST'])
def rest_credits():
    try:
        # Obtener datos del cuerpo JSON
        data = request.json
        user_id = data['user_id']
        amount = data['amount']

        # Actualizar créditos del usuario
        customer = customers_collection.find_one({'telegram_id': user_id})
        if customer:
            new_credits = customer['credits'] - amount
            customers_collection.update_one({'telegram_id': user_id}, {'$set': {'credits': new_credits}})
            return jsonify({'message': f"Se restaron {amount} créditos al usuario {user_id}"}), 200
        else:
            return jsonify({'error': f"Usuario con ID {user_id} no encontrado"}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add_days', methods=['POST'])
def add_days():
    try:
        user_id = request.json['user_id']
        days_to_add = request.json['days']

        customer = customers_collection.find_one({'telegram_id': user_id})
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404
        
        # Obtener la fecha de finalización actual o establecerla a hoy si no existe
        current_end_date = customer.get('end_date')
        if current_end_date:
            end_date = datetime.now()

        # Agregar los días
        new_end_date = end_date + timedelta(days=days_to_add)
        new_end_date_str = new_end_date.strftime('%Y-%m-%d %H:%M:%S')

        customers_collection.update_one(
            {'telegram_id': user_id},
            {
                '$set': {
                    'end_date': new_end_date_str,
                }
            }
        )

        return jsonify({'message': 'Days added successfully', 'new_end_date': new_end_date_str}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/more_days', methods=['POST'])
def more_days():
    try:
        data = request.json
        user_id = data['user_id']
        days = data['days']

        customer = customers_collection.find_one({'telegram_id': user_id})
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404
        
        if days < 1:
            plan = 'FREE'
            antispam = 30
        if days < 7:
            plan = 'VIP'
            antispam = 15
        elif days < 15:
            plan = 'VIP'
            antispam = 15
        elif days < 30:
            plan = 'PREMIUM'
            antispam = 15
        elif days < 60:
            plan = 'GOLD'
            antispam = 10        
        else:
            plan = 'GOLD'    
            antispam = 10
        # Obtener la fecha de finalización actual
        end_date_str = customer.get('end_date')
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d %H:%M:%S')
        else:
            end_date = datetime.now()
        
        # Agregar días a la fecha de finalización
        new_end_date = end_date + timedelta(days=days)
        new_end_date_str = new_end_date.strftime('%Y-%m-%d %H:%M:%S')

        customers_collection.update_one(
            {'telegram_id': user_id},
            {
                '$set': {
                    'end_date': new_end_date_str,
                    'plan': plan,
                    'antispam': antispam
                }
            }
        )

        return jsonify({'message': 'Days added successfully', 'new_end_date': new_end_date_str}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/anti_spam', methods=['POST'])
def anti_spam():
    try:
        user_id = request.json['user_id']
        amount = request.json['amount']

        customer = customers_collection.find_one({'telegram_id': user_id})
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404

        customers_collection.update_one(
            {'telegram_id': user_id},
            {
                '$set': {
                    'antispam': amount,
                }
            }
        )

        return jsonify({'message': 'Anti-spam actualizado a ', 'antispam': amount}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/update_last_query_time', methods=['POST'])
def update_last_query_time():
    try:
        data = request.json
        telegram_id = data['telegram_id']
        current_time = int(time.time())

        customers_collection.update_one(
            {'telegram_id': telegram_id},
            {'$set': {'last_query': current_time}}
        )
        return jsonify({'message': 'Last query time updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/increment_queries', methods=['POST'])
def increment_queries():
    try:
        data = request.json
        telegram_id = data['telegram_id']

        customers_collection.update_one(
            {'telegram_id': telegram_id},
            {'$inc': {'query': 1}}
        )
        return jsonify({'message': 'Query count incremented successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add_seller', methods=['POST'])
def add_seller():
    try:
        data = request.json
        telegram_id = data['telegram_id']

        customers_collection.update_one(
            {'telegram_id': telegram_id},
            {'$set': {'role': 'SELLER'}}
        )
        return jsonify({'message': 'Role updated to SELLER successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/rem_seller', methods=['POST'])
def rem_seller():
    try:
        data = request.json
        telegram_id = data['telegram_id']

        customers_collection.update_one(
            {'telegram_id': telegram_id},
            {'$set': {'role': 'CLIENTE'}}
        )
        return jsonify({'message': 'Role updated to CLIENTE successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/change_role', methods=['POST'])
def change_role():
    try:
        data = request.json
        user_id = data['user_id']
        role_id = data['role_id']
        
        roles = {
            1: 'OWNER',
            2: 'SELLER',
            3: 'CLIENTE'
        }
        
        if role_id not in roles:
            return jsonify({'error': 'Invalid role ID'}), 400

        customers_collection.update_one(
            {'telegram_id': user_id},
            {'$set': {'role': roles[role_id]}}
        )
        return jsonify({'message': 'Role updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# @app.route('/delete_all_customers', methods=['DELETE'])
# def delete_all_customers():
#     try:
#         result = customers_collection.delete_many({})
#         return jsonify({'message': f'Se eliminaron {result.deleted_count} documentos de customers'}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

    # current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # # Actualiza end_date para todos los usuarios registrados
    # customers_collection.update_many(
    #     {},
    #     {
    #         '$set': {
    #             'end_date': current_datetime
    #         }
    #     }
    # )
if __name__ == '__main__':
    
    app.run(host='0.0.0.0',port=80)



#USAR PARA INSTALAR LAS LIBRERIAS NECESARIAS 
#pip install -r requirements.txt
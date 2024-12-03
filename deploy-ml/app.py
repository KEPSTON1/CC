from flask import Flask, request, jsonify
from functools import wraps
import pandas as pd
from tensorflow.keras.models import load_model
import numpy as np
import jwt
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# untuk load file env
load_dotenv()

app = Flask(__name__)

SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret')  

model = load_model('mindcare_model.h5')  

DB_CONFIG = {
    'host': os.getenv('DB_HOST', '34.50.81.43'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'capstone12'),
    'database': os.getenv('DB_NAME', 'capstone')
}

def create_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def authenticate_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Unauthorized, token missing'}), 401

        try:
            token = token.split(' ')[1] 
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.id_usertoken = decoded_token['id_user']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Expired token'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

        return f(*args, **kwargs)
    return decorated_function

def get_level(skor, kategori):
    thresholds = {
        'Depresi': [9, 13, 20, 27],
        'Kecemasan': [7, 9, 14, 19],
        'Stres': [14, 18, 25, 33]
    }
    
    if kategori not in thresholds:
        return "Invalid category"

    thresholds_values = thresholds[kategori]

    if skor <= thresholds_values[0]:
        return "Normal"
    elif skor <= thresholds_values[1]:
        return "Ringan"
    elif skor <= thresholds_values[2]:
        return "Sedang"
    elif skor <= thresholds_values[3]:
        return "Parah"
    else:
        return "Sangat Parah"

def calculate_scores_and_categories(data):
    depresi_cols = [3, 5, 10, 13, 16, 17, 21, 24, 26, 31, 34, 37, 38, 42]
    kecemasan_cols = [2, 4, 7, 9, 15, 19, 20, 23, 25, 28, 30, 36, 40, 41]
    stres_cols = [1, 6, 8, 11, 12, 14, 18, 22, 27, 29, 32, 33, 35, 39]

    depresi_cols = [col - 1 for col in depresi_cols]
    kecemasan_cols = [col - 1 for col in kecemasan_cols]
    stres_cols = [col - 1 for col in stres_cols]

    valid_depresi_cols = [col for col in depresi_cols if col < data.shape[1]]
    valid_kecemasan_cols = [col for col in kecemasan_cols if col < data.shape[1]]
    valid_stres_cols = [col for col in stres_cols if col < data.shape[1]]

    data['Skor_Depresi'] = data.iloc[:, valid_depresi_cols].sum(axis=1)
    data['Skor_Kecemasan'] = data.iloc[:, valid_kecemasan_cols].sum(axis=1)
    data['Skor_Stres'] = data.iloc[:, valid_stres_cols].sum(axis=1)

    return data

def process_data(input_data):
    df = pd.DataFrame([input_data])
    df = calculate_scores_and_categories(df)
    if df.shape[1] < 48:
        df = pd.concat([df, pd.DataFrame(np.zeros((df.shape[0], 48 - df.shape[1])), columns=[f'Feature_{i}' for i in range(df.shape[1], 48)])], axis=1)
    return df

def get_user_from_db(user_id):
    try:
        connection = create_db_connection()
        if connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                result = cursor.fetchone()
            return result
        else:
            return None
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None
    finally:
        if connection and connection.is_connected():
            connection.close()

@app.route('/')
def home():
    return jsonify({"message": "Mindcare Good"})

@app.route('/predict', methods=['POST'])
@authenticate_user
def ukur_skala():
    data = request.json

    if not data:
        return jsonify({"error": "Harap sertakan JSON berisi jawaban kuisioner."}), 400

    try:
        user_data = get_user_from_db(request.id_usertoken)

        hasil = process_data(data)
        input_for_model = hasil[['Skor_Depresi', 'Skor_Kecemasan', 'Skor_Stres']].values

        if input_for_model.shape[1] != 48:
            input_for_model = np.concatenate([input_for_model, np.zeros((input_for_model.shape[0], 48 - input_for_model.shape[1]))], axis=1)

        predictions = model.predict(input_for_model)
        predicted_depresi = float(predictions[0][0])
        predicted_kecemasan = float(predictions[0][1])
        predicted_stres = float(predictions[0][2])

        result = {
            'Skor_Depresi': int(hasil['Skor_Depresi'].iloc[0]),
            'Kategori_Depresi': get_level(hasil['Skor_Depresi'].iloc[0], 'Depresi'),
            'Prediksi_Depresi': predicted_depresi,
            'Skor_Kecemasan': int(hasil['Skor_Kecemasan'].iloc[0]),
            'Kategori_Kecemasan': get_level(hasil['Skor_Kecemasan'].iloc[0], 'Kecemasan'),
            'Prediksi_Kecemasan': predicted_kecemasan,
            'Skor_Stres': int(hasil['Skor_Stres'].iloc[0]),
            'Kategori_Stres': get_level(hasil['Skor_Stres'].iloc[0], 'Stres'),
            'Prediksi_Stres': predicted_stres
        }

        connection = create_db_connection()
        if connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO histori (user_id, skor_depresi, kategori_depresi, prediksi_depresi, 
                        skor_kecemasan, kategori_kecemasan, prediksi_kecemasan, skor_stres, kategori_stres, prediksi_stres)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    request.id_usertoken, result['Skor_Depresi'], result['Kategori_Depresi'], predicted_depresi,
                    result['Skor_Kecemasan'], result['Kategori_Kecemasan'], predicted_kecemasan,
                    result['Skor_Stres'], result['Kategori_Stres'], predicted_stres
                ))
                connection.commit()

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Error during processing: {str(e)}"}), 500

@app.route('/history', methods=['GET'])
@authenticate_user
def get_history():
    try:
        connection = create_db_connection()
        if connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute("""
                    SELECT id, skor_depresi, kategori_depresi, prediksi_depresi, 
                           skor_kecemasan, kategori_kecemasan, prediksi_kecemasan, 
                           skor_stres, kategori_stres, prediksi_stres, created_at
                    FROM histori
                    WHERE user_id = %s
                    ORDER BY created_at DESC
                """, (request.id_usertoken,))
                history = cursor.fetchall()

            return jsonify({'history': history})

    except Exception as e:
        return jsonify({"error": f"Error fetching history: {str(e)}"}), 500
    finally:
        if connection and connection.is_connected():
            connection.close()
            
@app.route('/delete/<int:id>', methods=['DELETE'])
@authenticate_user
def delete_histori(id):
    try:
        connection = create_db_connection()
        if connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM histori WHERE id = %s AND user_id = %s
                """, (id, request.id_usertoken))
                record = cursor.fetchone()
                
                if not record:
                    return jsonify({"error" : "Data is Undefined"}), 404
                
                cursor.execute("DELETE FROM histori WHERE id = %s", (id,))
                connection.commit()
                
                return jsonify({"message": f"Data with id {id} successful deleted"})
        else:
            return jsonify({"message": "Failed connect to database"}), 500
    except Exception as e:
        return jsonify({"message": f"False: {str(e)}"}), 500
    finally:
        if connection and connection.is_connected():
            connection.close()


if __name__ == '__main__':
    app.run(debug=True)

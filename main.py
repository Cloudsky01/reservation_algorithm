import functions_framework
from flask import Flask, request
from utilities import visualize_solution_plot
from optimizer import getOptimizedSheet
from classes import Sheet
import json

import firebase_admin
from firebase_admin import credentials, auth

# Add private key to the project root directory
cred = credentials.Certificate('./privatekey.json')
firebase_admin.initialize_app(cred)

@functions_framework.http
def schedule():
    id_token = request.headers.get('Authorization').split('Bearer ')[1]
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
    except ValueError:
        # Token is invalid
        return "Unauthorized", 401
    try:
        sheet_data = request.get_json()
        sheet = Sheet(sheet_data)
        solution =  getOptimizedSheet(sheet)
        visualize_solution_plot(sheet.reservations, solution, len(sheet.rooms))
        #untested
        output = {}
        for i, reservation in enumerate(sheet.reservations):
            output[reservation.id] = [sheet.rooms[r] for r in range(len(sheet.rooms)) if solution[i][r] == 1 ]
        return json.dumps(output)
    except Exception as e:
        return str(e)




# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn
from firebase_admin import initialize_app
from utilities import visualize_solution_plot
from optimizer import getOptimizedSheet
from classes import Sheet
import json

@https_fn.on_request()
def schedule(request: https_fn.Request) -> https_fn.Response:
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
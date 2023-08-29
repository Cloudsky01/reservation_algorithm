import functions_framework
from flask import Flask, request
from utilities import visualize_solution_plot
from optimizer import getOptimizedSheet
from classes import Sheet
import json

app = Flask(__name__)


@functions_framework.http
def schedule():
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




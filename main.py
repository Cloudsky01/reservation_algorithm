import functions_framework
from flask import jsonify
from optimizer import getOptimizedSheet
from classes import Sheet
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR)

def cors_headers():
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }

@functions_framework.http
def schedule(request):
    # Handle OPTIONS request for CORS preflight
    if request.method == 'OPTIONS':
        return ('', 204, cors_headers())
    
    # Main request
    try:
        sheet_data = request.get_json()
        if not sheet_data:
            raise ValueError("No input data provided")
        sheet = Sheet(sheet_data)
        logging.debug("Processing request for tenant %s", sheet.tenant)
        solution = getOptimizedSheet(sheet)
        output = {}
        for i, reservation in enumerate(sheet.reservations):
            output[reservation.id] = [sheet.rooms[r] for r in range(len(sheet.rooms)) if solution[i][r] == 1]

        return (jsonify(output), 200, cors_headers())

    except Exception as e:
        logging.error("Failed to process request", exc_info=True)
        logging.debug("Request data: %s", sheet_data if 'sheet_data' in locals() else "N/A")
        
        return (str(e), 500, cors_headers())

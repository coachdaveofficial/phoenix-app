from flask import Blueprint, jsonify, make_response, request
from blueprints.auth.auth import login_required
from script import SeasonDataExtractor


script_bp = Blueprint("script", __name__)

extractor = SeasonDataExtractor("phoenix-fc-sheets-COPY.json", "Copy of Phoenix Historical Stats")

# extractor.insert_data([{'worksheet': "Spring 2023 Open", "year": "2023", "season": "Spring", "team_type": "Open"}])

@script_bp.route('/script/', methods=["POST"])
@login_required
def run_script():

    worksheet_data = request.get_json()
    
    response = extractor.insert_data([worksheet_data])
    print(response)

    # if POST request unsuccessful, response will look something like: {"status": {"success": False, "message": f'{e} is not a valid worksheet name', "worksheet_error": True}}
    if not response['status']['success']:
        if response['status']['worksheet_error']:
            return make_response({"message": f"Error inserting worksheet data, please check your worksheet info and try again. Error: {response['status']['message']}"}, 400)
        
        return make_response({"message": f"Error inserting worksheet data, please check your worksheet info and try again. Error: {response['status']['message']} was not provided."}, 400)
    
    # if successful, response will look like: {"status": {"success": False, "message": f'{e} is not a valid worksheet name'}}
    return make_response({"message": response['status']['message']}, 201)
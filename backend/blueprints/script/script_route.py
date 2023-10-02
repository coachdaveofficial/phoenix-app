from flask import Blueprint, jsonify, make_response, request
from blueprints.auth.auth import login_required
from script import SeasonDataExtractor
from flask_cors import cross_origin

script_bp = Blueprint("script", __name__)

extractor = SeasonDataExtractor("phoenix-fc-sheets-COPY.json", "Copy of Phoenix Historical Stats")

# extractor.insert_data([{'worksheet': 
# "Spring 2023 Open", 
# "year": "2023", 
# "season": "Spring", 
# "team_type": "Open"}])

@script_bp.route('/script/', methods=["POST"])
@cross_origin(supports_credentials=True)
def run_script():
    # worksheet_data will look like {'worksheet': 'Spring 2023 Open', 'year': '2023', 'season': 'Spring', 'team_type': 'Open'}
    worksheet_data = request.get_json()
    print(worksheet_data)
    year = worksheet_data.get('year')
    try:
        year = int(year)
    except ValueError:
        return make_response({"message": f"Error inserting worksheet data, please check your worksheet info and try again. Error message: year was not in correct format, please ensure that year is 4 digits long and only consists of numbers"}, 400)
    if year < 2010:
        return make_response({"message": f"Error inserting worksheet data, please check your worksheet info and try again. Error message: year was not in correct format, please ensure that year is 4 digits long and only consists of numbers"}, 400)
    
    response = extractor.insert_data([worksheet_data])
    print(response)

    # if POST request unsuccessful, response will look something like: {"status": {"success": False, "message": f'{e} is not a valid worksheet name', "worksheet_error": True}}
    if not response['status']['success']:
        if response['status']['worksheet_error']:
            return make_response({"message": f"Error inserting worksheet data, please check your worksheet info and try again. Error message: {response['status']['message']}"}, 400)
        
        return make_response({"message": f"Error inserting worksheet data, please check your worksheet info and try again. Error message: {response['status']['message']} was not provided."}, 400)
    
    # if successful, response will look like: {"status": {"success": False, "message": f'{e} is not a valid worksheet name'}}
    return make_response({"message": response['status']['message']}, 201)
from flask import Flask, request, jsonify
import logging
from patient_class import Patient
from pymongo import MongoClient

app = Flask(__name__)


@app.route("/new_patient", methods=["POST"])
def post_new_patient():
    """
    Adds test to a specific patient 

    This route is used to receive testing data
    for a specific patient and add that test result to the patient.
    The input to this route should be a dictioanry as the following 
    example:
    
    {"id": <int>, "name": <str>", "blood_type": <str>}
    """
    # Get the input data
    in_data = request.get_json()
    # Validate the input
    expected_keys = ["name", "id", "blood_type"]
    expected_types = [str, int, str]
    check_results = validate_post_input(in_data, expected_keys, expected_types)
    if check_results is not True:
        return check_results, 400
    # Call helper functions to implement the route
    add_patient_to_db(in_data)
    # Return a reponse
    logging.info("Entry added {}".format(in_data))
    answer = {"message": "Patient added", "data": in_data}
    return jsonify(answer), 200


@app.route("/add_test", methods=["POST"])
def post_add_test():
    in_data = request.get_json()
    expected_keys = ["id", "test_name", "test_result"]
    expected_types = [int, str, int]
    check_test = validate_post_input(in_data, expected_keys, expected_types)
    if check_test is not True:
        return check_test, 400
    result = add_test_to_patient(in_data)
    if result is not True:
        return result, 400
    return "Patient added", 200


def add_test_to_patient(in_data):
    patient = get_patient(in_data["id"])
    if patient is False:
        return "Patient not found"
    patient.add_test_result(in_data["test_name"], in_data["test_result"])
    patient.save()
    return True


def get_patient(mrn):
    patient = Patient.get_patient_from_db(mrn)
    if patient is None:
        return False
    else:
        return patient


@app.route("/get_results/<patient_id>", methods=["GET"])
def get_results():
    results = create_output()

def validate_post_input(in_data, expected_keys, expected_types):
    # check keys that you are expecting exists and the variable
    # types are what you are expecting
    for ex_key, ex_type in zip(expected_keys, expected_types):
        if ex_key not in in_data:
            return "Key {} is not found in input".format(ex_key)
        if type(in_data[ex_key]) is not ex_type:
            return ("the value for key {} is not the expected type of is not "
                    " the requested type of {}.".format(ex_key, ex_type))
    return True


def add_patient_to_db(in_data):
    first_name, last_name = in_data["name"].split(" ")
    new_patient = Patient(first_name, last_name, in_data["id"],
                          blood_type=in_data["blood_type"])
    new_patient.save()


def initialize_server():
    logging.basicConfig(filename="healt_db_server.log", filemode='w', level=logging.INFO)
    add_patient_to_db({"name": "Ann Ables", "id": 1, "blood_type": "A+"})


def connect_to_db():
    print("Connecting to database...")
    url = "mongodb+srv://KyUser:#Dancer*29@bme547.efj9u.mongodb.net/?retryWrites=true&w=majority&appName=BME547"
    Patient.client = MongoClient(url)
    Patient.database = Patient.client["Class_Database"]
    Patient.collection = Patient.database["Patients"]


if __name__ == "__main__":
    initialize_server()
    app.run()

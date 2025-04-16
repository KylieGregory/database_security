from health_db_server import app, connect_to_db
from patient_class import Patient
client = app.test_client() # use to make requets to a mock server
connect_to_db()


def test_post_new_patient():
    Patient.clear_database()
    test_patient = {
        "name": "Patient Zero",
        "id": 123,
        "blood_type": "O+"
    }
    r = client.post("/new_patient", json=test_patient)
    assert r.status_code == 200
    assert r.json["message"] == "Patient added"
    added_patient = Patient.get_patient_from_db(123)
    assert added_patient.blood_type == "O+"


def test_post_new_patient_bad_key():
    Patient.clear_database()
    test_patient = {
        "naaame": "Patient Zero",
        "id": 123,
        "blood_type": "O+"
    }
    r = client.post("/new_patient", json=test_patient)
    assert r.status_code == 400
    assert r.text == "Key name is not found in input"
    added_patient = Patient.get_patient_from_db(123)
    assert added_patient is None

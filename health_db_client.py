import requests

server = "http://127.0.0.1:5000"

patient_data = {"name": "Kylie Gregory", "id": 120, "blood_type": "O+"}
r = requests.post(server + "/new_patient", json=patient_data)
print(r.status_code)
print(r.text)


patient_data = {"name": "David Ward", "id": 123, "blood_type": "O+"}
r = requests.post(server + "/new_patient", json=patient_data)
print(r.status_code)
print(r.text)


test_data = {"id": int, "test_name": str, "test_result": int}
r = requests.post(server + "/add_test", json=test_data)
print(r.status_code)
print(r.text)


r = requests.get(server + "/get_results/<120>")
print(r.status_code)
print(r.text)

from fastapi import FastAPI, HTTPException, Query
import json
app = FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

@app.get("/")
def hello():
    return {"message": "patient management system API"}

@app.get('/about')
def about():
    return {"message": "A full management system for patient records."}

@app.get('/view')
def view():
    data = load_data()
    return data 

@app.get('/patirnt/{patient_id}')
def get_patient(patient_id: int):
    data = load_data()
    for patient in data:
        if patient['id'] == patient_id:
            return patient
    return {"error": "Patient not found"}

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str=Query(..., description="The ID of the patient in DB; e.g., 1")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get('/sort0/')
def sort_patients(sort_by: str=Query(..., description='sort on the basis of height, weight, or bmi')):
    data       = load_data()
    sorted_data = sorted(data, key=lambda x: x[sort_by] if sort_by in x else 0)
    return sorted_data

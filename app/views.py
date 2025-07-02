import os
from django.http import JsonResponse
from django.shortcuts import render, redirect
import requests
import json
from .patient import Patient
from django.core.paginator import Paginator
from django.contrib import messages
from datetime import datetime

def index(request):
    context = {}
    return render(request, 'app/index.html', context)

def create_patient(request):
    if request.method == 'POST':
        try:
            data = {
                'resourceType':"Patient",
                "name": [
                    {
                        "given": [request.POST.get('given_name')],
                        "family": request.POST.get('family_name')
                    }
                ],
                "gender": request.POST.get('gender'),
                "telecom": [
                    {
                        "system": "phone", 
                        "value": request.POST.get('phone'), 
                        "use": "mobile"
                    }                  
                ],
                "birthDate": request.POST.get('date_of_birth')
            }

            json_data = json.dumps(data)
            
            headers = {
                'accept':"application/json",
                'Content-Type':"application/json",
                'Cache-Control':'no-cache'
            }

            create_patients_url = "https://hapi.fhir.org/baseR4/Patient"

            response = requests.post(create_patients_url, headers=headers, data=json_data)

            print(response.text)
            messages.success(request, "Patient created successfully. (" + response.json()['id'] + ")")
        except Exception as err:
            messages.error(request, "Error creating Patient : " + str(err))
            
        return redirect('app:create-patient')
    else:
        today = datetime.now()
        context = {
            'today': today
        }
        return render(request, 'app/create-patient.html', context)

def update_patient(request, patient_id):
    if request.method == 'POST':
        try:
            data = {
                'resourceType':"Patient",
                'id': patient_id,
                "name": [
                    {
                        "given": [request.POST.get('given_name')],
                        "family": request.POST.get('family_name')
                    }
                ],
                "gender": request.POST.get('gender'),
                "telecom": [
                    {
                        "system": "phone", 
                        "value": request.POST.get('phone'), 
                        "use": "mobile"
                    }                  
                ],
                "birthDate": request.POST.get('date_of_birth')
            }

            json_data = json.dumps(data)
            print(json_data)
            headers = {
                'accept':"application/json",
                'Content-Type':"application/json",
                'Cache-Control':'no-cache'
            }

            upate_patients_url = "https://hapi.fhir.org/baseR4/Patient/" + patient_id

            response = requests.put(upate_patients_url, headers=headers, data=json_data)

            messages.success(request, "Patient updated successfully. (" + patient_id + ")")
        except Exception as err:
            messages.error(request, "Error creating Patient : " + str(err))
            
        return redirect('app:update-patient',patient_id=patient_id)
    else:
        get_patient_url = "https://hapi.fhir.org/baseR4/Patient/" + patient_id


        response = requests.get(get_patient_url)
        json_data = response.json()
        p = Patient()
        p.ID = json_data['id']

        if 'name' in json_data:
            names = json_data['name']
            given = " ".join(names[0]['given'])

            p.Name = given + ' ' + names[0]['family']
            p.FirstName = " ".join(names[0]['given'])
            p.LastName = names[0]['family']
        # print(entry)

        if 'telecom' in json_data:
            p.PhoneNumber = json_data['telecom'][0]['value']

        if 'gender' in json_data:
            p.Gender = json_data['gender']

        if 'birthDate' in json_data:
            p.DateOfBirth = json_data['birthDate']

        context = {
            'patient': p,
            'selected_gender': p.Gender,
            'gender_choices':['male', 'female', 'unknown', 'other']
        }

        return render(request, 'app/update-patient.html', context)
    
def search_patient(request):
    if request.method == 'POST':
        search_filter = request.POST.get('search_filter')

        name = request.POST.get('name')
        phone_number = request.POST.get('phone')

        if search_filter == 'phone_number':
            response = requests.get("https://hapi.fhir.org/baseR4/Patient?telecom=" + phone_number)

        elif search_filter == 'name':
            response = requests.get("https://hapi.fhir.org/baseR4/Patient?name=" + name)

        json_response = response.json()

        patients = []
        for entry in json_response['entry']:
            p = Patient()
            p.ID = entry['resource']['id']

            if 'name' in entry['resource']:
                names = entry['resource']['name']
                given = " ".join(names[0]['given'])

                p.Name = given + ' ' + names[0]['family']
                p.FirstName = " ".join(names[0]['given'])
                p.LastName = names[0]['family']

            if 'telecom' in entry['resource']:
                p.PhoneNumber = entry['resource']['telecom'][0]['value']

            if 'gender' in entry['resource']:
                p.Gender = entry['resource']['gender']

            if 'birthDate' in entry['resource']:
                p.DateOfBirth = entry['resource']['birthDate'] 

            patients.append(p)

        context = {
            'patients': patients
        }
        print(patients)
        return render(request, 'app/search-patient.html', context)
    
    else:
        context = {}
        return render(request, 'app/search-patient.html', context)

def search_patient_filter(request):
    query = request.GET.get('q', '')

    get_patients_url = "https://hapi.fhir.org/baseR4/Patient"

    response = requests.get(get_patients_url)

    json_response = json.loads(response.text)

    entrys = json_response['entry']

    patients = []
    for entry in entrys:
        # print(entry)
        if entry['resource']['resourceType'] == 'Patient':
            p = Patient()
            p.ID = entry['resource']['id']
            
            if 'name' in entry['resource']:
                
                names = entry['resource']['name']

                given = ''
                if 'given' in names[0]:
                    given = " ".join(names[0]['given'])

                p.Name = given + ' ' + names[0]['family']
            # print(entry)

            if 'gender' in entry['resource']:
                p.Gender = entry['resource']['gender']

            if 'birthDate' in entry['resource']:
                p.DateOfBirth = entry['resource']['birthDate']

            p.PhoneNumber = ''
            if 'telecom' in entry['resource']:
                p.PhoneNumber = entry['resource']['telecom'][0]['value']

            patients.append(p)

    for patient in patients:
        print(patient.PhoneNumber)
    return JsonResponse({
        'msg': 'Done!'
    })

def list_patients(request):
    get_patients_url = "https://hapi.fhir.org/baseR4/Patient"

    response = requests.get(get_patients_url)

    json_response = json.loads(response.text)

    entrys = json_response['entry']

    patients = []
    for entry in entrys:
        if entry['resource']['resourceType'] == 'Patient':
            p = Patient()
            p.ID = entry['resource']['id']

            if 'name' in entry['resource']:
                names = entry['resource']['name']

                given = ''
                if 'given' in names[0]:
                    given = " ".join(names[0]['given'])

                p.Name = given + ' ' + names[0]['family']
            # print(entry)

            if 'gender' in entry['resource']:
                p.Gender = entry['resource']['gender']

            if 'birthDate' in entry['resource']:
                p.DateOfBirth = entry['resource']['birthDate']

            patients.append(p)
    
            # items = response.json()

            # Paginate manually
    paginator = Paginator(patients, 10)  # 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'app/list-patients.html', {'page_obj': page_obj})
    # context = {
    #     'patients': patients
    # }

    # return render(request, 'app/list-patients.html', context)


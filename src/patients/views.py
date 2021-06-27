from django.shortcuts import render
import pip._vendor.requests as requests
from datetime import datetime

# Create your views here.

def patient_view(request):
    r = requests.get('https://hapi.fhir.org/baseR4/Patient?_pretty=true')
    json = r.json()
    # data = [{
    #     'given': item.get('resource').get('name')[0].get('given')[0],
    #     'family': item.get('resource').get('name')[0].get('family'),
    #     'gender': item.get('resource').get('gender'),
    #     'birthDate': item.get('resource').get('birthDate')
    #     } for item in json['entry']]

    data = []
    for item in json['entry']:
        obj = {}
        if item.get('resource').get('name'):
            obj['given'] = item.get('resource').get('name')[0].get('given')[0]
            obj['family'] = item.get('resource').get('name')[0].get('family')
        if item.get('resource').get('gender'):
            obj['gender'] = item.get('resource').get('gender')
        if item.get('resource').get('birthDate'):
            obj['birthDate'] = item.get('resource').get('birthDate')     
        
        data.append(obj)
    ages = []
    for item in data:
        if item.get('birthDate') != None:
            ages.append((datetime.now() - datetime.strptime(item['birthDate'], "%Y-%m-%d")).days // 365)
    context = {
        'avg_age': round(sum(ages) / len(ages)),
        'data': data
    }

    return render(request, "patients/patient_list.html", context)

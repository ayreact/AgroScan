from django.shortcuts import render, get_object_or_404
from django.forms.models import model_to_dict
import requests
from .models import PlantDiagnosis, StoredDiagnosis
from django.http import JsonResponse
from django.conf import settings
import random

def diagnosis_page(request):
    return render(request, 'submissions/diagnosis.html')

def run_diagnosis(request):
    api_url = settings.AI_API
    if request.method == 'POST':
        image_file = request.FILES.get('image')
        image_prompt = request.POST.get('notes', '')

        if not image_file:
            return JsonResponse({'error': 'No image file provided'}, status=400)

        try:
            # Check settings if api url is present, if it isn't, run request through Stored Diagnosis DB
            if api_url:
                # Prepare payload for AI API
                files = {'image': image_file}
                data = {'text': image_prompt} if image_prompt else {}

                # Make request to AI
                response = requests.post(api_url, files=files, data=data)
                response.raise_for_status()
                ai_data = response.json()

                # Save to DB if the user is authenticated
                if request.user.is_authenticated:
                    diagnosis = PlantDiagnosis.objects.create(
                        user=request.user,
                        image=image_file,
                        image_prompt=image_prompt,
                        diagnosis_title=ai_data.get('diagnosis_title', 'Untitled'),
                        health_condition=ai_data.get('health_condition', 'Unknown'),
                        cause=ai_data.get('cause', 'Unknown'),
                        disease_signs=ai_data.get('disease_signs', 'None detected'),
                        control_suggestions=ai_data.get('control_suggestions', 'None provided'),
                        summary=ai_data.get('summary', 'No summary available'),
                    )
                    diagnosis.save()

                return JsonResponse({
                    'message': 'Diagnosis saved successfully',
                    'data': {
                        'diagnosis_title': ai_data.get('diagnosis_title', 'Untitled'),
                        'health_condition': ai_data.get('health_condition', 'Unknown'),
                        'cause': ai_data.get('cause', 'Unknown'),
                        'disease_signs': ai_data.get('disease_signs', 'None detected'),
                        'control_suggestions': ai_data.get('control_suggestions', 'None provided'),
                        'summary': ai_data.get('summary', 'No summary available'),
                    }
                }, status=201)

            else:
                # Handle stored diagnosis logic if no API URL is present
                stored_diagnosis = StoredDiagnosis.objects.all()
                stored_list = list(stored_diagnosis)
                random.shuffle(stored_list)

                diagnosis_result = None 

                for item in stored_list:
                    if item.name.lower() in image_prompt.lower():
                        diagnosis_result = item
                        break  # Stop once a match is found

                # Check if diagnosis_result was found
                if diagnosis_result is None:
                    return JsonResponse({'error': 'No diagnosis could be taken with the provided prompt!'}, status=400)

                # Save response to DB if user is authenticated
                if request.user.is_authenticated:
                    diagnosis = PlantDiagnosis.objects.create(
                        user=request.user,
                        image=image_file,
                        image_prompt=image_prompt,
                        diagnosis_title=diagnosis_result.diagnosis_title,
                        health_condition=diagnosis_result.health_condition,
                        cause=diagnosis_result.cause,
                        disease_signs=diagnosis_result.disease_signs,
                        control_suggestions=diagnosis_result.control_suggestions,
                        summary=diagnosis_result.summary,
                    )
                    diagnosis.save()

                return JsonResponse({
                    'message': 'Diagnosis done successfully',
                    'data': {
                        'diagnosis_title': diagnosis_result.diagnosis_title,
                        'health_condition': diagnosis_result.health_condition,
                        'cause': diagnosis_result.cause,
                        'disease_signs': diagnosis_result.disease_signs,
                        'control_suggestions': diagnosis_result.control_suggestions,
                        'summary': diagnosis_result.summary,
                    }
                }, status=201)

        except requests.RequestException as e:
            return JsonResponse({'error': f'Failed to connect to AI API: {str(e)}'}, status=502)
        except ValueError:
            return JsonResponse({'error': 'Invalid JSON response from AI'}, status=500)

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)


def diagnosis_history(request, user_id):
    all_diagnosis = PlantDiagnosis.objects.all()

    user_diagnosis = []

    for item in all_diagnosis:
        if item.user_id == user_id:
            user_diagnosis.append(item)

    last_diagnosis = None
    diagnosis_list = list(all_diagnosis)
    diagnosis_list.reverse()
    
    for item in diagnosis_list:
        if item.user_id == user_id:
            last_diagnosis = item
            break

    user_diagnosis.reverse()
    
    context = {
        'user_diagnosis':user_diagnosis,
        'last_diagnosis':last_diagnosis,
    }
    return render(request, 'submissions/history.html', context)

def get_history(request, diagnosis_id):
    diagnosis = PlantDiagnosis.objects.get(id=diagnosis_id)
    data = model_to_dict(diagnosis)

    
    if diagnosis.image: 
        data['image'] = diagnosis.image.url
    else:
        data['image'] = None

    return JsonResponse({'message': 'Diagnosis fetched successfully', 'data': data}, status=200)
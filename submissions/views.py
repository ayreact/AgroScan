from django.shortcuts import render
from django.forms.models import model_to_dict
from .models import PlantDiagnosis
from .gemini_utils import generate_crop_diagnosis
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json

def diagnosis_page(request):
    return render(request, 'submissions/diagnosis.html')

# Diagnosis endpoint
def run_diagnosis(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)
    
    try:
        image_file = request.FILES.get('image')  # None if not provided
        text = request.POST.get('notes', '')     # Empty string if not provided
        
        # Generate diagnosis
        diagnosis_result = generate_crop_diagnosis(text, image_file)
        
        if 'error' in diagnosis_result:
            return JsonResponse({'error': diagnosis_result['error']}, status=400)
        
        # Prepare response data
        response_data = {
            'data': {
                'diagnosis_title': diagnosis_result.get('diagnosis_title', 'Untitled'),
                'health_condition': diagnosis_result.get('health_condition', 'Unknown'),
                'cause': diagnosis_result.get('cause', 'Unknown'),
                'disease_signs': diagnosis_result.get('disease_signs', 'None detected'),
                'control_suggestions': diagnosis_result.get('control_suggestions', 'None provided'),
                'summary': diagnosis_result.get('summary', 'No summary available'),
            }
        }

        # Save for authenticated users
        if request.user.is_authenticated:
            diagnosis = PlantDiagnosis.objects.create(
                user=request.user,
                image=image_file,
                image_prompt=text,
                **response_data['data']
            )
            response_data['message'] = 'Diagnosis saved successfully'
            status_code = 201
        else:
            response_data['message'] = 'Diagnosis Complete'
            status_code = 200

        return JsonResponse(response_data, status=status_code)

    except Exception as e:
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)
    

# SMS Diagnosis
@csrf_exempt
def sms_diagnosis(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)

    diagnosis_key = request.headers.get('Diagnosis-Key') or request.headers.get('diagnosis-key')
    if not diagnosis_key or diagnosis_key != settings.DIAGNOSIS_KEY:
        return JsonResponse({'error': 'Invalid or missing diagnosis key'}, status=401)

    text = ''
    image_file = None
    response_data = {
        'data': {
            'diagnosis_title': 'Untitled',
            'health_condition': 'Unknown',
            'cause': 'Unknown',
            'disease_signs': 'None detected',
            'control_suggestions': 'None provided',
            'summary': 'No summary available'
        },
        'message': 'Diagnosis Complete'
    }

    try:
        text = request.POST.get('text', '').strip()
        image_file = request.FILES.get('image')

        if image_file:
            if image_file.size > 5 * 1024 * 1024:
                raise ValueError("Image too large (max 5MB)")
            if not image_file.content_type.startswith('image/'):
                raise ValueError("Invalid image format")

        diagnosis_result = generate_crop_diagnosis(text or None, image_file)

        if 'error' in diagnosis_result:
            return JsonResponse({'error': diagnosis_result['error']}, status=400)

        for field in response_data['data']:
            if field in diagnosis_result:
                response_data['data'][field] = diagnosis_result[field]

        return JsonResponse(response_data, status=200)

    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Internal server error'}, status=500)
    

# History    
@login_required
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


# History Details
@login_required
def get_history(request, diagnosis_id):
    diagnosis = PlantDiagnosis.objects.get(id=diagnosis_id)
    data = model_to_dict(diagnosis)

    
    if diagnosis.image: 
        data['image'] = diagnosis.image.url
    else:
        data['image'] = None

    return JsonResponse({'message': 'Diagnosis fetched successfully', 'data': data}, status=200)
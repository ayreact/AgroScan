from openai import OpenAI
import base64
import json
from django.conf import settings

# Configure API key
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_crop_diagnosis(text=None, image_file=None):
    """
    Generate crop diagnosis from text and/or image with integrated warnings.
    Returns:
        - Full diagnosis in structured JSON format (for valid inputs)
        - Error object for invalid inputs
    """

    # Build the conversation messages
    messages = [
        {
            "role": "system",
            "content": (
                "You are an agricultural expert analyzing crop health. "
                "Follow these rules strictly:\n"
                "1. First validate if inputs are crop-related\n"
                "2. Return errors for completely irrelevant inputs\n"
                "3. For partially valid inputs, include warnings in health_condition\n"
                "4. For crop images which you can identify the crop itself, include the crop name in diagnosis_title or health_condition\n"
                "5. Include possible wrong human actions that could cause the crop disease in cause\n"
                "6. In your entire response, make sure you don't use big vocabulary, use simple common words anyone either learned or not can easily understand\n"
                "7. Always use the exact specified JSON format"
            )
        }
    ]

    # Prepare content parts
    content_parts = []
    
    # Add text if provided
    if text:
        content_parts.append({
            "type": "text",
            "text": f"User's description: {text}"
        })

    # Add image if provided (CORRECTED FORMAT)
    if image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        content_parts.append({
            "type": "image_url",
            # Must be an object with 'url' property
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
        })

    # Add instructions
    content_parts.append({
        "type": "text",
        "text": (
            "ANALYSIS INSTRUCTIONS:\n"
            "1. If NON-CROP image AND NO crop-related text:\n"
            '   RETURN {"error": "No crop data detected. Please provide a crop image or description."}\n\n'
            
            "2. For valid analysis:\n"
            "   - If image is non-crop BUT text is valid:\n"
            "     Include in health_condition: \"[DIAGNOSIS] (Warning: Diagnosing from text only - image appears unrelated)\"\n"
            "   - If text is irrelevant BUT image is valid:\n"
            "     Include in health_condition: \"[DIAGNOSIS] (Warning: Diagnosing from image only - text appears unrelated)\"\n"
            "   - If and only if you can identify the crop in the image itself:\n"
            "     Include in diagnosis_title or health_condition the name of the crop\"\n\n"
            
            "3. Provide output in THIS EXACT FORMAT:\n"
            '{\n'
            '  "diagnosis_title": "string",\n'
            '  "health_condition": "string [with integrated warnings if needed]",\n'
            '  "cause": "string",\n'
            '  "disease_signs": "string",\n'
            '  "control_suggestions": "string",\n'
            '  "summary": "string"\n'
            '}'
        )
    })

    messages.append({
        "role": "user",
        "content": content_parts
    })

    # Make the API call
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",  # Current vision-capable model
            messages=messages,
            max_tokens=1000,
            response_format={"type": "json_object"},
            temperature=0.3
        )

        # Parse and return the JSON response
        return json.loads(response.choices[0].message.content)

    except Exception as e:
        # Handle specific API errors
        if hasattr(e, 'response') and hasattr(e.response, 'json'):
            error_data = e.response.json()
            if 'error' in error_data:
                return {"error": f"OpenAI API: {error_data['error'].get('message', 'Unknown error')}"}
        
        return {"error": f"Analysis failed: {str(e)}"}
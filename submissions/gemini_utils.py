import google.generativeai as genai
import base64
import json
from django.conf import settings
from PIL import Image
import io

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

def generate_crop_diagnosis(text=None, image_file=None):
    """
    Generate crop diagnosis from text and/or image with integrated warnings using Gemini.
    Returns:
        - Full diagnosis in structured JSON format (for valid inputs)
        - Error object for invalid inputs
    """
    # Initialize the model (using gemini-pro-vision for multimodal support)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # Build the system instruction part
    system_instruction = (
        "You are an agricultural expert analyzing crop health. Follow these rules strictly:\n"
        "1. First validate if inputs are crop-related\n"
        "2. Return errors for completely irrelevant inputs\n"
        "3. For partially valid inputs, include warnings in health_condition\n"
        "4. For crop images which you can identify the crop itself, include the crop name in diagnosis_title or health_condition\n"
        "5. Include possible wrong human actions that could cause the crop disease in cause\n"
        "6. Use simple common words anyone can easily understand\n"
        "7. Always respond with valid JSON in this exact format:\n"
        '{\n'
        '  "diagnosis_title": "string",\n'
        '  "health_condition": "string [with integrated warnings if needed]",\n'
        '  "cause": "string",\n'
        '  "disease_signs": "string",\n'
        '  "control_suggestions": "string",\n'
        '  "summary": "string"\n'
        '}\n\n'
        "ANALYSIS INSTRUCTIONS:\n"
        "1. If NON-CROP image AND NO crop-related text:\n"
        '   RETURN {"error": "No crop data detected. Please provide a crop image or description."}\n\n'
        
        "2. For valid analysis:\n"
        "   - If image is non-crop BUT text is valid:\n"
        "     Include in health_condition: \"[DIAGNOSIS] (Warning: Diagnosing from text only - image appears unrelated)\"\n"
        "   - If text is irrelevant BUT image is valid:\n"
        "     Include in health_condition: \"[DIAGNOSIS] (Warning: Diagnosing from image only - text appears unrelated)\"\n\n"
    )

    # Prepare the content parts
    content_parts = [system_instruction]
    
    # Add text if provided
    if text:
        content_parts.append(f"User's description: {text}")

    # Prepare image if provided
    image_part = None
    if image_file:
        # Read and prepare the image
        image = Image.open(image_file)
        image_part = image

    # Make the API call
    try:
        if image_part:
            # For image + text case
            if text:
                response = model.generate_content(
                    [system_instruction + f"\nUser's description: {text}", image_part]
                )
            else:
                # For image-only case
                response = model.generate_content(
                    [system_instruction, image_part]
                )
        else:
            # For text-only case (switch to text-only model)
            text_model = genai.GenerativeModel('gemini-2.0-flash')
            full_prompt = system_instruction
            if text:
                full_prompt += f"\nUser's description: {text}"
            response = text_model.generate_content(full_prompt)
        
        # Extract the response text
        response_text = response.text
        
        # Clean the response (Gemini sometimes adds markdown formatting)
        response_text = response_text.strip().replace('```json', '').replace('```', '').strip()
        
        # Parse the JSON response
        return json.loads(response_text)

    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON response from AI: {str(e)}. Raw response: {response_text}"}
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}
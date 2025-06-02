# 📡 SMS Diagnosis API

This API allows users to send **text** and/or **image** data to receive a crop diagnosis. It is useful for remote agricultural support systems where users may send symptoms or images via SMS/MMS for automated analysis.

---

## 🔗 Endpoint

POST https://agroscan-xasy.onrender.com/new-chat/sms-diagnosis

---

## 🔐 Authentication

- Requires a custom header:

| Header Name      | Value                        | Required |
|------------------|------------------------------|----------|
| `Diagnosis-Key`  | `your_secret_diagnosis_key`  | ✅       |

> ✅ The key must match `settings.DIAGNOSIS_KEY` on the server.

---

## 📨 Request

### Method
`POST`

### Headers

| Name           | Value                    |
|----------------|--------------------------|
| `Diagnosis-Key`| Your secret key (string) |

### Form Data (`multipart/form-data`)

| Field   | Type    | Description                                      | Required |
|---------|---------|--------------------------------------------------|----------|
| `text`  | string  | Description of symptoms (optional if image is provided) | ❌       |
| `image` | file    | Image file (`.jpg`, `.png`, etc.), max 5MB       | ❌       |

> At least **one** of `text` or `image` should be included.

---

## 🧾 Sample cURL Request

```bash
curl -X POST https://agroscan-xasy.onrender.com/new-chat/sms-diagnosis \
  -H "Diagnosis-Key: your_secret_diagnosis_key" \
  -F "text=Leaves are turning yellow" \
  -F "image=@/path/to/leaf.jpg"


✅ Successful Response
{
  "data": {
    "diagnosis_title": "Leaf Blight",
    "health_condition": "Unhealthy",
    "cause": "Fungal Infection",
    "disease_signs": "Spots and yellowing",
    "control_suggestions": "Use fungicide, improve drainage",
    "summary": "The crop shows signs of fungal infection requiring immediate treatment."
  },
  "message": "Diagnosis Complete"
}


❌ Error Responses
Method Not Allowed (Non-POST)
{
  "error": "Only POST method allowed"
}
Status Code: 405

Missing or Invalid Diagnosis Key
{
  "error": "Invalid or missing diagnosis key"
}
Status Code: 401

Invalid Input (e.g., large file, unsupported format)
{
  "error": "Image too large (max 5MB)"
}
or
{
  "error": "Invalid image format"
}
Status Code: 400

Backend Error
{
  "error": "Internal server error"
}
Status Code: 500


🧠 Notes
The backend handles both text and image-based diagnosis.

Image must be of type image/* and should not exceed 5MB.

When both text and image are supplied, the AI may use both for better accuracy.

The default response includes placeholder values if no diagnosis can be made.

📞 Contact
For support or questions about integrating this API, contact the AgroScan team.
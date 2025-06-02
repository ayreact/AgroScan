// Image upload and preview functionality
const imageUpload = document.getElementById('image-upload');
const desCription = document.getElementById('description');
const previewImage = document.getElementById('preview-image');
const uploadPrompt = document.getElementById('upload-prompt');
const cameraButton = document.getElementById('camera-button');
const errorMessage = document.getElementById('image-upload-error');
const form = document.getElementById('diagnosis-form');
const diagnosis_title = document.getElementById("diagnosis-title");
const health_condition = document.getElementById("health-condition");
const cause = document.getElementById("causes");
const disease_signs = document.getElementById("disease-signs");
const control_suggestions = document.getElementById("control-suggestions");
const summary = document.getElementById("summary");
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const result_container = document.getElementById('results-container');
const imageClear = document.getElementById('image-clear');

// Store captured image blob
let capturedImageBlob = null;

// Helper function to convert data URL to Blob
function dataURLtoBlob(dataURL) {
  const arr = dataURL.split(',');
  const mime = arr[0].match(/:(.*?);/)[1];
  const bstr = atob(arr[1]);
  let n = bstr.length;
  const u8arr = new Uint8Array(n);
  while (n--) {
    u8arr[n] = bstr.charCodeAt(n);
  }
  return new Blob([u8arr], { type: mime });
}

imageUpload.addEventListener('change', function() {
  const file = this.files[0];
  if (file) {
    // Clear any previously captured image
    capturedImageBlob = null;
    
    const reader = new FileReader();
    reader.onload = function(e) {
      previewImage.src = e.target.result;
      previewImage.style.display = 'block';
      uploadPrompt.style.display = 'none';
      imageClear.style.display = 'inline';
    }
    reader.readAsDataURL(file);
  }
});

cameraButton.addEventListener('click', function () {
  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    
    const cameraContainer = document.createElement('div');
    cameraContainer.style.position = 'fixed';
    cameraContainer.style.top = '0';
    cameraContainer.style.left = '0';
    cameraContainer.style.width = '100%';
    cameraContainer.style.height = '100%';
    cameraContainer.style.backgroundColor = 'rgba(0,0,0,0.9)';
    cameraContainer.style.zIndex = '1000';
    cameraContainer.style.display = 'flex';
    cameraContainer.style.flexDirection = 'column';
    cameraContainer.style.alignItems = 'center';
    cameraContainer.style.justifyContent = 'center';
    
    const videoEl = document.createElement('video');
    videoEl.style.maxWidth = '90%';
    videoEl.style.maxHeight = '70%';
    videoEl.style.objectFit = 'contain';
    videoEl.autoplay = true;
    videoEl.playsInline = true;
    
    const buttonContainer = document.createElement('div');
    buttonContainer.style.display = 'flex';
    buttonContainer.style.gap = '1rem';
    buttonContainer.style.marginTop = '1rem';
    
    const captureBtn = document.createElement('button');
    captureBtn.className = 'btn btn-primary';
    captureBtn.innerHTML = '<i class="fas fa-camera"></i>';
    
    const switchBtn = document.createElement('button');
    switchBtn.className = 'btn btn-secondary';
    switchBtn.innerHTML = '<i class="fas fa-sync-alt"></i>';
    
    const cancelBtn = document.createElement('button');
    cancelBtn.className = 'btn btn-outline';
    cancelBtn.style.backgroundColor = 'white';
    cancelBtn.innerHTML = '<i class="fas fa-times"></i>';

    buttonContainer.appendChild(switchBtn);
    buttonContainer.appendChild(captureBtn);
    buttonContainer.appendChild(cancelBtn);
    
    cameraContainer.appendChild(videoEl);
    cameraContainer.appendChild(buttonContainer);
    document.body.appendChild(cameraContainer);

    let currentFacingMode = 'environment';
    let stream = null;

    function startCamera() {
      navigator.mediaDevices.getUserMedia({ video: { facingMode: currentFacingMode } })
        .then(function (mediaStream) {
          stream = mediaStream;
          videoEl.srcObject = stream;
          videoEl.play();
        })
        .catch(function (error) {
          errorMessage.textContent = 'Error accessing camera: ' + error.message;
          document.body.removeChild(cameraContainer);
        });
    }

    startCamera(); 

    switchBtn.addEventListener('click', function () {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
      currentFacingMode = currentFacingMode === 'user' ? 'environment' : 'user';
      startCamera();
    });

    cancelBtn.addEventListener('click', function () {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
      document.body.removeChild(cameraContainer);
    });

    captureBtn.addEventListener('click', function () {
      const canvas = document.createElement('canvas');
      canvas.width = videoEl.videoWidth;
      canvas.height = videoEl.videoHeight;
      canvas.getContext('2d').drawImage(videoEl, 0, 0);
      const imageDataUrl = canvas.toDataURL('image/png');
      
      // Convert to Blob and store for form submission
      capturedImageBlob = dataURLtoBlob(imageDataUrl);
      
      // Clear file input if switching from upload to camera
      imageUpload.value = '';
      
      previewImage.src = imageDataUrl;
      previewImage.style.display = 'block';
      uploadPrompt.style.display = 'none';
      imageClear.style.display = 'inline';
      
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
      document.body.removeChild(cameraContainer);
    });
    
  } else {
    errorMessage.textContent = 'Your browser does not support camera access';
  }
});

form.addEventListener('submit', async function (e) {
    e.preventDefault();

    if (previewImage.style.display === 'none' && desCription.value.length == 0) {
        errorMessage.textContent = 'Please provide an image or type a prompt';
        return;
    }else{
      errorMessage.textContent = '';
    }

    const formData = new FormData(form);
    
    // If there's a captured image (from camera), add it to the form data
    if (capturedImageBlob) {
        formData.delete('image'); // Remove empty file input if present
        formData.append('image', capturedImageBlob, 'captured-image.png');
    }

    try {
        const response = await fetch(diagnosisUrl, {
            method: 'POST',
            headers: {
              'X-CSRFToken': csrfToken,
            },
            credentials: "include",
            body: formData,
        });

        const prompt_response = await response.json();

        if (response.ok) {
            localStorage.setItem('lastDiagnosis', JSON.stringify(prompt_response.data));
            result_container.style.display = 'block';
            diagnosis_title.textContent = prompt_response.data.diagnosis_title;
            health_condition.textContent = prompt_response.data.health_condition;
            cause.textContent = prompt_response.data.cause;
            disease_signs.textContent = prompt_response.data.disease_signs;
            control_suggestions.textContent = prompt_response.data.control_suggestions;
            summary.textContent = prompt_response.data.summary;
            result_container.scrollIntoView({ behavior: 'smooth' });
        } else {
            alert(prompt_response.error);
            console.log(prompt_response.error)
        }
    } catch (error) {
        console.error('Network error:', error);
        alert('Something went wrong. Please try again.');
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const savedDiagnosis = localStorage.getItem('lastDiagnosis');
    console.log("Retrieved from localStorage:", savedDiagnosis);
    if (savedDiagnosis) {
        try {
            result_container.style.display = 'block';
            const data = JSON.parse(savedDiagnosis);
            diagnosis_title.textContent = data.diagnosis_title;
            health_condition.textContent = data.health_condition;
            cause.textContent = data.cause;
            disease_signs.textContent = data.disease_signs;
            control_suggestions.textContent = data.control_suggestions;
            summary.textContent = data.summary;
            result_container.scrollIntoView({ behavior: 'smooth' });
        } catch (e) {
            console.error("Failed to parse saved diagnosis:", e);
            localStorage.removeItem('lastDiagnosis');
        }
    }
});

function clearImageUpload() {
  if (imageUpload.value != ""){
    imageUpload.value = "";
    previewImage.src = '';
    previewImage.style.display = 'none';
    uploadPrompt.style.display = 'block';
  }
}

imageClear.addEventListener("click", clearImageUpload)
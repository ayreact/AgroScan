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
const loaderCon = document.querySelector(".loader-con");
const mainBody = document.body;

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

imageUpload.addEventListener('click', function() {
  // Store the current value
  this.previousValue = this.value;
});

imageUpload.addEventListener('cancel', function() {
  // If dialog was cancelled and value is empty, restore the previous value
  if (this.value === '' && this.previousValue) {
      this.value = this.previousValue;
  }
});

imageUpload.addEventListener('change', function() {
  const file = this.files[0];
  if (file) {
      // Clear any previously captured image
      capturedImageBlob = null;
      
      // Store the current file for restoration if needed
      this.currentFile = file;
      
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
    // Create camera modal
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
    
    // Create camera dialog
    const cameraDialog = document.createElement('div');
    cameraDialog.style.backgroundColor = '#1a1a1a';
    cameraDialog.style.borderRadius = '16px';
    cameraDialog.style.overflow = 'hidden';
    cameraDialog.style.width = '90%';
    cameraDialog.style.maxWidth = '500px';
    cameraDialog.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.3)';
    
    // Create header
    const header = document.createElement('div');
    header.style.display = 'flex';
    header.style.justifyContent = 'space-between';
    header.style.alignItems = 'center';
    header.style.padding = '16px 20px';
    header.style.backgroundColor = '#2a2a2a';
    header.style.color = 'white';
    
    const title = document.createElement('h3');
    title.textContent = 'Take a Photo';
    title.style.margin = '0';
    title.style.fontWeight = '500';
    title.style.fontSize = '18px';
    
    const closeBtn = document.createElement('button');
    closeBtn.innerHTML = '&times;';
    closeBtn.style.background = 'none';
    closeBtn.style.border = 'none';
    closeBtn.style.color = 'white';
    closeBtn.style.fontSize = '24px';
    closeBtn.style.cursor = 'pointer';
    closeBtn.style.padding = '0';
    closeBtn.style.width = '30px';
    closeBtn.style.height = '30px';
    closeBtn.style.borderRadius = '50%';
    closeBtn.style.display = 'flex';
    closeBtn.style.alignItems = 'center';
    closeBtn.style.justifyContent = 'center';
    
    header.appendChild(title);
    header.appendChild(closeBtn);
    
    // Create video preview
    const previewContainer = document.createElement('div');
    previewContainer.style.position = 'relative';
    previewContainer.style.width = '100%';
    previewContainer.style.paddingBottom = '75%'; // 4:3 aspect ratio
    previewContainer.style.backgroundColor = '#000';
    previewContainer.style.overflow = 'hidden';
    
    const videoEl = document.createElement('video');
    videoEl.style.position = 'absolute';
    videoEl.style.top = '0';
    videoEl.style.left = '0';
    videoEl.style.width = '100%';
    videoEl.style.height = '100%';
    videoEl.style.objectFit = 'cover';
    videoEl.autoplay = true;
    videoEl.playsInline = true;
    
    // Create camera frame
    const cameraFrame = document.createElement('div');
    cameraFrame.style.position = 'absolute';
    cameraFrame.style.top = '50%';
    cameraFrame.style.left = '50%';
    cameraFrame.style.transform = 'translate(-50%, -50%)';
    cameraFrame.style.width = '80%';
    cameraFrame.style.height = '80%';
    cameraFrame.style.border = '2px solid rgba(255, 255, 255, 0.5)';
    cameraFrame.style.borderRadius = '8px';
    cameraFrame.style.pointerEvents = 'none';
    
    // Create frame corners
    const createCorner = (position) => {
      const corner = document.createElement('div');
      corner.style.position = 'absolute';
      corner.style.width = '20px';
      corner.style.height = '20px';
      corner.style.borderColor = 'white';
      corner.style.borderStyle = 'solid';
      
      switch(position) {
        case 'top-left':
          corner.style.top = '-2px';
          corner.style.left = '-2px';
          corner.style.borderWidth = '3px 0 0 3px';
          corner.style.borderRadius = '8px 0 0 0';
          break;
        case 'top-right':
          corner.style.top = '-2px';
          corner.style.right = '-2px';
          corner.style.borderWidth = '3px 3px 0 0';
          corner.style.borderRadius = '0 8px 0 0';
          break;
        case 'bottom-left':
          corner.style.bottom = '-2px';
          corner.style.left = '-2px';
          corner.style.borderWidth = '0 0 3px 3px';
          corner.style.borderRadius = '0 0 0 8px';
          break;
        case 'bottom-right':
          corner.style.bottom = '-2px';
          corner.style.right = '-2px';
          corner.style.borderWidth = '0 3px 3px 0';
          corner.style.borderRadius = '0 0 8px 0';
          break;
      }
      
      return corner;
    };
    
    cameraFrame.appendChild(createCorner('top-left'));
    cameraFrame.appendChild(createCorner('top-right'));
    cameraFrame.appendChild(createCorner('bottom-left'));
    cameraFrame.appendChild(createCorner('bottom-right'));
    
    previewContainer.appendChild(videoEl);
    previewContainer.appendChild(cameraFrame);
    
    // Create controls
    const controls = document.createElement('div');
    controls.style.display = 'flex';
    controls.style.justifyContent = 'space-between';
    controls.style.alignItems = 'center';
    controls.style.padding = '20px';
    controls.style.backgroundColor = '#2a2a2a';
    
    const createControlButton = (icon, className) => {
      const btn = document.createElement('button');
      btn.className = className;
      btn.innerHTML = `<i class="fas ${icon}"></i>`;
      btn.style.background = 'none';
      btn.style.border = 'none';
      btn.style.color = 'white';
      btn.style.cursor = 'pointer';
      btn.style.padding = '12px';
      btn.style.borderRadius = '50%';
      btn.style.display = 'flex';
      btn.style.alignItems = 'center';
      btn.style.justifyContent = 'center';
      btn.style.transition = 'all 0.2s';
      
      return btn;
    };
    
    const switchBtn = createControlButton('fa-sync-alt', 'switch-camera');
    switchBtn.style.fontSize = '20px';
    switchBtn.style.width = '50px';
    switchBtn.style.height = '50px';
    
    const captureBtn = createControlButton('', 'capture-btn');
    captureBtn.style.width = '64px';
    captureBtn.style.height = '64px';
    captureBtn.style.background = 'white';
    captureBtn.style.border = '4px solid rgba(255, 255, 255, 0.3)';
    
    const captureCircle = document.createElement('div');
    captureCircle.style.width = '56px';
    captureCircle.style.height = '56px';
    captureCircle.style.borderRadius = '50%';
    captureCircle.style.background = 'white';
    captureCircle.style.border = '2px solid rgba(0, 0, 0, 0.1)';
    captureBtn.appendChild(captureCircle);
    
    const cancelBtn = createControlButton('fa-times', 'cancel-btn');
    cancelBtn.style.fontSize = '20px';
    cancelBtn.style.width = '50px';
    cancelBtn.style.height = '50px';
    
    controls.appendChild(switchBtn);
    controls.appendChild(captureBtn);
    controls.appendChild(cancelBtn);
    
    // Assemble dialog
    cameraDialog.appendChild(header);
    cameraDialog.appendChild(previewContainer);
    cameraDialog.appendChild(controls);
    cameraContainer.appendChild(cameraDialog);
    document.body.appendChild(cameraContainer);
    document.body.style.overflow = 'hidden';

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
          closeCamera();
        });
    }

    function closeCamera() {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
      document.body.removeChild(cameraContainer);
      document.body.style.overflow = '';
    }

    startCamera();

    switchBtn.addEventListener('click', function () {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
      currentFacingMode = currentFacingMode === 'user' ? 'environment' : 'user';
      startCamera();
    });

    closeBtn.addEventListener('click', closeCamera);
    cancelBtn.addEventListener('click', closeCamera);

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
      
      closeCamera();
    });
    
  } else {
    errorMessage.textContent = 'Your browser does not support camera access';
  }
});

form.addEventListener('submit', async function (e) {
    e.preventDefault();

    const hasFileInput = imageUpload.files.length > 0 && imageUpload.files[0];
    const hasCapturedImage = capturedImageBlob !== null;
    
    if (!hasFileInput && !hasCapturedImage && desCription.value.length == 0) {
        errorMessage.textContent = 'Please provide an image or type a prompt';
        return;
    } else {
        errorMessage.textContent = '';
    }

    if (previewImage.style.display === 'none' && desCription.value.length == 0) {
        errorMessage.textContent = 'Please provide an image or type a prompt';
        return;
    }else{
      errorMessage.textContent = '';
    }

    const formData = new FormData(form);
    loaderCon.style.display = 'flex';
    mainBody.style.overflow = 'hidden';
    
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
        loaderCon.style.display = 'none';
        mainBody.style.overflow = 'scroll';

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
        loaderCon.style.display = 'none';
        mainBody.style.overflow = 'scroll';
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
  // Clear file input if it has a value
  if (imageUpload.value != "") {
      imageUpload.value = "";
  }
  
  // Clear captured image blob if it exists
  capturedImageBlob = null;
  
  // Reset preview UI
  previewImage.src = '';
  previewImage.style.display = 'none';
  uploadPrompt.style.display = 'block';
  imageClear.style.display = 'none';
}

imageClear.addEventListener("click", clearImageUpload)
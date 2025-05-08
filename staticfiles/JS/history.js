const historyItems = document.querySelectorAll('.history-item');
const historyToggleBtn = document.getElementById('historyToggleBtn');
const historySidebar = document.getElementById('historySidebar');
const historySidebarOverlay = document.getElementById('historySidebarOverlay');

document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll(".getHistoryBtn");
    const currentDiagnosisTitle = document.getElementById("currentDiagnosisTitle");
    const currentDiagnosishealth = document.getElementById("currentDiagnosishealth");
    const currentDiagnosisCause = document.getElementById("currentDiagnosisCause");
    const currentDiagnosisSigns = document.getElementById("currentDiagnosisSigns");
    const currentDiagnosisControl = document.getElementById("currentDiagnosisControl");
    const currentDiagnosisSummary = document.getElementById("currentDiagnosisSummary");
    const currentDiagnosisImage = document.getElementById("currentDiagnosisImage");

    // ✅ Load from localStorage on page load
    const savedHistory = localStorage.getItem("historyData");
    if (savedHistory) {
        const parsed = JSON.parse(savedHistory);
        currentDiagnosisTitle.textContent = parsed.data.diagnosis_title;
        currentDiagnosishealth.textContent = parsed.data.health_condition;
        currentDiagnosisCause.textContent = parsed.data.cause;
        currentDiagnosisSigns.textContent = parsed.data.disease_signs;
        currentDiagnosisControl.textContent = parsed.data.control_suggestions;
        currentDiagnosisSummary.textContent = parsed.data.summary;
        currentDiagnosisImage.src = parsed.data.image;
    }

    buttons.forEach(button => {
        const diagnosisId = button.dataset.id;
        const historyUrl = baseHistoryUrl.replace("0", diagnosisId);

        firstButton = historyItems[0]

        if (!sessionStorage.getItem('reloaded')) {
            firstButton.classList.add('active');
        }

        button.addEventListener("click", async (event) => {
            event.preventDefault();
            
            try {
                const response = await fetch(historyUrl, { method: 'GET' });
                const history_data = await response.json();

                if (response.ok) {
                    localStorage.setItem('historyData', JSON.stringify(history_data));
                    currentDiagnosisTitle.textContent = history_data.data.diagnosis_title;
                    currentDiagnosishealth.textContent = history_data.data.health_condition;
                    currentDiagnosisCause.textContent = history_data.data.cause;
                    currentDiagnosisSigns.textContent = history_data.data.disease_signs;
                    currentDiagnosisControl.textContent = history_data.data.control_suggestions;
                    currentDiagnosisSummary.textContent = history_data.data.summary;
                    currentDiagnosisImage.src = history_data.data.image;

                    
                } else {
                    alert("Failed to load history data.");
                }
            } catch (error) {
                console.error('Network error:', error);
                alert('Something went wrong. Please try again.');
            }
        });
    });
});

historyItems.forEach(item => {
    item.addEventListener('click', function() {
      // Remove active class from all items
      historyItems.forEach(i => i.classList.remove('active'));
      
      // Add active class to clicked item
      this.classList.add('active');
      
      // On mobile, close sidebar after selecting an item
      if (window.innerWidth < 768) {
        toggleHistorySidebar(false);
      }
    });
});

function toggleHistorySidebar(show) {
    if (show === undefined) {
      historySidebar.classList.toggle('active');
      historySidebarOverlay.classList.toggle('active');
    } else {
      if (show) {
        historySidebar.classList.add('active');
        historySidebarOverlay.classList.add('active');
      } else {
        historySidebar.classList.remove('active');
        historySidebarOverlay.classList.remove('active');
      }
    }
  }
  
// Show/hide toggle button based on screen size
function updateHistoryLayout() {
    if (window.innerWidth < 768) {
      historyToggleBtn.style.display = 'inline-block';
    } else {
      historyToggleBtn.style.display = 'none';
      toggleHistorySidebar(false);
    }
}
  
// Initial layout setup
updateHistoryLayout();
  
// Add event listeners
historyToggleBtn.addEventListener('click', () => toggleHistorySidebar());
historySidebarOverlay.addEventListener('click', () => toggleHistorySidebar(false));
window.addEventListener('resize', updateHistoryLayout);

window.addEventListener('beforeunload', () => {
    sessionStorage.setItem('reloaded', 'true');
});
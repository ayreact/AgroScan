// Common JavaScript functionality for AgroScan

// Theme color variables
const colors = {
    primary: '#15803d',
    secondary: '#ca8a04',
    accent: '#16a34a',
    background: '#f0fdf4',
    white: '#ffffff'
  };
  
  // Helper function to format dates
  function formatDate(date) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(date).toLocaleDateString(undefined, options);
  }
  
  // Mobile navigation toggle (for responsive design)
  document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu functionality
    const mobileMenuBtn = document.createElement('button');
    mobileMenuBtn.className = 'mobile-menu-btn';
    mobileMenuBtn.innerHTML = '☰';
    mobileMenuBtn.setAttribute('aria-label', 'Toggle navigation menu');
    
    const nav = document.querySelector('nav');
    const navLinks = document.querySelector('.nav-links');
    
    if (nav && navLinks) {
      nav.insertBefore(mobileMenuBtn, navLinks);
      
      mobileMenuBtn.addEventListener('click', function() {
        navLinks.classList.toggle('active');
        mobileMenuBtn.innerHTML = navLinks.classList.contains('active') ? '✕' : '☰';
      });
      
      // Close menu when clicking outside
      document.addEventListener('click', function(event) {
        if (!nav.contains(event.target) && navLinks.classList.contains('active')) {
          navLinks.classList.remove('active');
          mobileMenuBtn.innerHTML = '☰';
        }
      });
      
      // Close menu when window is resized to desktop size
      window.addEventListener('resize', function() {
        if (window.innerWidth > 768 && navLinks.classList.contains('active')) {
          navLinks.classList.remove('active');
          mobileMenuBtn.innerHTML = '☰';
        }
      });
    }
    
    console.log('AgroScan app initialized');
    
    // Add page transition effect
    document.body.classList.add('fade-in');
    
    // Add any global event listeners or initializations here
  });
  
  // Mock diagnosis function (would be replaced by actual API calls)
  function performDiagnosis(imageData, notes) {
    return new Promise((resolve) => {
      // Simulate API delay
      setTimeout(() => {
        // Mock response data
        const result = {
          title: 'Leaf Spot Disease on Tomato Plant',
          healthCondition: 'Moderate infection. Plant is still viable but requires immediate treatment.',
          diseaseCauses: 'Early blight (Alternaria solani) fungal infection, likely caused by humid conditions and poor air circulation.',
          diseaseSigns: 'Brown to black spots with concentric rings on older leaves. Yellowing around the spots. Spots may merge as infection progresses.',
          controlSuggestions: 'Remove and destroy infected leaves. Apply copper-based fungicide. Improve air circulation around plants. Water at soil level to keep leaves dry. Rotate crops next season.',
          summary: 'Your tomato plant has early blight, a common fungal disease. With immediate treatment using the suggested measures, the plant should recover and produce a healthy yield. Monitor for recurring symptoms over the next two weeks.'
        };
        resolve(result);
      }, 1500);
    });
  }
  
  // Save diagnosis to local storage (for history feature)
  function saveDiagnosisToHistory(diagnosis) {
    // Get existing history or initialize empty array
    const history = JSON.parse(localStorage.getItem('diagnosisHistory') || '[]');
    
    // Add new diagnosis with timestamp
    const diagnosisWithTimestamp = {
      ...diagnosis,
      timestamp: new Date().toISOString(),
      id: Date.now()
    };
    
    // Add to history and save
    history.unshift(diagnosisWithTimestamp);
    localStorage.setItem('diagnosisHistory', JSON.stringify(history));
  }
  
  // Retrieve diagnosis history
  function getDiagnosisHistory() {
    return JSON.parse(localStorage.getItem('diagnosisHistory') || '[]');
}
  
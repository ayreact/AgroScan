const navDiagnosis = document.querySelectorAll(".diagBtn");
const navHistory = document.querySelectorAll(".historyBtn");

navDiagnosis.forEach((navDia) => {

    navDia.addEventListener('click', () => {
        localStorage.removeItem('lastDiagnosis');
        window.location.href = DiagnosisURL
    });
});

navHistory.forEach((navHis) => {

    navHis.addEventListener('click', () => {
        localStorage.removeItem('historyData');
        window.location.href = HistoryURL
    });
});

window.addEventListener('load', () => {
    const container = document.getElementById('agroscanButtons');
    if (!sessionStorage.getItem('agroscanClosed')) {
      setTimeout(() => {
        container.classList.add('slide-in');
      }, 1500); // 1.5 seconds delay
    }
  });

  document.getElementById('closeAgroscan').addEventListener('click', () => {
    const container = document.getElementById('agroscanButtons');
    container.classList.remove('slide-in');
    container.classList.add('slide-out');
    sessionStorage.setItem('agroscanClosed', 'true');
  });
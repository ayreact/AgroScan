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
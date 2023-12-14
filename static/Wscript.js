
document.addEventListener('DOMContentLoaded', function() {
    const selectRefereeBtn = document.getElementById('select-referee-btn');
    const selectedRefereeDiv = document.getElementById('selected-referee');
    const statusDiv = document.getElementById('status');

    selectRefereeBtn.addEventListener('click', function() {
        fetch('/weekend_selection')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.message === 'All referees have been selected') {
                    statusDiv.textContent = data.message;
                    selectedRefereeDiv.textContent = '';
                } else {
                    statusDiv.textContent = '';
                    selectedRefereeDiv.textContent = `Weekend ${data.weekend_num} Selection: ${data.selected_referee}`;
                }
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    });
});
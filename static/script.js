document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('weekend-selection-form');
    const status = document.getElementById('status');
    const selectedReferee = document.getElementById('selected-referee');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const weekendNum = document.getElementById('weekend_num').value;

        // Send the data to the server using AJAX
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/weekend_selection', true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    const response = JSON.parse(xhr.responseText);
                    status.textContent = response.message;
                    selectedReferee.textContent = `Selected Referee: ${response.selected_referee}`;
                } else {
                    status.textContent = 'Error: ' + xhr.statusText;
                }
            }
        };
        const data = `weekend_num=${encodeURIComponent(weekendNum)}`;
        xhr.send(data);
    });
});

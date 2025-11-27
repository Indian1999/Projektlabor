async function loadLogs() {
    try {
        const response = await fetch('/api/logs');
        const data = await response.json();

        if (response.ok) {
            const logsContainer = document.getElementById('logsContainer');
            if (data.logs && data.logs.length > 0) {
                logsContainer.textContent = data.logs.join('');
            } else {
                logsContainer.innerHTML = '<p class="text-muted">Nincs napló bejegyzés</p>';
            }
        } else {
            document.getElementById('logsContainer').innerHTML = '<p class="text-danger">Hiba a naplók betöltésekor: ' + (data.error || 'Unknown error') + '</p>';
        }
    } catch (error) {
        console.error('Error loading logs:', error);
        document.getElementById('logsContainer').innerHTML = '<p class="text-danger">Hiba: ' + error.message + '</p>';
    }
}

function refreshLogs() {
    loadLogs();
}

document.addEventListener('DOMContentLoaded', function() {
    loadLogs();
});

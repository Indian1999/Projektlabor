document.addEventListener('DOMContentLoaded', function() {
    loadStats();
});

async function loadStats() {
    try {
        const response = await fetch('/api/stats');
        const stats = await response.json();
        
        document.getElementById('totalResults').textContent = stats.total_results;
        document.getElementById('activeProcesses').textContent = stats.active_processes;
        document.getElementById('nValues').textContent = stats.n_values.length;
        
        displayBestResults(stats.best_by_n, stats.n_values);
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

function displayBestResults(bestByN, nValues) {
    const container = document.getElementById('bestResults');
    
    if (nValues.length === 0) {
        container.innerHTML = '<p class="text-muted">Még nincsenek eredmények</p>';
        return;
    }
    
    nValues.sort((a, b) => a - b);
    
    let tableHTML = `
        <div class="table-responsive">
            <table class="table table-hover">
                <thead class="table-light">
                    <tr>
                        <th>N érték</th>
                        <th>Legjobb megoldás értéke</th>
                        <th>Megtekintés</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    for (const n of nValues) {
        const score = bestByN[n] || '-';
        tableHTML += `
            <tr>
                <td><strong>N = ${n}</strong></td>
                <td><span class="badge bg-success fs-6">${score}</span></td>
                <td>
                    <a href="/browse?n=${n}" class="btn btn-sm btn-primary">Megtekintés</a>
                </td>
            </tr>
        `;
    }
    
    tableHTML += `
                </tbody>
            </table>
        </div>
    `;
    
    container.innerHTML = tableHTML;
}

setInterval(loadStats, 5000);
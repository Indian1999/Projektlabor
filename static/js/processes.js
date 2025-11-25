document.addEventListener('DOMContentLoaded', function() {
    loadProcesses();
    setInterval(loadProcesses, 3000);
});

async function loadProcesses() {
    try {
        const response = await fetch('/api/processes');
        const data = await response.json();
        
        displayProcesses(data.processes, data.active_index);
        document.getElementById('processCount').textContent = data.processes.length;
    } catch (error) {
        console.error('Error loading processes:', error);
    }
}

function displayProcesses(processes, activeIndex) {
    const container = document.getElementById('processesList');
    
    if (processes.length === 0) {
        container.innerHTML = '<p class="text-muted text-center p-5">Nincs aktív folyamat</p>';
        return;
    }
    
    let html = '';
    processes.forEach((process, index) => {
        const isActive = index === activeIndex;
        const processType = process.population_size !== undefined ? 'Genetic' : 'Constructive';
        const borderClass = isActive ? 'border-success border-3' : '';
        const bgClass = isActive ? 'bg-success bg-opacity-10' : '';
        
        html += `
            <div class="card mb-3 ${borderClass} ${bgClass} shadow-sm">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-3">
                        <div>
                            <h5 class="card-title mb-1">
                                ${processType} Algorithm 
                                ${isActive ? '<span class="badge bg-success ms-2">AKTÍV</span>' : ''}
                            </h5>
                            <p class="card-text text-muted mb-0">
                                <strong>N:</strong> ${process.n} | <strong>Prioritás:</strong> ${process.priority}
                            </p>
                        </div>
                        <div class="btn-group">
                            ${!isActive ? `
                                <button onclick="activateProcess(${index})" class="btn btn-sm btn-success">
                                    Aktiválás
                                </button>
                            ` : ''}
                            <button onclick="terminateProcess(${index})" class="btn btn-sm btn-danger">
                                Leállítás
                            </button>
                        </div>
                    </div>
                    <div class="row g-3 small">
                        ${getProcessDetails(process, processType)}
                    </div>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

function getProcessDetails(process, type) {
    if (type === 'Genetic') {
        return `
            <div class="col-md-4"><strong>Populáció:</strong> ${process.population_size}</div>
            <div class="col-md-4"><strong>Generációk:</strong> ${process.generations || '∞'}</div>
            <div class="col-md-4"><strong>Mutációs ráta:</strong> ${process.mutation_rate}</div>
            <div class="col-md-4"><strong>Pontosság:</strong> ${process.accuracy}</div>
            <div class="col-md-4"><strong>Fitness mód:</strong> ${process.fitness_mode}</div>
            <div class="col-md-4"><strong>Reach:</strong> ${process.reach || 'auto'}</div>
        `;
    } else {
        return `
            <div class="col-md-3"><strong>Stratégia:</strong> ${process.strategy}</div>
            <div class="col-md-3"><strong>Iterációk:</strong> ${process.iterations}</div>
            <div class="col-md-3"><strong>Pontosság:</strong> ${process.accuracy}</div>
            <div class="col-md-3"><strong>Reach:</strong> ${process.reach || 'auto'}</div>
        `;
    }
}

async function activateProcess(index) {
    if (!confirm('Biztosan aktiválni szeretnéd ezt a folyamatot? Ez megállítja az aktív folyamatot.')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/processes/${index}/activate`, {
            method: 'POST'
        });
        
        if (response.ok) {
            loadProcesses();
        } else {
            alert('Hiba történt a folyamat aktiválásakor');
        }
    } catch (error) {
        console.error('Error activating process:', error);
        alert('Hiba történt');
    }
}

async function terminateProcess(index) {
    if (!confirm('Biztosan leállítod ezt a folyamatot?')) {
        return;
    }
    
    const response = await fetch(`/api/processes/${index}/terminate`, {
        method: 'POST'
    });
    
    if (response.ok) {
        loadProcesses();
    } else {
        alert('Hiba történt a folyamat leállításakor');
    }
}

function refreshProcesses() {
    loadProcesses();
}
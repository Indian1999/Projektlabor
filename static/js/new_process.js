document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('newProcessForm').addEventListener('submit', handleSubmit);
    updateFormFields();
});

function updateFormFields() {
    const type = document.querySelector('input[name="type"]:checked').value;
    
    const geneticParams = document.getElementById('geneticParams');
    const constructiveParams = document.getElementById('constructiveParams');
    
    if (type === 'genetic') {
        geneticParams.style.display = 'block';
        constructiveParams.style.display = 'none';
    } else {
        geneticParams.style.display = 'none';
        constructiveParams.style.display = 'block';
    }
}

async function handleSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const type = formData.get('type');
    
    const payload = {
        type: type,
        n: parseInt(formData.get('n')),
        accuracy: parseInt(formData.get('accuracy')),
        priority: parseInt(formData.get('priority')),
        start_immediately: formData.get('start_immediately') === 'on'
    };
    
    if (type === 'genetic') {
        payload.population_size = parseInt(formData.get('population_size'));
        payload.generations = parseInt(formData.get('generations'));
        payload.mutation_rate = parseFloat(formData.get('mutation_rate'));
        payload.fitness_mode = parseInt(formData.get('fitness_mode'));
        payload.reach = null; // Auto
    } else {
        payload.strategy = formData.get('strategy');
        payload.iterations = parseInt(formData.get('iterations'));
        payload.reach = null; // Auto
    }
    
    if (payload.n < 8 || payload.n > 200) {
        showStatus('error', 'N-nek 8 és 200 között kell lennie!');
        return;
    }

    if (type === 'constructive') {
        if (payload.iterations < 1 || payload.iterations > 10) {
            showStatus('error', 'Az iterációk száma 1 és 10 között kell legyen!');
            return;
        }
    }
    
    showStatus('info', 'Folyamat indítása...');
    
    try {
        const response = await fetch('/api/processes/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        if (response.ok) {
            showStatus('success', 'Folyamat sikeresen elindítva!');
            setTimeout(() => {
                window.location.href = '/processes';
            }, 1500);
        } else {
            const error = await response.json();
            showStatus('error', `Hiba: ${error.error || 'Ismeretlen hiba'}`);
        }
    } catch (error) {
        console.error('Error adding process:', error);
        showStatus('error', 'Hálózati hiba történt');
    }
}

function showStatus(type, message) {
    const statusDiv = document.getElementById('formStatus');
    
    let alertClass = 'alert-info';
    if (type === 'success') alertClass = 'alert-success';
    if (type === 'error') alertClass = 'alert-danger';
    
    statusDiv.className = `alert ${alertClass}`;
    statusDiv.textContent = message;
    statusDiv.style.display = 'block';
    
    if (type === 'success') {
        setTimeout(() => {
            statusDiv.style.display = 'none';
        }, 3000);
    }
}
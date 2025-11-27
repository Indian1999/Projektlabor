let scene, camera, renderer, controls;
let cubes = [];
let gridHelper;
let currentData = null;
let selectedN = null;
let lastNValues = [];

document.addEventListener('DOMContentLoaded', function() {
    init3DViewer();
    loadNValues();

    const urlParams = new URLSearchParams(window.location.search);
    const nParam = urlParams.get('n');
    if (nParam) {
        selectedN = parseInt(nParam);
        setTimeout(() => selectN(parseInt(nParam)), 500);
    }

    // Amúgy nem frissíteni a results lista új értékeivel
    // setInterval(loadNValues, 3000); Nice try, de nem jó ötlet, three.js-t is frissíti
});

async function loadNValues() {
    try {
        const response = await fetch('/api/results');
        const resultsByN = await response.json();

        const nSelector = document.getElementById('nSelector');
        const nValues = Object.keys(resultsByN).map(Number).sort((a, b) => a - b);

        if (nValues.length === 0) {
            nSelector.innerHTML = '<p class="placeholder">Nincsenek eredmények</p>';
            selectedN = null;
            lastNValues = [];
            return;
        }

        const nValuesChanged = JSON.stringify(nValues) !== JSON.stringify(lastNValues);

        if (nValuesChanged) {
            let html = '';
            for (const n of nValues) {
                const count = resultsByN[n].length;
                const isSelected = selectedN === n ? 'btn-primary' : 'btn-outline-primary';
                html += `
                    <button class="btn ${isSelected} w-100 n-btn" data-n="${n}">
                        N = ${n} <span class="badge bg-secondary">${count}</span>
                    </button>
                `;
            }

            nSelector.innerHTML = html;

            // eseménykezelő onClick helyett, mert új n érték esetén kibugoltatja az eredmények megjelenítését
            document.querySelectorAll('.n-btn').forEach(btn => {
                btn.addEventListener('click', function() {
                    selectN(parseInt(this.getAttribute('data-n')));
                });
            });

            lastNValues = nValues;
        } else {
            for (const n of nValues) {
                const btn = document.querySelector(`[data-n="${n}"]`);
                if (btn) {
                    const isSelected = selectedN === n;
                    if (isSelected) {
                        btn.classList.remove('btn-outline-primary');
                        btn.classList.add('btn-primary');
                    } else {
                        btn.classList.add('btn-outline-primary');
                        btn.classList.remove('btn-primary');
                    }
                    const count = resultsByN[n].length;
                    btn.querySelector('.badge').textContent = count;
                }
            }
        }

        if (selectedN !== null && nValues.includes(selectedN)) {
            // Itt lehet, hogy még nem fejeződött be a fetch, ugyhogy várunk
            setTimeout(refreshSelectedResults, 100);
        }
    } catch (error) {
        console.error('Error in loadNValues():', error);
    }
}

async function selectN(n) {
    selectedN = n;
    document.getElementById('selectedN').textContent = n;

    document.querySelectorAll('.n-btn').forEach(btn => {
        btn.classList.remove('btn-primary');
        btn.classList.add('btn-outline-primary');
    });

    const selectedBtn = document.querySelector(`[data-n="${n}"]`);
    if (selectedBtn) {
        selectedBtn.classList.remove('btn-outline-primary');
        selectedBtn.classList.add('btn-primary');
    }

    refreshSelectedResults();
}

async function refreshSelectedResults() {
    if (selectedN === null) return;

    try {
        const response = await fetch(`/api/results/${selectedN}`);
        const results = await response.json();

        displayResults(results);
    } catch (error) {
        console.error('Error loading results:', error);
    }
}

function displayResults(results) {
    const container = document.getElementById('resultsList');
    
    if (results.length === 0) {
        container.innerHTML = '<p class="text-muted">Nincsenek eredmények</p>';
        return;
    }
    
    let html = '';
    results.forEach((result, index) => {
        html += `
            <div class="card mb-2 result-item" onclick="loadResult(${index})" style="cursor: pointer;">
                <div class="card-body p-3">
                    <h5 class="card-title text-success mb-2">${result.result}</h5>
                    <p class="card-text mb-1"><strong>N:</strong> ${result.n}</p>
                    <p class="card-text mb-1"><strong>Pontosság:</strong> ${result.accuracy}</p>
                    <p class="card-text mb-0"><strong>Kockák:</strong> ${result.cubes.length}</p>
                ${result.date ? `<p class="card-text mb-0"><strong>Dátum:</strong> ${result.date}</p>` : ''}
                </div>
            </div>
        `;
        // A result.date egy újabb paraméter, a régieknér nincs, ezért feltételes a betöltése
    });
    
    container.innerHTML = html;
    
    window.currentResults = results;
    
    if (results.length > 0) {
        loadResult(0);
    }
}

function loadResult(index) {
    const result = window.currentResults[index];

    document.querySelectorAll('.result-item').forEach((item, i) => {
        if (i === index) {
            item.classList.add('border-primary', 'border-3');
            item.classList.remove('border');
        } else {
            item.classList.remove('border-primary', 'border-3');
            item.classList.add('border');
        }
    });

    render3D(result);

    updateCubeInfo(result);

    document.getElementById('downloadBtn').style.display = 'inline-block';
}

function init3DViewer() {
    const container = document.getElementById('viewer3d');
    container.innerHTML = '';
    
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf0f0f0);
    
    const aspect = container.clientWidth / container.clientHeight;
    camera = new THREE.PerspectiveCamera(75, aspect, 0.1, 1000);
    camera.position.set(20, 20, 20);
    camera.lookAt(0, 0, 0);
    
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(renderer.domElement);
    
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true; 
    controls.dampingFactor = 0.05;
    controls.screenSpacePanning = false;
    controls.minDistance = 5;
    controls.maxDistance = 500;
    controls.maxPolarAngle = Math.PI;
    
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(10, 10, 10);
    scene.add(directionalLight);
    
    gridHelper = new THREE.GridHelper(50, 50);
    scene.add(gridHelper);
    
    animate();
    
    window.addEventListener('resize', onWindowResize);
}

function render3D(data) {
    currentData = data;
    
    cubes.forEach(cube => scene.remove(cube));
    cubes = [];
    
    if (!data || !data.cubes) return;
    
    let maxCoord = data.n || 10;
    
    data.cubes.forEach((cubeData, index) => {
        const geometry = new THREE.BoxGeometry(cubeData.size, cubeData.size, cubeData.size);
        
        let color;
        let opacity;
        
        if (index === 0) {
            color = 0xff4444; 
            opacity = 0.9; 
        } else {
            const hue = ((index - 1) / (data.cubes.length - 1)) * 360;
            color = new THREE.Color().setHSL(hue / 360, 0.8, 0.6);
            opacity = 0.8; 
        }
        
        const material = new THREE.MeshPhongMaterial({ 
            color: color,
            transparent: true,
            opacity: opacity,
            side: THREE.DoubleSide
        });
        
        const cube = new THREE.Mesh(geometry, material);
        
        cube.position.set(
            cubeData.x + cubeData.size / 2 - maxCoord / 2,
            cubeData.y + cubeData.size / 2,
            cubeData.z + cubeData.size / 2 - maxCoord / 2
        );
        
        const edges = new THREE.EdgesGeometry(geometry);
        const line = new THREE.LineSegments(
            edges, 
            new THREE.LineBasicMaterial({ color: 0x000000, linewidth: 2 })
        );
        cube.add(line);
        
        scene.add(cube);
        cubes.push(cube);
    });
    
    camera.position.set(maxCoord * 1.5, maxCoord * 1.5, maxCoord * 1.5);
    camera.lookAt(0, maxCoord / 2, 0);
}

function animate() {
    requestAnimationFrame(animate);
    
    if (controls) {
        controls.update();
    }
    
    renderer.render(scene, camera);
}

function onWindowResize() {
    const container = document.getElementById('viewer3d');
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
}

function resetCamera() {
    if (!currentData) return;
    const maxCoord = currentData.n || 10;
    camera.position.set(maxCoord * 1.5, maxCoord * 1.5, maxCoord * 1.5);
    camera.lookAt(0, maxCoord / 2, 0);
    
    if (controls) {
        controls.target.set(0, maxCoord / 2, 0);
        controls.update();
    }
}

function toggleGrid() {
    const checkbox = document.getElementById('showGrid');
    gridHelper.visible = checkbox.checked;
}

function updateCubeInfo(data) {
    const container = document.getElementById('cubeInfo');
    
    if (!data) {
        container.innerHTML = '<p>Nincs betöltött megoldás</p>';
        return;
    }
    
    const html = `
        <div><strong>Megoldás értéke:</strong> ${data.result}</div>
        <div><strong>N:</strong> ${data.n}</div>
        <div><strong>Pontosság:</strong> ${data.accuracy}</div>
        <div><strong>Kockák száma:</strong> ${data.cubes.length}</div>
        <hr style="margin: 0.5rem 0;">
        <div style="max-height: 200px; overflow-y: auto;">
            ${data.cubes.map((c, i) => {
                return `
                <div style="margin: 0.25rem 0;">
                    <strong>${i}:</strong> 
                    size=${c.size}, pos=(${c.x}, ${c.y}, ${c.z})
                </div>
            `}).join('')}
        </div>
    `;
    
    container.innerHTML = html;
}

function downloadSolution() {
    if (!currentData) {
        alert('Nincs betöltött megoldás!');
        return;
    }

    const jsonData = {
        n: currentData.n,
        result: currentData.result,
        accuracy: currentData.accuracy,
        cubes: currentData.cubes
    };

    const jsonString = JSON.stringify(jsonData, null, 2);

    const blob = new Blob([jsonString], { type: 'application/json' });

    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `megoldas_n${currentData.n}_${currentData.result}.json`;

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    URL.revokeObjectURL(url);
}
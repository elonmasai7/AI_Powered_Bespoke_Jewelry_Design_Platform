let scene, camera, renderer, controls, currentModel;

function initThreeJS() {
    const canvas = document.querySelector('#3dCanvas');
    
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, canvas.clientWidth / canvas.clientHeight, 0.1, 1000);
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
    renderer.setSize(canvas.clientWidth, canvas.clientHeight);
    renderer.setClearColor(0x1a1a1a);

    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(5, 5, 5);
    scene.add(directionalLight);

    controls = new THREE.OrbitControls(camera, renderer.domElement);
    camera.position.z = 5;

    function animate() {
        requestAnimationFrame(animate);
        if (currentModel) currentModel.rotation.y += 0.01;
        controls.update();
        renderer.render(scene, camera);
    }
    animate();
}

async function generateDesign() {
    const prompt = document.getElementById('prompt').value;
    const jewelryType = document.getElementById('jewelryType').value;
    const material = document.getElementById('material').value;
    
    showLoading(true);
    
    try {
        // Generate 2D
        const imageResponse = await fetch('/generate-2d', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt })
        });
        
        const imageData = await imageResponse.json();
        if(imageData.error) throw new Error(imageData.error);
        addToGallery(imageData.image, prompt, material);

        // Generate 3D
        const modelResponse = await fetch('/generate-3d', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                prompt: `${prompt} (${material})`,
                type: jewelryType
            })
        });
        
        const modelData = await modelResponse.json();
        if(modelData.error) throw new Error(modelData.error);
        if(modelData.model_url) load3DModel(modelData.model_url);

    } catch(error) {
        showError(error.message);
    } finally {
        showLoading(false);
    }
}

function load3DModel(url) {
    if(currentModel) scene.remove(currentModel);
    
    new THREE.GLTFLoader().load(url, (gltf) => {
        currentModel = gltf.scene;
        currentModel.scale.set(0.1, 0.1, 0.1);
        
        const box = new THREE.Box3().setFromObject(currentModel);
        const center = box.getCenter(new THREE.Vector3());
        currentModel.position.sub(center);
        
        scene.add(currentModel);
    });
}

function addToGallery(imageData, prompt, material) {
    const gallery = document.getElementById('gallery');
    const card = document.createElement('div');
    card.className = 'design-card';
    card.innerHTML = `
        <img src="data:image/webp;base64,${imageData}">
        <div class="card-body">
            <p>${prompt}</p>
            <div class="material-tag">${material}</div>
        </div>
    `;
    gallery.prepend(card);
}

function showLoading(show) {
    document.getElementById('loading').style.display = show ? 'grid' : 'none';
}

function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    document.body.prepend(errorDiv);
    setTimeout(() => errorDiv.remove(), 5000);
}

// Event Listeners
document.getElementById('designForm').addEventListener('submit', (e) => {
    e.preventDefault();
    generateDesign();
});

document.getElementById('resetBtn').addEventListener('click', () => {
    controls.reset();
    camera.position.z = 5;
});

// Initialize
initThreeJS();

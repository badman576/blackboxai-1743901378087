import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

class Avatar3D {
    constructor() {
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({ alpha: true });
        this.renderer.setSize(300, 300);
        document.getElementById('3d-avatar-container').appendChild(this.renderer.domElement);
        
        this.loader = new GLTFLoader();
        this.clock = new THREE.Clock();
        this.mixer = null;
        
        this.initScene();
        this.animate();
    }

    initScene() {
        // Lights
        const light = new THREE.DirectionalLight(0xffffff, 1);
        light.position.set(0, 1, 1);
        this.scene.add(light);
        
        // Load 3D model
        this.loader.load(
            '/static/models/ai_avatar.glb',
            (gltf) => {
                this.model = gltf.scene;
                this.scene.add(this.model);
                
                // Set up animations
                this.mixer = new THREE.AnimationMixer(this.model);
                gltf.animations.forEach((clip) => {
                    this.mixer.clipAction(clip).play();
                });
            },
            undefined,
            (error) => {
                console.error('Error loading 3D model:', error);
            }
        );
        
        this.camera.position.z = 2;
    }

    animate() {
        requestAnimationFrame(() => this.animate());
        
        const delta = this.clock.getDelta();
        if (this.mixer) this.mixer.update(delta);
        
        this.renderer.render(this.scene, this.camera);
    }

    setEmotion(emotion) {
        // Change animation based on state
        if (this.mixer) {
            // Implementation would depend on your 3D model's animations
        }
    }
}

export default Avatar3D;
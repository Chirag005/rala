import * as THREE from 'three'
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js'
export default defineNuxtPlugin(() => {
  const three = {
    createGreenhouseScene: (canvas: any) => {
      const scene = new THREE.Scene()
      const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)
      const renderer = new THREE.WebGLRenderer({ canvas, alpha: true })
      renderer.setSize(window.innerWidth, window.innerHeight)
      // Add wireframe greenhouse model (load GLTF)
      const loader = new GLTFLoader()
      loader.load('/models/greenhouse.gltf', (gltf: { scene: THREE.Object3D<THREE.Object3DEventMap> }) => scene.add(gltf.scene))
      // Energy particles: PointsMaterial with emerald color
      const particles = new THREE.BufferGeometry().setFromPoints(new Array(1000).fill(0).map(() => new THREE.Vector3(Math.random() * 10 - 5, Math.random() * 10 - 5, 0)))
      const material = new THREE.PointsMaterial({ color: 0x10B981, size: 0.05 })
      scene.add(new THREE.Points(particles, material))
      camera.position.z = 5
      return scene
    },
    animateParticles: (scene: { children: { rotation: { y: number } }[] }) => {
      /* Update positions for flow effect */
      if (scene.children[1]) {
        scene.children[1].rotation.y += 0.01
      }
    }
  }
  return { provide: { three } }
})
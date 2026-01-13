import * as THREE from 'three'

export default defineNuxtPlugin(() => {
  return {
    provide: {
      three: {
        createParticleField: (canvas: HTMLCanvasElement, mouse: { x: number; y: number }) => {
          const scene = new THREE.Scene()
          const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)
          const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true }) // Added antialias for smoother
          renderer.setSize(window.innerWidth, window.innerHeight)
          renderer.setClearColor(0x000000, 0) // Transparent clear for better blending
          
          // Particle system: Increased to 5000 points for density
          const particles = new THREE.BufferGeometry()
          const positions = new Float32Array(5000 * 50)
          for (let i = 0; i < positions.length; i += 3) {
            positions[i] = (Math.random() - 0.5) * 300 // Wider spread
            positions[i + 1] = (Math.random() - 0.5) * 300
            positions[i + 2] = (Math.random() - 0.5) * 300
          }
          particles.setAttribute('position', new THREE.BufferAttribute(positions, 3))
          
          // Add glow texture for better visibility (simple star sprite)
          const textureLoader = new THREE.TextureLoader()
          const sprite = textureLoader.load('https://threejs.org/examples/textures/sprites/disc.png') // Public glow texture; replace if needed
          
          const material = new THREE.PointsMaterial({
            color: 0x10B981, // RAALA green
            size: 0.3, // Larger for visibility
            map: sprite, // Adds glow
            blending: THREE.AdditiveBlending,
            transparent: true,
            depthWrite: false
          })
          
          const particleSystem = new THREE.Points(particles, material)
          scene.add(particleSystem)
          

          
          camera.position.z = 100 // Pulled back for wider view
          
          let time = 0 // For pulse animation
          const animate = () => {
            requestAnimationFrame(animate)
            time += 0.01
            // Gentle flow + cursor response + pulse
            particleSystem.rotation.y += 0.0005
            particleSystem.position.x = (mouse.x - 0.5) * 20 // Stronger tilt
            particleSystem.position.y = (mouse.y - 0.5) * -20
            particleSystem.scale.set(1 + Math.sin(time) * 0.1, 1 + Math.sin(time) * 0.1, 1) // Subtle breathing
            

            
            renderer.render(scene, camera)
          }
          animate()
          
          // Resize handler
          const onResize = () => {
            camera.aspect = window.innerWidth / window.innerHeight
            camera.updateProjectionMatrix()
            renderer.setSize(window.innerWidth, window.innerHeight)
          }
          window.addEventListener('resize', onResize)
          
          return { scene, renderer, cleanup: () => window.removeEventListener('resize', onResize) } // For potential unmount
        }
      }
    }
  }
})
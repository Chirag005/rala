<template>
  <footer class="footer">
    <div class="footer-container">
      <div class="footer-grid">
        
        <!-- Brand Column -->
        <div class="brand-column">
          <a href="#" class="brand-link">
            <span class="brand-name">RAALA</span>
          </a>
          <p class="brand-description">
            Autonomous Greenhouse OS powered by AI Agents and Reinforcement Learning. Optimizing energy, maximizing yields, and securing the future of food.
          </p>
          
          <!-- Socials -->
          <div class="social-links">
            <a href="#" class="social-link">
              <span class="sr-only">Twitter</span>
              <svg class="social-icon" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
            </a>
            <a href="#" class="social-link">
              <span class="sr-only">LinkedIn</span>
              <svg class="social-icon" viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
            </a>
            <a href="#" class="social-link">
              <span class="sr-only">GitHub</span>
              <svg class="social-icon" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
            </a>
          </div>
        </div>
        
        <!-- Links Columns -->
        <div class="links-column">
          <h4 class="links-heading">Platform</h4>
          <ul class="links-list">
            <li><a href="#mission" class="link-item">Mission</a></li>
            <li><a href="#how" class="link-item">Technology</a></li>
            <li><a href="#" class="link-item">Case Studies</a></li>
            <li><a href="#gtm" class="link-item">Roadmap</a></li>
          </ul>
        </div>

        <div class="links-column">
          <h4 class="links-heading">Company</h4>
          <ul class="links-list">
            <li><a href="#" class="link-item">About Us</a></li>
            <li>
              <a href="#" class="link-item">Careers</a> 
              <span class="hiring-badge">Hiring</span>
            </li>
            <li><a href="#" class="link-item">Press</a></li>
            <li><a href="#" class="link-item">Contact</a></li>
          </ul>
        </div>

        <div class="links-column resources-column">
          <h4 class="links-heading">Resources</h4>
          <ul class="links-list">
            <li><a href="#" class="link-item">Documentation</a></li>
            <li><a href="#" class="link-item">API Reference</a></li>
            <li><a href="#" class="link-item">System Status</a></li>
            <li><a href="#" class="link-item">Privacy</a></li>
          </ul>
        </div>
      </div>

      <!-- Bottom Bar -->
      <div class="footer-bottom">
        <div class="copyright">
          &copy; <span>{{ currentYear }}</span> RAALA Systems Inc. All rights reserved.
        </div>
        <div class="status-container">
          <div class="status-badge">
            <span class="status-indicator">
              <span class="status-ping"></span>
              <span class="status-dot"></span>
            </span>
            <span class="status-text">SYSTEM ONLINE</span>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { ref } from 'vue'

const currentYear = ref(new Date().getFullYear())
</script>

<style scoped>
/* Footer */
.footer {
  background-color: #000;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 5rem;
  padding-bottom: 2.5rem;
  margin-top: auto;
  position: relative;
  z-index: 10;
}

.footer-container {
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

/* Grid Layout */
.footer-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 3rem 2rem;
  margin-bottom: 5rem;
}

@media (min-width: 768px) {
  .footer-grid {
    grid-template-columns: repeat(12, 1fr);
    gap: 3rem 2rem;
  }
}

/* Brand Column */
.brand-column {
  grid-column: span 2;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 1.5rem;
}

@media (min-width: 768px) {
  .brand-column {
    grid-column: 1 / span 5;
  }
}

@media (min-width: 1024px) {
  .brand-column {
    grid-column: 1 / span 6;
  }
}

.brand-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
}

.brand-name {
  font-size: 1.25rem;
  font-weight: 700;
  letter-spacing: -0.025em;
  color: #fff;
  transition: color 300ms ease;
}

.brand-link:hover .brand-name {
  color: #10b981;
}

.brand-description {
  color: #71717a;
  font-size: 0.875rem;
  line-height: 1.6;
  max-width: 28rem;
}

/* Social Links */
.social-links {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding-top: 0.5rem;
}

.social-link {
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 9999px;
  background-color: #18181b;
  border: 1px solid #27272a;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #a1a1aa;
  text-decoration: none;
  transition: all 300ms ease;
}

.social-link:hover {
  color: #fff;
  border-color: rgba(16, 185, 129, 0.5);
  background-color: #27272a;
}

.social-icon {
  width: 1rem;
  height: 1rem;
  fill: currentColor;
  transition: transform 300ms ease;
}

.social-link:hover .social-icon {
  transform: scale(1.1);
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

/* Links Columns */
.links-column {
  grid-column: span 1;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

@media (min-width: 768px) {
  .links-column {
    grid-column: span 2;
  }
  
  /* Position links on the right side */
  .links-column:nth-child(2) {
    grid-column: 7 / span 2;
  }
  
  .links-column:nth-child(3) {
    grid-column: 9 / span 2;
  }
  
  .links-column:nth-child(4) {
    grid-column: 11 / span 2;
  }
}

@media (min-width: 1024px) {
  .links-column:nth-child(2) {
    grid-column: 8 / span 2;
  }
  
  .links-column:nth-child(3) {
    grid-column: 10 / span 2;
  }
  
  .links-column:nth-child(4) {
    grid-column: 12 / span 1;
  }
}

.links-heading {
  font-weight: 600;
  color: #fff;
  font-size: 0.875rem;
  letter-spacing: -0.025em;
}

.links-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  list-style: none;
  padding: 0;
  margin: 0;
  font-size: 0.875rem;
  color: #71717a;
}

.link-item {
  color: #71717a;
  text-decoration: none;
  transition: color 300ms ease;
}

.link-item:hover {
  color: #10b981;
}

.hiring-badge {
  font-size: 0.625rem;
  background-color: #27272a;
  color: #d4d4d8;
  padding: 0.125rem 0.375rem;
  border-radius: 0.25rem;
  margin-left: 0.25rem;
}

/* Footer Bottom */
.footer-bottom {
  border-top: 1px solid rgba(255, 255, 255, 0.02);
  padding-top: 2rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  font-size: 0.75rem;
}

@media (min-width: 768px) {
  .footer-bottom {
    flex-direction: row;
  }
}

.copyright {
  color: #52525b;
}

.status-container {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  background-color: rgba(24, 24, 27, 0.5);
  border: 1px solid rgba(39, 39, 42, 0.5);
}

.status-indicator {
  position: relative;
  display: flex;
  height: 0.375rem;
  width: 0.375rem;
}

.status-ping {
  position: absolute;
  display: inline-flex;
  height: 100%;
  width: 100%;
  border-radius: 9999px;
  background-color: #10b981;
  opacity: 0.75;
  animation: ping 2s cubic-bezier(0, 0, 0.2, 1) infinite;
}

.status-dot {
  position: relative;
  display: inline-flex;
  border-radius: 9999px;
  height: 0.375rem;
  width: 0.375rem;
  background-color: #10b981;
}

.status-text {
  font-family: 'JetBrains Mono', monospace;
  color: rgba(16, 185, 129, 0.9);
  letter-spacing: 0.05em;
}

/* Animations */
@keyframes ping {
  75%, 100% {
    transform: scale(2);
    opacity: 0;
  }
}
</style>

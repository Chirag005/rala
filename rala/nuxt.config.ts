// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  ssr: true, // Hybrid: SSR for SEO, client for animations
  css: ['~/assets/css/main.css'], // Tailwind imports
  modules: ['@nuxtjs/tailwindcss', '@nuxtjs/supabase'],
  supabase: {
    url: process.env.NUXT_PUBLIC_SUPABASE_URL,
    key: process.env.NUXT_PUBLIC_SUPABASE_KEY,
    redirect: false
  },
  nitro: { prerender: { routes: ['/'] } }, // SSG homepage
  app: { head: { meta: [{ name: 'og:title', content: 'RALA: Autonomous Greenhouse OS – Cut Energy 30%, Boost Yields 12%' }] } },
  vue: {
    compilerOptions: {
      isCustomElement: (tag) => tag === 'iconify-icon'
    }
  }
})
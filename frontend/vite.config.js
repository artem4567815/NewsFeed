import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'url';

// https://vite.dev/config/
export default defineConfig({
  define: {
    optimizeDeps: {
      include: ['fabric']
    },
    'process.env': process.env,
  },
  plugins: [vue(),tailwindcss()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
})

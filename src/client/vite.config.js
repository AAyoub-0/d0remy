import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/songs': 'http://127.0.0.1:8000',
      '/playlists': 'http://127.0.0.1:8000',
      '/media': 'http://127.0.0.1:8000'
    }
  }
})

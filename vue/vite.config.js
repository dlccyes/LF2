import { fileURLToPath, URL } from 'url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'

// https://vitejs.dev/config/
APP_ENV = process.env.APP_ENV;
// APP_ENV = 'production';
APP_ENV = 'development';
export default defineConfig({
  plugins: [vue(), vueJsx()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  base: APP_ENV === 'development' ? '/' : '/LF2/vue/dist/',
})

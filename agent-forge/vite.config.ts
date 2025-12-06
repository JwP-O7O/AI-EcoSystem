import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  return {
    define: {
      'process.env': {
        ...env,
        API_KEY: env.VITE_API_KEY
      }
    },
    plugins: [react()],

    server: {
      host: true,
      port: 3001, // We use 3001 to avoid conflict with the bot on 3000
      hmr: { overlay: false }
    }
  }
})

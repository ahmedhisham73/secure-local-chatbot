import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import fs from 'fs'

// Define the path to your certificates
const certPath = '/home/ahmedetsh/Desktop/chatbot_enterprise_local/certs';

export default defineConfig({
  plugins: [react()],
  server: {
    https: {
      key: fs.readFileSync(`${certPath}/key.pem`),  // Path to your private key
      cert: fs.readFileSync(`${certPath}/cert.pem`), // Path to your certificate
    },
    proxy: {
      '/login': {
        target: 'https://localhost:8443',
        changeOrigin: true,
        secure: false,  // If using self-signed certificates, disable SSL verification
      },
      '/chat': {
        target: 'https://localhost:8443',
        changeOrigin: true,
        secure: false,  // If using self-signed certificates, disable SSL verification
      },
    }
  }
})


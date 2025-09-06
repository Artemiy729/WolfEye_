import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), 'VITE_')
  const isDev = mode === 'development'
  const isStaging = mode === 'staging'

  return {
    plugins: [react()],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },
    server: {
      host: true,
      port: 5173,
      open: isDev,
      strictPort: true,
      hmr: { overlay: true },
    },
    preview: {
      host: true,
      port: 4173,
      strictPort: true,
    },
    esbuild: {
      target: 'es2022',
    },
    build: {
      target: 'es2022',
      sourcemap: isDev ? 'inline' : isStaging ? 'hidden' : false,
      minify: 'esbuild',
      reportCompressedSize: false,
      chunkSizeWarningLimit: 600,
      rollupOptions: {
        output: {
          manualChunks: {
            react: ['react', 'react-dom'],
          },
        },
      },
    },
    optimizeDeps: {
      esbuildOptions: { target: 'es2022' },
    },
    define: {
      __APP_ENV__: JSON.stringify(mode),
      __API_URL__: JSON.stringify(env.VITE_API_URL ?? ''),
    },
  }
})
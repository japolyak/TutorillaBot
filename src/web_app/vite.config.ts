import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url';
import vueI18N from '@intlify/unplugin-vue-i18n/vite';
import { resolveFileURL } from './src/plugins/vite';

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [
		vue(),
		vueI18N({
			include: resolveFileURL(import.meta.url, 'src/plugins/i18n/locales/*.json'),
		}),
	],
	define: {
		'__VUE_PROD_HYDRATION_MISMATCH_DETAILS__': true,
	},
    resolve: {
    // https://vitejs.dev/config/shared-options.html#resolve-alias
		alias: {
			'@': fileURLToPath(new URL('./src', import.meta.url)),
			'~': fileURLToPath(new URL('./node_modules', import.meta.url)),
		},
		extensions: ['.js', '.json', '.jsx', '.mjs', '.ts', '.tsx', '.vue'],
		dedupe: ['vue'],
    },
})

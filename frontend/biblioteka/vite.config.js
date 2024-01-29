import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';

export default defineConfig({
	proxy:{
		'/api': {
			target: 'http://127.0.0.1:8000',  // Your Django backend URL
			changeOrigin: true,
			rewrite: (path) => path.replace(/^\/api/, ''),  // Strip '/api' from the request path
		  },
	},
	plugins: [sveltekit()],
	test: {
		include: ['src/**/*.{test,spec}.{js,ts}']
	},
	server: {
		headers: {
			'access-control-allow-origin': '*',
			'access-control-allow-methods': 'GET, POST, PUT',
			'access-control-allow-headers': '*',
			'access-control-allow-credentials': 'true'
		}
	}
});

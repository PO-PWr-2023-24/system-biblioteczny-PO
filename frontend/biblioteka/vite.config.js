import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';

export default defineConfig({
	
	plugins: [sveltekit()],
	test: {
		include: ['src/**/*.{test,spec}.{js,ts}']
	},
	server: {
		headers: {
			'access-control-allow-origin': '*',
			'access-control-allow-methods': 'GET, POST, PUT',
			'access-control-allow-headers': '*',
			'access-control-allow-credentials': 'true',
			'access-control-request-headers': '*',
			'access-control-request-method': '*'
		},
		// proxy: {
		// 	'api/reservations':{
		// 		target: 'http://127.0.0.1:8000',
		// 		changeOrigin: true
		// 	}
		// }
	}
});

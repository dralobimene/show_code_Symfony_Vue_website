import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import fs from 'fs';

// https://vitejs.dev/config/
// ATTENTION:
// l'adresse du 1° proxy doit correspondre avec l'adresse
// de la route du controller IndexController de SF
export default defineConfig({
  plugins: [vue()],
  server : {
      https: {
        key: fs.readFileSync('./sslcert/key-no-pass.pem'),
        cert: fs.readFileSync('./sslcert/cert.pem'),
      },

      proxy: {
          /*
        "/": {
	          target: "https://127.0.0.1:8000",
	          changeOrigin: true,
	          secure: false,
	          ws:true,
	      },
          */

	      "/index": {
	          target: "https://127.0.0.1:8000",
	          changeOrigin: true,
	          secure: false,
	          ws:true,
	      },

        "/check_token": {
            target: "https://127.0.0.1:8000",
            changeOrigin: true,
            secure: false,
            ws: true,
        },

        "/connect": {
            target: "https://127.0.0.1:8000",
            changeOrigin: true,
            secure: false,
            ws: true,
        },

        // route de class
        "/secured_user": {
            target: "https://127.0.0.1:8000",
            changeOrigin: true,
            secure: false,
            ws: true,
        },

        "/logout": {
            target: "https://127.0.0.1:8000",
            changeOrigin: true,
            secure: false,
            ws: true,
        },

        // route de class
        "/comment_user": {
            target: "https://127.0.0.1:8000",
            changeOrigin: true,
            secure: false,
            ws: true,
        },

        "/reply_user_post": {
            target: "https://127.0.0.1:8000",
            changeOrigin: true,
            secure: false,
            ws: true,
        },

        "/reply_user_post_step2": {
            target: "https://127.0.0.1:8000",
            changeOrigin: true,
            secure: false,
            ws: true,
        },

        // route de classe
        // concerne les controllers suivants:
        // AdmSommaireController.php
        // DeleteCommentController.php
        // DeleteUserController.php
        // ...
        '/adm': {
            target: 'https://127.0.0.1:8000',
            changeOrigin: true,
            rewrite: (path) => path.replace(/^\/adm/, ''),
        },

        "/contact": {
	          target: "https://127.0.0.1:8000",
	          changeOrigin: true,
	          secure: false,
	          ws:true,
	      },

      },
  },
})

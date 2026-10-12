import { defineConfig } from 'astro/config';
export default defineConfig({
  site: 'https://pratikshya-regmi.github.io',
  base: '/',
  output: 'static',
  trailingSlash: 'always',
  build: { format: 'directory' }
});

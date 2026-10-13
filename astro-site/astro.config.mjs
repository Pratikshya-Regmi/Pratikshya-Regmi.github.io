import { defineConfig } from 'astro/config';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
export default defineConfig({
  site: 'https://pratikshya-regmi.github.io',
  base: '/',
  output: 'static',
  trailingSlash: 'always',
  vite: {
    // Load this CommonJS content-loader dependency through Node during Astro sync.
    plugins: [{
      name: 'picomatch-node-loader',
      enforce: 'pre',
      resolveId(id) {
        if (id === 'picomatch') {
          return '\0picomatch-node-loader';
        }
      },
      load(id) {
        if (id === '\0picomatch-node-loader') {
          return `import { createRequire } from 'node:module';
            const require = createRequire(import.meta.url);
            export default require(${JSON.stringify(require.resolve('picomatch'))});`;
        }
      }
    }]
  },
  build: { format: 'directory' }
});

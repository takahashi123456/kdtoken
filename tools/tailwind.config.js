/** @type {import('tailwindcss').Config} */
module.exports = {
  future: {
    removeDeprecatedGapUtilities: true,
    purgeLayersByDefault: true,
  },
  purge: {
    enabled: false,
    content: ['../**/templates/*.html', '../**/templates/**/*.html'],
  },
  theme: {
    extend: {},
  },
  variants: {},
  plugins: [],
}

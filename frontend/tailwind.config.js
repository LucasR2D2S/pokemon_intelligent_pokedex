/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
// This is a Tailwind CSS configuration file that specifies the content sources for class scanning and extends the default theme.
// It includes all JavaScript and TypeScript files in the `src` directory and its subdirectories.
// The `extend` section allows for customizations to the default theme, but currently, it is empty.
// The `plugins` array is also empty, indicating no additional plugins are being used.
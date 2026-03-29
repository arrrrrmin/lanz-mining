import { renderMeta } from './src/components/head.js';

// See https://observablehq.com/framework/config for documentation.
export default {
  title: 'LanzMining',
  root: 'src',
  head: renderMeta,
  theme: 'air',
  toc: true,
  // Drop gstatic links and use fontsource cdn (without tracking)
  globalStylesheets: ['/assets/global.css'],
  header: 'LanzMining',
  output: 'build',
  pager: false,
  sidebar: false,
  dynamicPaths: [
    '/components/charts.js',
    '/data/fetchLanzMining.js',
    '/assets/web-app-manifest-512x512.png',
  ],

  // footer: "Built with Observable.", // what to show in the footer (HTML)
  // search: true,
  // linkify: true, // convert URLs in Markdown to links
  // typographer: false, // smart quotes and other typographic improvements
  // preserveExtension: false, // drop .html from URLs
  // preserveIndex: false, // drop /index from URLs
};

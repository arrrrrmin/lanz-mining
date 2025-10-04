// See https://observablehq.com/framework/config for documentation.
export default {
  // The app’s title; used in the sidebar and webpage titles.
  title: "LanzMining",

  // The pages and sections in the sidebar. If you don’t specify this option,
  // all pages will be listed in alphabetical order. Listing pages explicitly
  // lets you organize them into sections and have unlisted pages.
  // pages: [
  //   {
  //     name: "Examples",
  //     pages: [
  //       {name: "Dashboard", path: "/example-dashboard"},
  //       {name: "Report", path: "/example-report"}
  //     ]
  //   }
  // ],

  root: "src",
  head: '<link rel="icon" href="assets/favicon-96x96.png" type="image/png" sizes="96x96">',
  theme: "air",
  toc: true,
  // Drop gstatic links and use fontsource cdn (without tracking)
  // style: "/assets/global.css",
  globalStylesheets: ["/assets/global.css"],
  header: "LanzMining",
  output: "dist",
  pager: false,
  sidebar: false,
  typographer: false,

  // header: "", // what to show in the header (HTML)
  // footer: "Built with Observable.", // what to show in the footer (HTML)
  // output: "dist", // path to the output root for build
  // search: true, // activate search
  // linkify: true, // convert URLs in Markdown to links
  // typographer: false, // smart quotes and other typographic improvements
  // preserveExtension: false, // drop .html from URLs
  // preserveIndex: false, // drop /index from URLs
};

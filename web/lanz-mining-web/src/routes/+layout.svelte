<script>
  let { children } = $props();
  import "../app.css";
</script>

{@render children()}

<style lang="postcss">
  @reference "tailwindcss/theme";
  :global(h2) {
    @apply max-w-2xl mx-auto pt-10 pb-6 font-bold text-3xl text-gray-800;
  }
  :global(h3) {
    @apply max-w-2xl mx-auto pt-4 font-bold text-2xl text-gray-800;
  }
  :global(p) {
    @apply max-w-2xl mx-auto py-6 text-base text-gray-800 leading-7;
  }
  :global(a) {
    @apply text-base underline text-gray-500 hover:text-gray-800;
  }
  :global(ol) {
    @apply py-8 ml-6 list-decimal;
  }
</style>

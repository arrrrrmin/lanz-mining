<script></script>

<p>
    <span>Lesebeispiel zur Grafik:</span>
    <slot></slot>
</p>

<style lang="postcss">
    @reference "tailwindcss/theme";

    span {
        @apply underline;
    }
    p {
        @apply max-w-5xl mx-auto py-4 text-sm text-gray-500 leading-5;
    }
</style>

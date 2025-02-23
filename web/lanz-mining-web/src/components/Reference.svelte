<script>
    let { srcName, srcSub, srcUrlTitle, srcUrl, srcDate } = $props();
</script>

<li>
    <a href={srcUrl} target="_blank"
        ><span>{srcName}</span>
        {#if srcSub}
         von <span>{srcSub}</span>
        {/if}
        : <span>"{srcUrlTitle}"</span>, <span>{srcDate}</span></a
    >
</li>

<style lang="postcss">
    @reference "tailwindcss/theme";
    a {
        @apply text-base underline text-gray-500 hover:text-gray-800;
    }
    li {
        @apply py-0.5;
    }
    li::marker {
        @apply text-base text-gray-800;
    }
</style>

<script>
    import requestedFeatures from "$lib/requests";
</script>

<dl class="pb-6">
    <h3 class="pt-8 pb-4 text-2xl font-bold">
        Requested features (via <a
            class="underline hover:text-stone-400"
            target="_blank"
            href="https://entropia.de/GPN23">GPN23</a
        >)
    </h3>
    {#each requestedFeatures as feature}
        <div class="flex gap-2 pb-2">
            <p>
                {#if feature.done}
                    ✔️
                {/if}
                <b>{feature.name}</b>: {feature.description}
            </p>
        </div>
    {/each}
</dl>

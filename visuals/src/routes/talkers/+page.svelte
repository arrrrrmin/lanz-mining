<script>
    import Head from "$lib/components/Head.svelte";
    import Component from "./Component.svelte";

    let { data } = $props();
</script>

<Head />
<div>
    <div class="max-w-5xl m-auto py-8">
        <a href="/" class="underline hover:text-stone-400">Home</a>
        <h1 class="font-black text-5xl">LanzMining</h1>
        <h2 class="font-semibold text-3xl">
            Top Talkende nach Auftritten und Format
        </h2>
        <Component id="v4-ia" {data}></Component>
    </div>
</div>

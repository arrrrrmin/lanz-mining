<script>
    import Head from "$lib/components/Head.svelte";
    import Versions from "$lib/components/Versions.svelte";
    import "../../app.css";

    export const prerender = true;
</script>

<div class="px-8 mx-auto sm:max-w-2xl md:max-w-7xl">
    <Head />
    <div>
        <div class="max-w-2xl m-auto py-8">
            <h1 class="font-black text-5xl">LanzMining</h1>
            <h2 class="font-semibold text-3xl">Archiv & Versionen</h2>
            <Versions />
        </div>
    </div>
</div>

<script>
    import V0 from "$lib/visualisations/V0.svelte";
    import V1 from "$lib/visualisations/V1.svelte";
    import V2 from "$lib/visualisations/V2.svelte";
    import V3 from "$lib/visualisations/V3.svelte";
    import V4 from "$lib/visualisations/V4.svelte";
    import V5 from "$lib/visualisations/V5.svelte";
    import V6 from "$lib/visualisations/V6.svelte";
    import VY from "$lib/visualisations/VY.svelte";
    import VX from "$lib/visualisations/VX.svelte";

    import TalkshowsVsSquidGame from "$lib/visualisations/TalkshowsVsSquidGame.svelte";
    import Experten from "$lib/visualisations/Experten.svelte";

    let { data } = $props();
    let formatOrder = $state({});
</script>

<div>
    <V0 {data} id={"v0"} />
    <div class="py-8"></div>

    <V1 {data} id={"v1"} bind:formatOrder />
    <div class="py-8"></div>

    <V2 {data} id={"v2"} {formatOrder} />
    <div class="py-8"></div>

    <TalkshowsVsSquidGame {data} id={"v1-1"} {formatOrder} />
    <div class="py-8"></div>

    <V3 {data} id={"v3"} n={15} {formatOrder} />
    <div class="py-8"></div>

    <V4 {data} id={"v4"} />
    <div class="py-8"></div>

    <V5 {data} id={"v5"} />
    <div class="py-8"></div>

    <V6 {data} id={"v6"} />
    <div class="py-8"></div>

    <VY {data} id={"vy"} />
    <div class="py-8"></div>

    <VX {data} id={"vx"} />
    <div class="py-8"></div>

    <Experten {data} id={"experts"} />
    <div class="py-32"></div>
</div>

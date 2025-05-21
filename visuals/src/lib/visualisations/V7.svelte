<script>
    import { onMount } from "svelte";
    import * as utils from "./utils.js";
    import * as d3 from "d3";

    let { data, id } = $props();

    const start = new Date(2024, 1, 1);
    _data = data.data.filter((d) => d.date >= start);
    _data = _data.filter((d) => d.group === "Journalismus");
    

</script>

<!-- MarketShare.svelte -->
<script>
    // Import necessary Svelte functions and D3 library
    import { onMount } from "svelte";
    import * as d3 from "d3";
    import * as utils from "./utils";

    let { data, formatOrder = $bindable(formatOrder) } = $props();

    // Fair data start for all talkshows
    const start = new Date(2024, 1, 1);
    data = data.data.filter((d) => d.date >= start);

    data = d3
        .rollups(
            data,
            (D) => ({
                episode_name: D[0].episode_name,
                len: D[0].len,
                talkshow: D[0].talkshow,
            }),
            (d) => d.episode_name,
        )
        .map((d) => d[1]);

    data = d3
        .rollups(
            data,
            (D) => D.length,
            (d) => d.talkshow,
        )
        .map((values) => ({ talkshow: values[0], size: values[1] }));

    data = data.sort((a, b) => b.size - a.size);
    let cumsums = d3.cumsum(data.map((d) => d.size));
    data = data.map((d, i) => ({
        talkshow: d.talkshow,
        start: cumsums[i] - d.size,
        end: cumsums[i],
    }));

    formatOrder = {
        markuslanz: data.findIndex((d) => d.talkshow === "markuslanz"),
        maybritillner: data.findIndex((d) => d.talkshow === "maybritillner"),
        maischberger: data.findIndex((d) => d.talkshow === "maischberger"),
        carenmiosga: data.findIndex((d) => d.talkshow === "carenmiosga"),
        hartaberfair: data.findIndex((d) => d.talkshow === "hartaberfair"),
    };

    onMount(() => {
        const width = 1200;
        const height = 150;
        const gapSize = 10;
        const margins = { bottom: 40 };
        const barHeight = 100;
        const animDelay = 75;

        var x = d3
            .scaleLinear()
            .range([0, width])
            .domain([0, d3.sum(data, (d) => d.end - d.start)]);

        var y = d3.scaleBand().range([40, height]).domain([0]);

        const svg = d3
            .select("#talkshow-market-share")
            .append("svg")
            .attr("viewBox", [0, 0, width, height])
            .attr("color", "#E8E0D3")
            .attr("style", `max-width: ${width}px; overflow: visible;`);

        const update = () => {
            var bar = svg
                .append("g")
                .attr("id", "market-share-g")
                .selectAll("rect")
                .data(data)
                .join("rect")
                .attr("id", (d) => `market-share-${d.talkshow}`)
                .transition()
                .delay((_, i) => i * animDelay)
                .attr("x", (d) => x(d.start))
                .attr("y", y(0))
                .attr("fill-opacity", 0)
                .attr("rx", 8)
                .attr("stroke", (d) => utils.showKeyToColour[d.talkshow])
                .attr("stroke-width", 2)
                .attr("width", (d, i) => x(d.end - d.start) - gapSize)
                .attr("height", y.bandwidth());

            var barNames = svg
                .append("g")
                .attr("id", "market-share-names-g")
                .selectAll("text")
                .data(data)
                .join("text")
                .transition()
                .delay((_, i) => i * animDelay)
                .attr("x", (d) => x(d.start) + gapSize)
                .attr("y", y(0) + y.bandwidth() - gapSize)
                .attr("text-anchor", "start")
                .text((d) => utils.mapShowNames[d.talkshow]);

            var barValues = svg
                .append("g")
                .attr("id", "market-share-values-g")
                .selectAll("text")
                .data(data)
                .join("text")
                .transition()
                .delay((_, i) => i * animDelay)
                .attr("x", (d) => x(d.start) + gapSize)
                .attr("y", y(0) + gapSize * 2)
                .attr("text-anchor", "start")
                .text((d) => `${d.end - d.start}`);

            var title = svg
                .append("g")
                .attr("id", "market-share-title-g")
                .append("text")
                .attr("id", "market-share-title-text")
                .attr("x", width / 2)
                .attr("y", 20)
                .attr("font-size", 24)
                .attr("font-weight", 600)
                .attr("text-anchor", "middle")
                .text("Gesendete Talkshow-Sendungen im ÖRR in 2024");
        };
        update();
    });
</script>

<!-- Container for the chart -->
<div id="talkshow-market-share" class="pt-8"></div>

<style></style>

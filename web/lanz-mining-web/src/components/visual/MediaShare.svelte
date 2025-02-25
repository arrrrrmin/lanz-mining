<!-- MediaShare.svelte -->
<script>
    // Import necessary Svelte functions and D3 library
    import { onMount } from "svelte";
    import * as utils from "./utils.js";
    import * as d3 from "d3";

    const pairwiseCumsumPercentage = (_d, denom) => {
        var values = d3.pairs([
            0,
            ...d3.cumsum(_d.children, (d) => (d.value / denom) * 100),
        ]);
        return _d.children.map((d, i) => ({
            ...d,
            start: values[i][0],
            end: values[i][1],
            percentage: values[i][1] - values[i][0],
            talkshow: _d.talkshow,
        }));
    };

    // Get props
    let { data, formatOrder } = $props();

    const start = new Date(2024, 1, 1);
    data = data.data.filter((d) => d.date >= start);
    data = data.filter((d) => d.group === "Journalismus");

    data = d3
        .groups(data, (d) => d.talkshow)
        .map((D) => ({
            talkshow: D[0],
            children: d3
                .groups(D[1], (e) => e.media)
                .map((E) => ({
                    media: E[0],
                    value: E[1].length,
                }))
                .sort((a, b) => b.value - a.value),
            count: D[1].length,
        }));

    data = data.sort(
        (a, b) => formatOrder[a.talkshow] - formatOrder[b.talkshow],
    );
    data = data.map((d) => ({
        ...d,
        children: pairwiseCumsumPercentage(d, d.count).map((d) => ({
            media: d.media,
            start: d.start,
            end: d.end,
            percentage: d.percentage,
            talkshow: d.talkshow,
        })),
    }));

    onMount(() => {
        const width = 1200;
        const height = 600;
        const gapSize = 4;
        const animDelay = 50;

        var svg = d3
            .select("#talkshow-media-share")
            .append("svg")
            .attr("viewBox", [0, 0, width, height])
            .attr("style", `max-width: ${width}px; overflow: visible;`);

        var x = d3.scaleLinear().range([0, width]).domain([0, 100]);
        var y = d3
            .scaleBand()
            .range([70, height])
            .padding(0.35)
            .paddingOuter(0)
            .domain(data.map((d) => d.talkshow));

        const percentageLabel = (d) => {
            if (d.end - d.start < 3) {
                return "";
            }
            return `${Math.round(d.end - d.start)}`;
        };

        const mediaLabel = (d) => {
            if (d.media === "") {
                d.media = "Ohne Angaben";
            }
            if (d.end - d.start < 3) {
                return "";
            }
            let w = x(d.end - d.start) - gapSize;
            let nUpperCase = (d.media.match(/[A-Z]/g) || []).length;
            let nLowerCase = (d.media.match(/[a-z]/g) || []).length;
            let labelWidth = nUpperCase * 10 + nLowerCase * 6;
            if (w - labelWidth < 30) {
                let nChars = Math.floor(w / 10);
                let label = d.media.slice(0, nChars - 1);
                if (label !== d.media) {
                    label = label + "...";
                }
                return label;
            }
            return d.media;
        };

        const update = () => {
            var bar = svg
                .selectAll("g")
                .data(data)
                .join("g")
                .attr("id", (d) => `media-share-g-${d.talkshow}`)
                .selectAll("rect")
                .data((d) => d.children)
                .join("rect")
                .attr("id", (d) => `media-share-rect-${d.media}`)
                .transition()
                .delay((_, i) => i * animDelay)
                .attr("x", (d) => x(d.start))
                .attr("y", (d) => y(d.talkshow))
                .attr("rx", 8)
                .attr("fill-opacity", 0)
                .attr("stroke", (d) => utils.showKeyToColour[d.talkshow])
                .attr("stroke-width", 2)
                .attr("width", (d, i) => x(d.end - d.start) - gapSize)
                .attr("height", y.bandwidth());

            var barValues = svg
                .selectAll("g#media-share-values")
                .data(data)
                .join("g")
                .attr("id", (d) => `media-share-values-g-${d.talkshow}`)
                .selectAll("text#media-share-values-text")
                .data((d) => d.children)
                .join("text")
                .attr("id", (d) => `media-share-values-text-${d.media}`)
                .transition()
                .delay((_, i) => i * animDelay)
                .attr("x", (d) => x(d.start) + gapSize)
                .attr("y", (d) => y(d.talkshow) + gapSize * 4)
                .attr("fill", "black")
                .attr("text-anchor", "start")
                .text((d) => percentageLabel(d));

            var barLabels = svg
                .selectAll("g#media-share-labels")
                .data(data)
                .join("g")
                .attr("id", (d) => `media-share-labels-g-${d.talkshow}`)
                .selectAll("text#media-share-labels-text")
                .data((d) => d.children)
                .join("text")
                .attr("id", (d) => `media-share-labels-text-${d.media}`)
                .transition()
                .delay((_, i) => i * animDelay)
                .attr("x", (d) => x(d.start) + gapSize / 2)
                .attr("y", (d) => y(d.talkshow) + y.bandwidth() - gapSize)
                .attr("fill", "black")
                .attr("text-anchor", "start")
                .text((d) => mediaLabel(d));

            var showTitles = svg
                .append("g")
                .attr("id", "media-share-showlabels-g")
                .selectAll("text")
                .data(data)
                .join("text")
                .attr("id", (d) => `media-share-showlabels-g-${d.talkshow}`)
                .attr("x", (d) => x(50))
                .attr("y", (d) => y(d.talkshow) - gapSize * 2)
                .attr("font-weight", 600)
                .attr("text-anchor", "middle")
                .text((d) => utils.mapShowNames[d.talkshow]);

            var title = svg
                .append("g")
                .attr("id", "media-share-title-g")
                .append("text")
                .attr("id", "media-share-title-text")
                .attr("x", width / 2)
                .attr("y", 20)
                .attr("font-size", 24)
                .attr("font-weight", 600)
                .attr("text-anchor", "middle")
                .text("Medienunternehmen nach Talkshow-Formaten in 2024 (%)");
        };
        update();
    });
</script>

<!-- Container for the chart -->
<div id="talkshow-media-share" class="pt-8"></div>

<style></style>

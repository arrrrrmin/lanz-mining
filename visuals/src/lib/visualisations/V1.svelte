<script>
    import { onMount } from "svelte";
    import * as d3 from "d3";
    import * as utils from "./utils";

    let { data, id, formatOrder = $bindable(formatOrder) } = $props();
    let _data = utils.uniformStart(data.data);

    _data = d3
        .rollups(
            _data,
            (D) => ({
                episode_name: D[0].episode_name,
                len: D[0].len,
                talkshow: D[0].talkshow,
            }),
            (d) => d.episode_name,
        )
        .map((d) => d[1]);

    _data = d3
        .rollups(
            _data,
            (D) => D.length,
            (d) => d.talkshow,
        )
        .map((values) => ({ talkshow: values[0], size: values[1] }));

    _data = _data.sort((a, b) => b.size - a.size);
    let cumsums = d3.cumsum(_data.map((d) => d.size));
    _data = _data.map((d, i) => ({
        talkshow: d.talkshow,
        start: cumsums[i] - d.size,
        end: cumsums[i],
    }));

    formatOrder = {
        markuslanz: _data.findIndex((d) => d.talkshow === "markuslanz"),
        maybritillner: _data.findIndex((d) => d.talkshow === "maybritillner"),
        maischberger: _data.findIndex((d) => d.talkshow === "maischberger"),
        carenmiosga: _data.findIndex((d) => d.talkshow === "carenmiosga"),
        hartaberfair: _data.findIndex((d) => d.talkshow === "hartaberfair"),
    };

    onMount(() => {
        const width = 1600;
        const height = 175;
        const gapSize = 10;
        const margins = { bottom: 20 };
        const barHeight = 100;
        const animDelay = 75;

        var x = d3
            .scaleLinear()
            .range([1, width])
            .domain([0, d3.sum(_data, (d) => d.end - d.start)]);

        var y = d3
            .scaleBand()
            .range([40, height - margins.bottom])
            .domain([0]);

        const svg = utils.createSvg(id, width, height, "visible");

        const update = () => {
            var bar = svg
                .append("g")
                .attr("id", "ds-share-g")
                .selectAll("rect")
                .data(_data)
                .join("rect")
                .attr("id", (d) => `market-share-${d.talkshow}`)
                .attr("x", (d) => x(d.start))
                .attr("y", y(0))
                .attr("fill", (d) => utils.showKeyToColour[d.talkshow])
                .attr("rx", 8)
                .attr("stroke-width", 3)
                .attr("width", (d, i) => x(d.end - d.start) - gapSize)
                .attr("height", y.bandwidth());

            var barNames = svg
                .append("g")
                .attr("id", "market-share-names-g")
                .selectAll("text")
                .data(_data)
                .join("text")
                .attr("x", (d) => x(d.start) + gapSize / 2)
                .attr("y", y(0) - gapSize)
                .text((d) => `${utils.mapShowNames[d.talkshow]}`);

            var barValues = svg
                .append("g")
                .attr("id", "market-share-values-g")
                .selectAll("text")
                .data(_data)
                .join("text")
                .attr("fill", "white")
                .attr("x", (d) => x(d.start) + gapSize / 2)
                .attr("y", y(0) + y.bandwidth() - gapSize)
                .text((d) => `${d.end - d.start}`);

            utils.setText(barNames, 24, 500, "start");
            utils.setText(barValues, 24, 600, "start");
        };
        update();
    });
</script>

<div {id}></div>

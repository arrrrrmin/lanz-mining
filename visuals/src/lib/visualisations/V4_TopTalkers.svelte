<script>
    import { onMount } from "svelte";
    import * as utils from "./utils.js";
    import * as d3 from "d3";

    // Get props
    let { data, id, n, formatOrder } = $props();

    // Fair data start for all talkshows
    let start = utils.dateContext.full;

    const transformData = (originalData) => {
        let _data = originalData.filter((d) => d.date >= start);

        _data = d3
            .groups(_data, (d) => d.name)
            .map((d) => ({
                name: d[0],
                invites: d3
                    .groups(d[1], (d) => d.talkshow)
                    .map((d) => ({ talkshow: d[0], values: d[1] })),
            }));
        _data = _data.map((d) => ({
            name: d.name,
            invites: d.invites,
            total_invites: d3.sum(d.invites, (D) => D.values.length),
        }));

        // Sort befor cumulative sum!
        _data = _data
            .map((d) => ({
                ...d,
                invites: d.invites
                    .sort(
                        (a, b) =>
                            formatOrder[a.talkshow] - formatOrder[b.talkshow],
                    )
                    .sort((a, b) => b.values.length - a.values.length),
            }))
            .sort((a, b) => b.total_invites - a.total_invites);
        _data = _data.map((d) => ({
            ...d,
            invites: utils.pairwiseCumsum(d.invites),
        }));
        
        _data = _data.slice(0, n);
        return _data;
    };

    let _data = transformData(data.data);

    onMount(() => {
        const width = 1600;
        const height = n * 60;
        const gapSize = 6;
        const animDelay = 350;

        var x = d3
            .scaleLinear()
            .range([1, width])
            .domain([0, d3.max(_data, (d) => d.total_invites)]);

        var y = d3
            .scaleBand()
            .range([1, height])
            .padding(0.175)
            .paddingOuter(0.02)
            .domain(_data.map((d) => d.name));

        const svg = utils.createSvg(id, width, height, "visible");

        var legendRects = svg
            .append("g")
            .attr("id", "main-speakers-legend-g")
            .selectAll("rect")
            .data(Object.keys(utils.showKeyToColour))
            .join("rect")
            .attr("x", (d, i) => width - y.bandwidth())
            .attr("y", (d, i) => y(_data[_data.length - 1 - i].name))
            .attr("rx", 4)
            .attr("width", y.bandwidth())
            .attr("height", y.bandwidth())
            .attr("fill", (d) => utils.showKeyToColour[d]);

        var legendTexts = svg
            .select("g#main-speakers-legend-g")
            .selectAll("text")
            .data(Object.keys(utils.mapShowNames))
            .join("text")
            .attr("x", (d, i) => width - y.bandwidth() - gapSize)
            .attr(
                "y",
                (d, i) =>
                    y(_data[_data.length - 1 - i].name) + y.bandwidth() / 2 + 5,
            )
            .text((d) => utils.mapShowNames[d]);

        utils.setText(legendTexts, 22, 500, "end");

        x.domain([0, d3.max(_data, (d) => d.total_invites)]);
        y.domain(_data.map((d) => d.name));

        var barGroups = svg
            .selectAll("g#main-speakers-bars-g")
            .data(_data)
            .join("g")
            .attr("id", "main-speakers-bars-g")
            .attr("transform", (d) => `translate(0,${y(d.name)})`);
        var nameGroups = svg.append("g").attr("id", "main-speakers-names-g");

        var bars = barGroups
            .selectAll("rect#main-speakers-rect")
            .data((d) => d.invites)
            .join("rect") // per bar in series
            .attr("id", "main-speakers-rect")
            .transition()
            .delay((_, i) => i * animDelay)
            .attr("x", (d) => x(d.start))
            .attr("y", 0)
            .attr("fill", (d) => utils.showKeyToColour[d.talkshow])
            .attr("rx", 4)
            .attr("width", (d) => x(d.end - d.start) - gapSize)
            .attr("height", y.bandwidth());

        var nameLabels = nameGroups
            .selectAll("text#main-speakers-names-g-text")
            .data(_data)
            .join("text")
            .attr("x", (d) => x(d.invites[0].start) + gapSize * 1.75)
            .attr("y", (d) => y(d.name) + y.bandwidth() / 2 + 5)
            .text((d) => d.name);

        utils.setText(nameLabels, 22, 500, "start");

        var barValues = barGroups
            .selectAll("text#main-speakers-values-text")
            .data((d) => d.invites)
            .join("text")
            .attr("x", (d) => x(d.end) - gapSize * 2)
            .attr("y", y.bandwidth() / 2 + 5)
            .text((d) => `${d.end - d.start}`);

        utils.setText(barValues, 22, 500, "end");
    });
</script>

<div {id}></div>

<style></style>

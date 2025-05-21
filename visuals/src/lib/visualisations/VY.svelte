<script>
    import { onMount } from "svelte";
    import * as utils from "./utils.js";
    import * as d3 from "d3";

    /** Helper functions */
    export const pairwiseCumsumPercentage = (_d, denom) => {
        var values = d3.pairs([
            0,
            ...d3.cumsum(_d, (d) => (d.values.length / denom) * 100),
        ]);
        return _d.map((d, i) => ({
            ...d,
            start: values[i][0],
            end: values[i][1],
            percentage: values[i][1] - values[i][0],
        }));
    };

    /** Passed data and id */
    let { data, id } = $props();

    let start = utils.dateContext.full;
    let end = new Date(2025, 1, 23);

    const transformData = (originalData, s, e) => {
        let _data = originalData.filter((d) => d.date >= s);
        if (e) {
            _data = _data.filter((d) => d.date < e);
        }
        _data = _data.filter((d) => d.group == "Politik");
        _data = _data.map((d) => ({
            ...d,
            party: utils.normalizeParties(d.party),
        }));
        _data = d3
            .groups(_data, (d) => d.party)
            .map((D) => ({ party: D[0], values: D[1] }))
            .sort((a, b) => b.values.length - a.values.length);

        _data = pairwiseCumsumPercentage(
            _data,
            d3.sum(_data, (d) => d.values.length),
        );

        return _data;
    };

    let _fulldata = transformData(data.data, start, undefined);
    let _btwdata = transformData(
        data.data,
        new Date(2024, 10, 6),
        new Date(2025, 1, 23),
    );

    onMount(() => {
        const width = 1600;
        const barvals = { height: 125, gap: 50 };
        const height = barvals.height * 2 + barvals.gap * 2 + 1;
        const gapSize = 4;

        const svg = utils.createSvg(id, width, height, "visible");
        var x = d3.scaleLinear().range([0, width]).domain([0, 100]);

        var g1 = svg
            .append("g")
            .attr("id", `${id}-g1`)
            .attr("transform", `translate(0,0)`);

        var bars1 = g1
            .selectAll(`rect#${id}-g1-r`)
            .data(_fulldata)
            .join("rect")
            .attr("id", `${id}-g1-r`)
            .attr("x", (d) => x(d.start))
            .attr("width", (d) => x(d.end - d.start) - gapSize)
            .attr("y", barvals.gap)
            .attr("height", barvals.height)
            .attr("rx", 8)
            .attr("fill", (d) => utils.partyToColour[d.party])
            .attr("fill-opacity", 0.9)
            .attr("stroke", (d) => utils.partyToColour[d.party])
            .attr("stroke-opacity", 0.9);

        var title1 = g1
            .append("text")
            .attr("id", `${id}-g1-t`)
            .attr("x", width / 2)
            .attr("y", 40)
            .text("Verteilung aller Daten");

        utils.setText(title1, 22, 600, "middle");

        var barpercs1 = g1
            .selectAll(`text#${id}-g1-rt1`)
            .data(_fulldata)
            .join("text")
            .attr("id", `text#${id}-g1-rt1`)
            .attr("y", (d) => barvals.gap + 20)
            .attr("x", (d) => x(d.start) + gapSize)
            //.attr("fill", (d) => utils.partyToInnerColor[d.party])
            .attr("fill", "white")
            .text((d) =>
                d.percentage > 1.5 ? `${Math.round(d.percentage, 2)}%` : "",
            );

        utils.setText(barpercs1, 18, 600, "start");

        var barlabels1 = g1
            .selectAll(`text#${id}-g1-rt2`)
            .data(_fulldata)
            .join("text")
            .attr("id", `text#${id}-g1-rt2`)
            .attr("y", (d) => barvals.gap + barvals.height - 10)
            .attr("x", (d) => x(d.start) + gapSize)
            .attr("fill", "white")
            .text((d) => (d.percentage <= 1.5 ? "" : d.party == "Parteilos" ? "-": d.party));

        utils.setText(barlabels1, 18, 600, "start");

        var g2 = svg
            .append("g")
            .attr("id", `${id}-g2`)
            .attr("transform", `translate(0,${barvals.height + barvals.gap})`);

        var bars2 = g2
            .selectAll(`rect#${id}-g2-r`)
            .data(_btwdata)
            .join("rect")
            .attr("id", `${id}-g2-r`)
            .attr("x", (d) => x(d.start))
            .attr("width", (d) => x(d.end - d.start) - gapSize)
            .attr("y", barvals.gap)
            .attr("height", barvals.height)
            .attr("rx", 8)
            .attr("fill", (d) => utils.partyToColour[d.party])
            .attr("fill-opacity", 0.9)
            .attr("stroke", (d) => utils.partyToColour[d.party])
            .attr("stroke-opacity", 0.9);

        var title2 = g2
            .append("text")
            .attr("id", `${id}-g2-t`)
            .attr("x", width / 2)
            .attr("y", 40)
            .text("Im Zeitraum der Bundestagswahl");

        utils.setText(title2, 22, 600, "middle");

        var barpercs2 = g2
            .selectAll(`text#${id}-g2-rt2`)
            .data(_btwdata)
            .join("text")
            .attr("id", `text#${id}-g2-rt2`)
            .attr("y", (d) => barvals.gap + 20)
            .attr("x", (d) => x(d.start) + gapSize)
            .attr("fill", "white")
            .text((d) =>
                d.percentage > 1.5 ? `${Math.round(d.percentage, 2)}%` : "",
            );

        utils.setText(barpercs2, 20, 600, "start");

        var barlabels2 = g2
            .selectAll(`text#${id}-g2-rt2`)
            .data(_btwdata)
            .join("text")
            .attr("id", `text#${id}-g2-rt2`)
            .attr("y", (d) => barvals.gap + barvals.height - 10)
            .attr("x", (d) => x(d.start) + gapSize)
            .attr("fill", "white")
            .text((d) => (d.percentage <= 1.5 ? "" : d.party == "Parteilos" ? "-": d.party));

        utils.setText(barlabels2, 20, 600, "start");
    });
</script>

<div {id}></div>

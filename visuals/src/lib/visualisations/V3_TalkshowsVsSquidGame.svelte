<script>
    import { onMount } from "svelte";
    import * as d3 from "d3";
    import * as utils from "./utils";

    const pairwiseCumsum = (_d) => {
        var values = d3.pairs([0, ...d3.cumsum(_d, (d) => d.len)]);
        return _d.map((d, i) => ({
            ...d,
            start: values[i][0],
            end: values[i][1],
        }));
    };

    let { data, id, formatOrder = $bindable(formatOrder) } = $props();
    let _data = utils.uniformStart(data.data);
    _data = _data.map((d) => ({
        ...d,
        ym: new Date(d.date.getFullYear(), d.date.getMonth(), 1),
    }));

    _data = d3
        .groups(_data, (d) => d.ym)
        .map((D) => ({
            ym: D[0],
            children: d3
                .rollups(
                    D[1],
                    (E) =>
                        d3.rollups(
                            E,
                            (F) => F[0].len,
                            (f) => f.episode_name,
                        ),
                    (e) => e.talkshow,
                )
                .map((f) => ({
                    talkshow: f[0],
                    children: f[1].map((F) => ({
                        episode_name: F[0],
                        len: F[1],
                    })),
                    episodes: f[1].length,
                })),
        }));

    _data = _data.map((d) => ({
        ...d,
        children: d.children
            .map((D) => ({
                ...D,
                len: d3.sum(D.children, (e) => e.len),
            }))
            .sort((a, b) => formatOrder[a.talkshow] - formatOrder[b.talkshow]),
    }));
    _data = _data.map((d) => ({
        ...d,
        children: pairwiseCumsum(d.children),
    }));

    _data = _data.sort((a, b) => a.ym - b.ym);

    let avrgMonthData = [];
    Object.entries(formatOrder).forEach(([talkshow, index], i) => {
        let name = _data[0].children[i].talkshow;
        avrgMonthData.push({
            talkshow: name,
            len:
                d3.sum(
                    _data.filter((d) => d.children.length == 5),
                    (d) => d.children[i].len,
                ) / _data.filter((d) => d.children.length == 5).length,
        });
    });
    avrgMonthData = pairwiseCumsum(avrgMonthData);
    let squidGame1 = [60, 63, 55, 56, 52, 62, 59, 33, 56];
    let otherData = [
        { name: "Squid Game (S1)", len: d3.sum(squidGame1) },
        { name: "Squid Game (S1)", len: d3.sum(squidGame1) },
        { name: "Squid Game (S1)", len: d3.sum(squidGame1) },
        { name: "Squid Game (S1, 1-6)", len: d3.sum(squidGame1.splice(0, 6)) },
    ];
    otherData = pairwiseCumsum(otherData);
    
    onMount(() => {
        const width = 400;
        const height = 600;
        const gapSize = 8;

        const svg = utils.createSvg(id, width, height, "visible");

        var x = d3
            .scaleBand()
            .range([0, width])
            .domain(["Talkshows", "OtherData"])
            .padding(0.2)
            .paddingOuter(0);

        var y = d3
            .scaleLinear()
            .range([height, 10])
            .domain([0, d3.max(avrgMonthData, (d) => d.end)]);

        var g1 = svg.append("g").attr("id", "g1");
        var g2 = svg.append("g").attr("id", "g2");

        var g1bars = g1
            .selectAll("rect")
            .data(avrgMonthData)
            .join("rect")
            .attr("id", "g1-r")
            .attr("x", x("Talkshows"))
            .attr("y", (d) => y(d.end))
            .attr("width", x.bandwidth())
            .attr("height", (d) => y(d.start) - y(d.end) - gapSize)
            .attr("fill", (d) =>
                d.talkshow in utils.showKeyToColour
                    ? utils.showKeyToColour[d.talkshow]
                    : "gray",
            )
            .attr("stroke-width", 3)
            .attr("rx", 8);

        var g1bars = g2
            .selectAll("rect")
            .data(otherData)
            .join("rect")
            .attr("id", "g2-r")
            .attr("x", x("OtherData"))
            .attr("y", (d) => y(d.end))
            .attr("width", x.bandwidth())
            .attr("height", (d) => y(d.start) - y(d.end) - gapSize)
            .attr("fill", "#c70036")
            .attr("stroke-width", 3)
            .attr("rx", 8);

        var bar1labels = g1
            .selectAll("text")
            .data(avrgMonthData)
            .join("text")
            .attr("x", x("Talkshows") + gapSize / 2)
            .attr("y", (d) => y(d.end) + gapSize * 2.5)
            .attr("fill", "white")
            .text((d) => Math.round(d.len));

        var bar2labels = g2
            .selectAll("text")
            .data(otherData)
            .join("text")
            .attr("x", x("OtherData") + gapSize / 2)
            .attr("y", (d) => y(d.end) + gapSize * 2.5)
            .attr("fill", "white")
            .text((d) => (d.len == 496 ? `${d.len}` : `${d.len} (E 1-6)`));

        utils.setText(bar1labels, 22, 600, "start");
        utils.setText(bar2labels, 22, 600, "start");
    });
</script>

<div {id} class="max-w-2xl m-auto"></div>

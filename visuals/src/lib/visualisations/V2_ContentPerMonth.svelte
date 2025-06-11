<script>
    import { onMount } from "svelte";
    import * as utils from "./utils.js";
    import * as d3 from "d3";

    import { timeFormatDeLocale } from "./formatting.js";

    const pairwiseCumsum = (_d) => {
        var values = d3.pairs([0, ...d3.cumsum(_d, (d) => d.len)]);
        return _d.map((d, i) => ({
            ...d,
            start: values[i][0],
            end: values[i][1],
        }));
    };

    let { data, id, formatOrder } = $props();

    // Fair data start for all talkshows
    let _data = utils.uniformStart(data.data.filter((d) => !isNaN(d.len)));
    const sonderformate = [
        {
            index: data.length,
            episode_name:
                "klartext - Das ZDF-Wahlforum mit den Kanzlerkandidaten",
            date: new Date(2025, 1, 13),
            factcheck: true,
            len: 141,
            name: "Olaf Scholz, Friedrich Merz, Robert Habeck, Alice Weidel",
            talkshow: "Sonderformat",
            party: null,
            group: null,
            media: null,
        },
        {
            index: data.length + 1,
            episode_name: "Hart aber fair 360 mit Tino Chrupalla",
            date: new Date(2025, 1, 16),
            factcheck: true,
            len: 45,
            name: "Tino Chrupalla",
            talkshow: "Sonderformat",
            party: "AfD",
            group: "Politik",
            media: null,
        },
        {
            index: data.length + 2,
            episode_name: "Hart aber fair 360 mit Robert Habeck",
            date: new Date(2025, 1, 16),
            factcheck: true,
            len: 43,
            name: "Robert Habeck",
            talkshow: "Sonderformat",
            party: "B90G",
            group: "Politik",
            media: null,
        },
    ];
    // sonderformate.forEach((d) => data.push(d));
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

    onMount(() => {
        const width = 1600;
        const height = 700;
        const gapSize = 8;
        const animDelay = 50;

        const svg = utils.createSvg(id, width, height, "visible");

        var x = d3
            .scaleBand()
            .range([0, width])
            .domain(_data.map((d) => d.ym))
            .padding(0.2)
            .paddingOuter(0);

        var y = d3
            .scaleLinear()
            .range([height - 30, 70])
            .domain([
                0,
                d3.max(_data, (d) => d3.max(d.children, (D) => D.end)),
            ]);

        const update = () => {
            var bar = svg
                .selectAll("g#over-time-g")
                .data(_data)
                .join("g")
                .attr("id", "over-time-g")
                .attr("transform", (d) => `translate(${x(d.ym)}, 0)`)
                .selectAll("rect")
                .data((d) => d.children)
                .join("rect")
                .attr("id", (d) => `over-time-${d.talkshow}`)
                .transition()
                .delay((_, i) => i * animDelay)
                .attr("x", (d) => 0)
                .attr("y", (d) => y(d.end))
                .attr("width", x.bandwidth())
                .attr("height", (d) => y(d.start) - y(d.end) - gapSize)
                .attr("fill", (d) =>
                    d.talkshow in utils.showKeyToColour
                        ? utils.showKeyToColour[d.talkshow]
                        : "gray",
                )
                .attr("stroke", (d) =>
                    d.talkshow in utils.showKeyToColour
                        ? utils.showKeyToColour[d.talkshow]
                        : "gray",
                )
                .attr("stroke-width", 3)
                .attr("rx", 8);

            var barLabels = svg
                .selectAll("text#over-time-bar-labels-text")
                .data(_data)
                .join("text")
                .attr("id", "over-time-bar-labels-text")
                .attr("x", (d) => x(d.ym) + x.bandwidth() / 2)
                .attr(
                    "y",
                    (d) => y(d.children[d.children.length - 1].end) - gapSize,
                )
                .attr("text-anchor", "middle")
                .text((d) => d.children[d.children.length - 1].end);

            utils.setText(barLabels, 22, 500, "middle");

            var xlabels = svg.append("g").attr("id", "over-time-g-xlabels");

            xlabels
                .selectAll("g#over-time-g-xlabels")
                .data(_data)
                .join("text")
                .attr("x", (d) => x(d.ym) + x.bandwidth() / 2)
                .attr("y", (d) => y(0) + 2 * gapSize)
                .text((d) => timeFormatDeLocale.format("%b %y")(d.ym));
            utils.setText(xlabels, 22, 500, "middle");
        };

        update();
    });
</script>

<div {id}></div>

<style></style>

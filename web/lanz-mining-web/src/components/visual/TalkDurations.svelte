<!-- TalkDurations.svelte -->
<script>
    // Import necessary Svelte functions and D3 library
    import { onMount } from "svelte";
    import * as utils from "./utils.js";
    import * as d3 from "d3";

    const pairwiseCumsum = (_d) => {
        var values = d3.pairs([0, ...d3.cumsum(_d, (d) => d.len)]);
        return _d.map((d, i) => ({
            ...d,
            start: values[i][0],
            end: values[i][1],
        }));
    };

    let { data, formatOrder } = $props();

    // Fair data start for all talkshows
    const start = new Date(2024, 1, 1);
    data = data.data.filter((d) => d.date >= start);
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
    sonderformate.forEach((d) => data.push(d));
    data = data.map((d) => ({
        ...d,
        ym: new Date(d.date.getFullYear(), d.date.getMonth(), 1),
    }));

    data = d3
        .groups(data, (d) => d.ym)
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

    data = data.map((d) => ({
        ...d,
        children: d.children
            .map((D) => ({
                ...D,
                len: d3.sum(D.children, (e) => e.len),
            }))
            .sort((a, b) => formatOrder[a.talkshow] - formatOrder[b.talkshow]),
    }));
    data = data.map((d) => ({
        ...d,
        children: pairwiseCumsum(d.children),
    }));

    data = data.sort((a, b) => a.ym - b.ym);

    onMount(() => {
        const width = 1200;
        const height = 700;
        const gapSize = 8;
        const animDelay = 50;

        var svg = d3
            .select("#talkshow-over-time")
            .append("svg")
            .attr("viewBox", [0, 0, width, height])
            .attr("style", `max-width: ${width}px; overflow: visible;`);

        var x = d3
            .scaleBand()
            .range([0, width])
            .domain(data.map((d) => d.ym))
            .padding(0.2)
            .paddingOuter(0);

        var y = d3
            .scaleLinear()
            .range([height - 30, 70])
            .domain([0, d3.max(data, (d) => d3.max(d.children, (D) => D.end))]);

        const update = () => {
            var bar = svg
                .selectAll("g#over-time-g")
                .data(data)
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
                .attr("fill-opacity", 0)
                .attr("stroke", (d) =>
                    d.talkshow in utils.showKeyToColour
                        ? utils.showKeyToColour[d.talkshow]
                        : "gray",
                )
                .attr("stroke-width", 2)
                .attr("rx", 8);

            var barLabels = svg
                .selectAll("text#over-time-bar-labels-text")
                .data(data)
                .join("text")
                .attr("id", "over-time-bar-labels-text")
                .attr("x", (d) => x(d.ym) + x.bandwidth() / 2)
                .attr(
                    "y",
                    (d) => y(d.children[d.children.length - 1].end) - gapSize,
                )
                .attr("text-anchor", "middle")
                .text((d) => d.children[d.children.length - 1].end);

            var xlabels = svg.append("g").attr("id", "over-time-g-xlabels");

            xlabels
                .selectAll("g#over-time-g-xlabels")
                .data(data)
                .join("text")
                .attr("x", (d) => x(d.ym))
                .attr("y", (d) => y(0) + 2 * gapSize)
                .text(
                    (d) =>
                        `${d.ym.toLocaleString("default", { month: "short" })}. ${d.ym.getFullYear()}`,
                );

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
                .text("Talkdauer pro Monat und Format (in Min.)");
        };

        update();
    });
</script>

<div id="talkshow-over-time" class="pt-8"></div>

<style></style>

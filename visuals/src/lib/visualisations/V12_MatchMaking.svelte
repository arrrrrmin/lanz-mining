<script>
    import { onMount } from "svelte";
    import * as utils from "./utils.js";
    import * as d3 from "d3";

    let { data, id } = $props();

    let _data = data.data.filter((d) => d.date > utils.dateContext.full);
    // let _data = data.data.filter((d) => d.date > utils.dateContext.btw && d.date <= new Date(2025, 1, 23));

    const parties = new Array(...new Set(_data.map((d) => d.party)))
        .filter((d) => d !== "")
        .sort((a, b) => a.localeCompare(b));

    const findMatches = (data, party) => {
        const numEpisodesWithPol = data.filter(
            (d) => d.children.filter((D) => D.party != "").length > 0,
        ).length;
        const numPoliticalAppears = d3.sum(
            data.map((d) => d.children.filter((D) => D.party).length),
        );
        console.log(numEpisodesWithPol);
        let partyEpisodes = data
            .filter(
                (d) => d.children.filter((D) => D.party === party).length > 0,
            )
            .map((d) => ({
                ...d,
                children: d.children.map(({ name, party, group, media }) => ({
                    name,
                    party,
                    group,
                    media,
                })),
            }));
        // Number of all the politicians in every episode
        // const numPoliticians = d3.sum(
        //     partyEpisodes,
        //     (d) => d.children.filter((D) => D.party !== "").length,
        // );
        // Number of episodes (a single person of this party is in every episode)
        const nSelf = partyEpisodes.length;

        const sequence = parties.map((_party) => {
            let n = partyEpisodes.filter(
                (d) => d.children.filter((D) => D.party === _party).length,
            ).length;
            if (_party === party) {
                n -= nSelf;
            }

            return { party: _party, n: n }; // numEpisodesWithPol // (numPoliticians - nSelf)
        });
        return { source: party, sequence: sequence };
    };

    const transformData = (originalData) => {
        let _data = d3
            .groups(originalData, (d) => d.episode_name)
            .map((D) => ({ name: D[0], children: D[1] }));
        const matrix = parties.map((party, i) => findMatches(_data, party));
        return matrix;
    };

    const matrix = transformData(_data);

    onMount(() => {
        const width = 800;
        const height = 800;
        const margins = { left: 150, top: 100, right: 10, bottom: 10 };

        const x = d3
            .scaleBand()
            .range([margins.left, width - margins.right])
            .domain(parties);
        const y = d3
            .scaleBand()
            .range([margins.top, height - margins.bottom])
            .domain(parties);
        const c = d3.scaleSequential([0, 50], d3.interpolateRdPu);

        var svg = utils.createSvg(id, width, height, "visible");

        const g = svg
            .selectAll(`g#${id}-g`)
            .data(matrix)
            .join((enter) => {
                enter
                    .append("g")
                    .attr("id", `${id}-g`)
                    .attr("transform", (d) => `translate(0, ${y(d.source)})`)
                    .selectAll("rect")
                    .data((d) => d.sequence)
                    .join("rect")
                    .attr("x", (d) => x(d.party))
                    .attr("y", 0)
                    .attr("width", x.bandwidth())
                    .attr("height", y.bandwidth())
                    .attr("rx", 3)
                    .attr("stroke", "#000")
                    .attr("stroke-width", 2)
                    .attr("fill", (d) => c(d.n));
            });

        const labelsx = svg
            .append("g")
            .attr("id", `g#${id}-lx`)
            .selectAll("text")
            .data(matrix)
            .join("text")
            .attr(
                "transform",
                (d) =>
                    `translate(${x(d.source) + 20}, ${margins.top - 20}) rotate(-45)`,
            )
            .attr("x", 0)
            .attr("y", y.bandwidth() / 4)
            .text((d) => d.source);

        const labelsy = svg
            .append("g")
            .attr("id", `g#${id}-ly`)
            .selectAll("text")
            .data(matrix)
            .join("text")
            .attr(
                "transform",
                (d) =>
                    `translate(${margins.left - 20}, ${y(d.source) + 20}) rotate(0)`,
            )
            .attr("x", 0)
            .attr("y", y.bandwidth() / 4)
            .attr("text-anchor", "end")
            .text((d) => d.source);

        const values = svg
            .append("g")
            .attr("id", `g#${id}-values`)
            .selectAll("g")
            .data(matrix)
            .join((enter) => {
                enter
                    .append("g")
                    .attr("id", `${id}-g`)
                    .attr("transform", (d) => `translate(0, ${y(d.source)})`)
                    .selectAll("text")
                    .data((d) => d.sequence)
                    .join("text")
                    .attr("x", (d) => x(d.party) + x.bandwidth() / 2)
                    .attr("y", y.bandwidth() / 2 + 5)
                    .attr("text-anchor", "middle")
                    .attr("fill", (d) => (d.n > 30 ? "white" : "black"))
                    .text((d) => d.n > 0 ? d.n : "-"); // (d.n * 100).toFixed(1));

                utils.setText(enter.selectAll("text"), 20, 500, "middle");
            });

        utils.setText(labelsx, 20, 500, "start");
        utils.setText(labelsy, 20, 500, "end");
    });
</script>

<div {id} class="pt-8"></div>

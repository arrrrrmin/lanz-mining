<script>
    import { onMount } from "svelte";
    import * as utils from "./utils.js";
    import * as d3 from "d3";

    let { data, id, groupOrder } = $props();

    let _data = data.data.filter((d) => d.date > utils.dateContext.full);

    const parties = new Array(...new Set(_data.map((d) => d.party)))
        .filter((d) => d !== "")
        .sort((a, b) => a.localeCompare(b));

    const groups = Object.keys(groupOrder);

    const findMatches = (data, party) => {
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

        // Number of all guests with a group affiliation other than politican & journalist
        const nGuests = d3.sum(
            partyEpisodes,
            (d) => d.children.filter((D) => groups.includes(D.group)).length,
        );

        const sequence = groups.map((_grp) => {
            let n = d3.sum(
                partyEpisodes,
                (d) => d.children.filter((D) => D.group == _grp).length,
            );
            // let n = d3.sum(
            //     partyEpisodes,
            //     (d) => d.children.filter((D) => D.group === _grp).length,
            // );
            return { group: _grp, perc: n / nGuests, n: n }; //
        });
        // Check back everything sums up to one!
        // console.log(d3.sum(sequence, (d) => d.perc));
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
        const width = 1100;
        const height = 800;
        const margins = { left: 150, top: 150, right: 80, bottom: 10 };

        const x = d3
            .scaleBand()
            .range([margins.left, width - margins.right])
            .domain(groups);
        const y = d3
            .scaleBand()
            .range([margins.top, height - margins.bottom])
            .domain(parties);
        //const c = d3.scaleSequential([0, 30], d3.interpolateRdPu);
        const c = d3.scaleSequential([0, 25], d3.interpolateRdPu);

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
                    .attr("x", (d) => x(d.group))
                    .attr("y", 0)
                    .attr("width", x.bandwidth())
                    .attr("height", y.bandwidth())
                    .attr("rx", 3)
                    .attr("stroke", "#000")
                    .attr("stroke-width", 2)
                    // .attr("fill", (d) => c(d.n));
                    .attr("fill", (d) => c((d.perc * 100).toFixed(1)));
            });

        const labelsx = svg
            .append("g")
            .attr("id", `g#${id}-lx`)
            .selectAll("text")
            .data(groups)
            .join("text")
            .attr(
                "transform",
                (d) =>
                    `translate(${x(d) + 20}, ${margins.top - 20}) rotate(-45)`,
            )
            .attr("x", 0)
            .attr("y", y.bandwidth() / 4)
            .text((d) => d);

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

        const percentages = svg
            .append("g")
            .attr("id", `g#${id}-percentages`)
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
                    .attr("x", (d) => x(d.group) + x.bandwidth() / 2)
                    .attr("y", y.bandwidth() / 2 + 5)
                    // .attr("fill", (d) => (d.n >= 18 ? "white" : "black"))
                    // .text((d) => d.n);
                    .attr("fill", (d) => (d.perc > 0.15 ? "white" : "black"))
                    .text((d) =>
                        d.perc != 0.0 ? (d.perc * 100).toFixed(1) : "-",
                    );

                utils.setText(enter.selectAll("text"), 20, 500, "middle");
            });
        utils.setText(labelsx, 20, 500, "start");
        utils.setText(labelsy, 20, 500, "end");
    });
</script>

<div {id} class="pt-8"></div>

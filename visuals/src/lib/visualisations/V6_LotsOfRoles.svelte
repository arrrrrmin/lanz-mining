<script>
    import { onMount } from "svelte";
    import * as utils from "./utils.js";
    import * as d3 from "d3";

    // Get props
    let { data, id } = $props();

    let _data = data.data.filter((d) => d.role);

    let mappings = {
        name: "Gruppe",
        children: d3
            .rollups(
                _data,
                (D) =>
                    d3
                        .groups(D, (e) => e.role)
                        .map((E) => ({ name: E[0], count: E[1].length }))
                        .sort((a, b) => b.count - a.count),
                (d) => d.group,
            )
            .map((d) => ({ name: d[0], children: d[1] })),
    };

    onMount(() => {
        const width = 900;
        const height = width;
        const cx = width * 0.5;
        const cy = height * 0.5;
        const radius = Math.min(width, height) / 2 - 100;

        const tree = d3
            .tree()
            .size([2 * Math.PI, radius])
            .separation((a, b) => (a.parent == b.parent ? 1 : 2) / a.depth);

        const root = tree(
            d3
                .hierarchy(mappings)
                .sort((a, b) => d3.ascending(a.data.name, b.data.name)),
        );

        let svg = d3
            .select(`div#${id}`)
            .append("svg")
            .attr("viewBox", [-cx, -cy, width, height]);

        // Append links.
        svg.append("g")
            .attr("fill", "none")
            .attr("stroke", "#57534d")
            .attr("stroke-opacity", 0.3)
            .attr("stroke-width", 1.5)
            .selectAll()
            .data(root.links().filter((d) => d.source.depth > 0))
            .join("path")
            .attr(
                "d",
                d3
                    .linkRadial()
                    .angle((d) => d.x)
                    .radius((d) => d.y),
            );

        svg.append("g")
            .selectAll()
            .data(root.descendants().filter((d) => d.depth > 0))
            .join("circle")
            .attr(
                "transform",
                (d) =>
                    `rotate(${(d.x * 180) / Math.PI - 90}) translate(${d.y},0)`,
            )
            .attr("fill", (d) => "#0c0a09")
            .attr("r", (d) => (!d.children ? 2 : 4));

        svg.append("g")
            .selectAll()
            .data(root.descendants().filter((d) => d.depth > 0))
            .join("text")
            .attr(
                "transform",
                (d) =>
                    `rotate(${(d.x * 180) / Math.PI - 90}) translate(${d.y},0) rotate(${d.x >= Math.PI ? 180 : 0})`,
            )
            .attr("dy", "0.31em")
            .attr("x", (d) => (d.x < Math.PI === !d.children ? 6 : -6))
            .attr("text-anchor", (d) =>
                d.x < Math.PI === !d.children ? "start" : "end",
            )
            .attr("font-size", (d) => (!d.children ? 12 : 20))
            .attr("font-weight", (d) => (!d.children ? 400 : 600))
            .attr("fill", "#0c0a09")
            .text((d, i) =>
                i % 6 == 0 || d.parent.data.name === "Gruppe"
                    ? //d.children
                      d.data.name
                    : "",
            );
    });
</script>

<div {id} class="py-8"></div>

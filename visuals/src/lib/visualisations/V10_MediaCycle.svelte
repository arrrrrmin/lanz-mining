<script>
    import { onMount } from "svelte";
    import * as utils from "./utils.js";
    import * as d3 from "d3";

    let { data, id, formatOrder } = $props();

    const start = new Date(2024, 1, 1);

    const sortByChildren = (a, b) => {
        return b.children.length - a.children.length;
    };

    const sortByChildrenSum = (a, b) => {
        return (
            d3.sum(b.children, (d) => d.value) -
            d3.sum(a.children, (d) => d.value)
        );
    };

    const transformData = (originalData) => {
        let _data = originalData
            .filter((d) => d.date >= start)
            .filter((d) => d.group === "Journalismus" && d.media !== "");

        let _groups = d3
            .groups(_data, (d) => d.media)
            .map((D) => ({
                name: D[0], // media
                children: D[1]
                    .map((e) => ({ name: e.talkshow, value: 1 }))
                    .sort((a, b) => formatOrder[a.name] - formatOrder[b.name]),
                value: D[1].length,
            }))
            .sort(sortByChildrenSum);

        return { name: "media", children: _groups };
    };

    let _data = transformData(data.data);

    onMount(() => {
        const width = 900;
        const height = width;
        const cx = width * 0.5;
        const cy = height * 0.5;
        const radius = Math.min(width, height) / 2 - 10;

        const tree = d3
            .tree()
            .size([2 * Math.PI, radius])
            .separation((a, b) => (a.parent == b.parent ? 1 : 2) / a.depth);

        // Sort the tree and apply the layout.
        const root = tree(
            d3
                .hierarchy(_data)
                .sort((a, b) => d3.descending(a.data.value, b.data.value)),
        );

        const svg = d3
            .select(`div#${id}`)
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .attr("viewBox", [-cx, -cy, width, height])
            .attr("style", "width: 100%; height: auto; font: 10px sans-serif;");

        svg.append("g")
            .attr("fill", "none")
            .attr("stroke-opacity", 0.4)
            .attr("stroke-width", 1.5)
            .selectAll()
            .data(root.links().filter((d) => d.source.depth > 0))
            .join("path")
            .attr("stroke", (d) =>
                d.target.data.name in formatOrder
                    ? utils.showKeyToColour[d.target.data.name]
                    : "#ccc",
            )
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
            // .attr("fill", (d) => (d.children ? "#555" : "#999"))
            .attr("fill", (d) =>
                d.data.name in formatOrder
                    ? utils.showKeyToColour[d.data.name]
                    : "#ccc",
            )
            .attr("r", 5);

        // Append labels.
        svg.append("g")
            .attr("stroke-linejoin", "round")
            .attr("stroke-width", 3)
            .selectAll()
            .data(
                root
                    .descendants()
                    .filter((d) => d.depth === 1 && d.data.children.length > 4),
            )
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
            .attr("font-size", 22)
            .attr("font-weight", 500)
            //.attr("paint-order", "stroke")
            //.attr("stroke", "white")
            .attr("fill", "currentColor")
            .text((d) => d.data.name);
    });
</script>

<div {id} class="pt-8"></div>

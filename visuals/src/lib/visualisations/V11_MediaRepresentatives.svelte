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
                children: d3
                    .groups(D[1], (e) => e.name)
                    .map((E) => ({
                        name: E[0],
                        children: E[1]
                            .map((f) => ({ name: f.talkshow }))
                            .sort(
                                (a, b) =>
                                    formatOrder[a.name] - formatOrder[b.name],
                            ),
                        value: E[1].length,
                    }))
                    //.sort(sortByChildren),
                    .sort((a, b) => b.value - a.value),
                value: D[1].length,
            }))
            .sort(sortByChildrenSum);

        return { name: "media", children: _groups.slice(0, 10) };
    };

    let _data = transformData(data.data);

    onMount(() => {
        const width = 1600;
        const height = width;
        const cx = width * 0.5;
        const cy = height * 0.5;
        const radius = Math.min(width, height) / 2 - 10;

        const tree = d3
            .tree()
            .size([Math.PI, radius])
            .separation((a, b) => (a.parent == b.parent ? 1 : 4) / a.depth);

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
            .attr("height", height / 2)
            .attr("viewBox", [-cx, -cy, width, height / 2])
            .attr("style", "width: 100%; height: auto; font: 10px sans-serif;");

        const descendants = root.descendants().filter((d) => d.depth > 0);
        const links = root.links().filter((d) => d.source.depth > 0);

        svg.append("g")
            .attr("fill", "none")
            .attr("stroke-opacity", 0.4)
            .attr("stroke-width", 1.5)
            .attr("transform", "rotate(-90)")
            .selectAll()
            .data(links)
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
            .attr("transform", "rotate(-90)")
            .selectAll()
            .data(descendants)
            .join("circle")
            .attr(
                "transform",
                (d) =>
                    `rotate(${(d.x * 180) / Math.PI - 90}) translate(${d.y},0)`,
            )
            .attr("fill", (d) =>
                Object.keys(utils.showKeyToColour).includes(d.data.name)
                    ? utils.showKeyToColour[d.data.name]
                    : "black",
            )
            .attr("r", (d) => (d.depth === 3 ? 5 : 2.5));

        // Append labels.
        svg.append("g")
            .attr("transform", "rotate(-90)")
            .attr("stroke-linejoin", "round")
            .attr("stroke-width", 3)
            .selectAll()
            .data(
                descendants.filter(
                    (d) =>
                        (d.depth <= 2 && d.children.length > 3) ||
                        d.depth === 1,
                ),
            )
            .join("text")
            .attr("transform", (d) =>
                d.x >= Math.PI / 2
                    ? `rotate(${(d.x * 180) / Math.PI - 90}) translate(${d.y},0) rotate(${0})`
                    : `rotate(${(d.x * 180) / Math.PI - 90}) translate(${d.y},0) rotate(${180})`,
            )
            .attr("dy", "0.31em")
            .attr("x", (d) => (d.x >= Math.PI / 2 ? -6 : 6))
            .attr("text-anchor", (d) => (d.x >= Math.PI / 2 ? "end" : "start"))
            .attr("font-size", 24)
            .attr("font-weight", 500)
            .attr("fill", "currentColor")
            .text((d) => d.data.name);
    });
</script>

<div {id} class="pt-8"></div>

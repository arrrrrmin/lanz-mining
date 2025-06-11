<script>
    import { onMount } from "svelte";
    import * as utils from "./utils.js";
    import * as d3 from "d3";

    let { data, id } = $props();

    const transformData = (originalData, n = 10) => {
        let _data = originalData.filter((d) => d.date >= new Date(2024, 1, 1));
        _data = _data.filter((d) => d.role.toLowerCase().includes("expert"));
        _data = _data.sort(
            (a, b) =>
                _data.filter((d) => d.name == b.name).length -
                _data.filter((d) => d.name == a.name).length,
        );

        let n_names = new Array(...new Set(_data.map((d) => d.name))).slice(
            0,
            n,
        );
        _data = _data
            .filter((d) => n_names.includes(d.name))
            .filter((d) => d.role.length > 0);

        _data = d3
            .groups(_data, (D) => D.name)
            .map((e) => ({
                name: e[0],
                children: e[1].map((E) => ({ name: E.role })),
            }))
            .sort((a, b) => b.children.length - a.children.length);

        return { name: "Experten", children: _data };
    };

    let _data = transformData(data.data, 5);

    onMount(() => {
        const width = 1200;

        const root = d3.hierarchy(_data);
        const dx = 28;
        const dy = width / (root.height + 1);

        // Create a tree layout.
        const tree = d3.tree().nodeSize([dx, dy]);

        // Sort the tree and apply the layout.
        root.sort((a, b) =>
            d3.ascending(
                b.data.children ? b.data.children.length : 0,
                a.data.children ? a.data.children.length : 0,
            ),
        );
        tree(root);

        // Compute the extent of the tree. Note that x and y are swapped here
        // because in the tree layout, x is the breadth, but when displayed, the
        // tree extends right rather than down.
        let x0 = Infinity;
        let x1 = -x0;
        root.each((d) => {
            if (d.x > x1) x1 = d.x;
            if (d.x < x0) x0 = d.x;
        });

        // Compute the adjusted height of the tree.
        const height = x1 - x0 + dx * 2;

        const svg = d3
            .select(`div#${id}`)
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .attr("viewBox", [-dy / 3, x0 - dx, width, height])
            .attr(
                "style",
                "max-width: 100%; height: auto; font: 10px sans-serif;",
            );

        const link = svg
            .append("g")
            .attr("fill", "none")
            .attr("stroke", "#44403b")
            .attr("stroke-opacity", 0.4)
            .attr("stroke-width", 1.5)
            .selectAll()
            .data(root.links())
            .join("path")
            .attr(
                "d",
                d3
                    .linkVertical()
                    .x((d) => d.y)
                    .y((d) => d.x),
            );

        const node = svg
            .append("g")
            .attr("stroke-linejoin", "round")
            .attr("stroke-width", 3)
            .selectAll()
            .data(root.descendants())
            .join("g")
            .attr("transform", (d) => `translate(${d.y},${d.x})`);

        node.append("circle").attr("fill", "#44403b").attr("r", 4);

        var nodeTexts = node
            .append("text")
            .attr("dy", "0.31em")
            .attr("x", (d) => (d.children ? -6 : 6))
            .attr("font-size", 20)
            .attr("font-weight", (d) => (d.children ? 600 : 500))
            .text((d) => d.data.name);

        //utils.setText(nodeTexts, 20, 600);
        nodeTexts.attr("text-anchor", (d) => (d.children ? "end" : "start"));
    });
</script>

<div {id}></div>

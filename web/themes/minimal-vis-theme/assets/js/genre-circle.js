genreVisualization = async () => {
    
    transformToCirclePack = (rawData) => {
        //let csvData = await d3.csv("js/data.csv").then(d => d);
        var data = d3.groups(rawData, (D) => D.genre)
            .map(genreGrp =>
            ({
                name: genreGrp[0],
                children:
                    d3.groups(genreGrp[1], (d) => d.role)
                        .map(rolesGrp =>
                        ({
                            name: rolesGrp[0],
                            children:
                                d3.groups(rolesGrp[1], (E) => E.name)
                                    .map(nameGrp => ({ name: nameGrp[0], value: nameGrp[1].length }))
                        })
                        ),
            })
            )
        return { name: "guests", children: data };
    }

    const width = 900;
    const height = width;

    const csvData = await loadData("js/data.csv");
    var data = transformToCirclePack(csvData);

    const pack = data => d3.pack()
        .size([width, height])
        .padding(2)
        (d3.hierarchy(data)
            .sum(d => d.value)
            .sort((a, b) => b.value - a.value));
    const root = pack(data);

    const svg = d3.select("#genre-vis")
        .append("svg")
        .attr("viewBox", `-${width / 2} -${height / 2} ${width} ${height}`)
        .attr("width", width)
        .attr("height", height)
        .attr("style", `max-width: 100%; height: auto; cursor: pointer;`);

    const node = svg.append("g")
        .selectAll("circle")
        .data(root.descendants().slice(1))
        .join("circle")
        .attr("fill", d => d.children ? "#fff" : defaultColors.light)
        .attr("stroke", d => d.children ? defaultColors.light : null)
        .attr("stroke-width", 1)
        .attr("pointer-events", d => !d.children ? "none" : null)
        .on("mouseover", function () { d3.select(this).attr("stroke-opacity", 0.5); })
        .on("mouseout", function () { d3.select(this).attr("stroke-opacity", 1.0); })
        .on("click", (event, d) => focus !== d && (zoom(event, d), event.stopPropagation()));

    const labels = svg.append("g")
        .attr("pointer-events", "none")
        .attr("text-anchor", "middle")
        .selectAll("text")
        .data(root.descendants())
        .join("text")
        .style("fill-opacity", d => d.parent === root ? 1 : 0)
        .style("display", d => d.parent === root ? "inline" : "none")
        .text(d => d.data.name);

        applyFontConfig(labels, true)

    // Create the zoom behavior and zoom immediately in to the initial focus node.
    svg.on("click", (event) => zoom(event, root));
    let focus = root;
    let view;
    zoomTo([focus.x, focus.y, focus.r * 2]);

    function zoomTo(v) {
        const k = width / v[2];
        view = v;

        labels.attr("transform", d => `translate(${(d.x - v[0]) * k},${(d.y - v[1]) * k})`);
        node.attr("transform", d => `translate(${(d.x - v[0]) * k},${(d.y - v[1]) * k})`);
        node.attr("r", d => d.r * k);
    }

    function zoom(event, d) {
        focus = d;

        const transition = svg.transition()
            .duration(event.altKey ? 7500 : 750)
            .tween("zoom", _ => {
                const i = d3.interpolateZoom(view, [focus.x, focus.y, focus.r * 2]);
                return t => zoomTo(i(t));
            });

        labels
            .filter(function (d) { return d.parent === focus || this.style.display === "inline"; })
            .transition(transition)
            .style("fill-opacity", d => d.parent === focus ? 1 : 0)
            .on("start", function (d) { if (d.parent === focus) this.style.display = "inline"; })
            .on("end", function (d) { if (d.parent !== focus) this.style.display = "none"; });
    }

}

genreVisualization();
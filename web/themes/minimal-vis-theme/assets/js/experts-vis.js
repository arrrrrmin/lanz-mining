expertsVisualization = async () => {

    transformToStackedBar = (rawData) => {
        pairwiseCumsum = (d) => {
            var dSort = d.sort((a, b) => a["count"] - b["count"]);
            var values = d3.pairs([0, ...d3.cumsum(dSort, d => d["count"])]);
            return dSort.map((d, i) => ({ name: d["name"], start: values[i][0], end: values[i][1] }))
        }

        maxOfEnds = (d) => d3.max(d["experts"].map(D => D["end"]));

        var filteredData = d3.filter(rawData, d => !!d["expertise"])
        var data = d3.rollups(
            filteredData,
            (D) => (d3.rollups(D, E => E.length, e => e["name"]).map(
                vals => ({
                    name: vals[0],
                    count: vals[1],
                })
            )),
            d => d["expertise"]
        ).map(
            vals => ({
                expertise: vals[0],
                experts: pairwiseCumsum(vals[1].sort((a, b) => a["count"] - b["count"]))
            })
        ).sort((a, b) => maxOfEnds(b) - maxOfEnds(a)).slice(0, n);

        data = data.flatMap(d => {
            const expertise = d.expertise;
            return d.experts.map(D => ({
                expertise: expertise,
                name: D.name,
                start: D.start,
                end: D.end
            }));
        });
        return data;
    }

    clickExpertsBarAction = (event, d) => {
        sourceRect = d3.select(`#${event.target.id}`);
        if (d.name != helperText.node().innerHTML) {
            helperText
                .style("top", (event.pageY + 2.5) + "px")
                .style("left", (event.pageX + 2.5) + "px")
                .style("display", "block")
                .html(d.name);
        } else {
            helperText
                .style("top", null)
                .style("left", null)
                .style("display", "None")
                .html(null);
        }
    }

    const margins = { top: 25, right: 25, bottom: 25, left: 65 };
    const width = 900;
    const height = 1200;
    const n = 16;
    const csvData = await loadData("js/data.csv");
    var data = transformToStackedBar(csvData);

    var svg = d3.select("#experts-vis")
        .append("svg")
        .attr("viewBox", [0, 0, width + margins.right, height])
        .attr("style", `max-width: ${width}px; height: auto; font: 10px sans-serif; overflow: visible;`);

    var x = d3.scaleLinear()
        .range([width - margins.left, margins.right]);

    var y = d3.scaleBand()
        .range([margins.top, height - margins.bottom])
        .padding(0.1);

    var c = d3.scaleSequential()
        .interpolator(d3.interpolateRgb(defaultColors.light, defaultColors.dark));

    var gx = svg.append("g")
        .attr("id", "gx-experts")
        .attr("transform", `translate(${margins.left},${margins.top})`);
    var gy = svg.append("g")
        .attr("id", "gy-experts")
        .attr("transform", `translate(${margins.left + margins.right},0)`);

    var helperText = d3.select("#experts-vis").append("div")
        .attr("id", "expert-helper-tt-div")
        .attr("class", "px-1 py-0.5 bg-white rounded-sm")
        // Here we need to apply a different font size, since we'r not inside the svg.
        .style("font-size", "11px")
        .style("font-weight", 400)
        .style("position", "absolute")
        .style("display", "none")
        .style("text-anchor", "end");


    updateExpertsVisualization = () => {

        x.domain([d3.max(data, d => d["end"]), 0]).nice();
        y.domain(data.map(d => d["expertise"]));
        c.domain([1, d3.max(data, d => d["end"] - d["start"])]);

        gx.transition()
            .duration(1000)
            .call(d3.axisBottom(x).tickSizeOuter(0))
            .call(g => g.select(".domain").remove());
        
        applyFontConfig(gx, true);
        applyTextOffset(gx, "0em", "-0.75em", true)

        gy.transition()
            .duration(1000)
            .call(d3.axisLeft(y))
            .call(g => g.select(".domain").remove());
        
        applyFontConfig(gy, true);
        applyTextOffset(gy, "-0.25em", "0.25em", true)

        var bar = svg
            .append("g")
            .attr("id", "expert-bar-g")
            .attr("transform", `translate(${margins.left},0)`)
            .selectAll("rect")
            .data(data)

        bar
            .join("rect")  // per bar in series
            .attr("id", (_, i) => `expert-rect-${i}`)
            .on("click", (e, d) => clickExpertsBarAction(e, d))
            .on("mouseover", function () { d3.select(this).attr("fill-opacity", 0.85) })
            .on("mouseout", function () { d3.select(this).attr("fill-opacity", 1.0) })
            .transition()
            .delay((_, i) => i * 50)
            .attr("x", d => x(d.start))
            .attr("y", d => y(d.expertise))
            .attr("fill", d => c(d.end - d.start))
            .attr("rx", 3)
            .attr("stroke", "white")
            .attr("width", d => x(d.end) - x(d.start))
            .attr("height", y.bandwidth());

        var mainExpertLabels = bar.select("#expert-bar-g")
            .data(d3.groups(data, d => d["expertise"]).map(vals => vals[1][vals[1].length - 1]))
            .join("text")
            .attr("x", d => x(d.end))
            .attr("y", d => y(d.expertise))
            .style("text-anchor", "start")
            .text(d => d.name);

        applyFontConfig(mainExpertLabels, false);
        applyTextOffset(mainExpertLabels, "0.25em", "2em", false);

        bar
            .exit()
            .remove();
    }

    updateExpertsVisualization();

}

expertsVisualization();
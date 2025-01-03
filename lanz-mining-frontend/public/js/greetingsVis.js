
colors = {
    "SPD": "#ef4444",
    "CDU": "#292524",
    "CSU": "#292524",
    "B90G": "#16a34a",
    "FDP": "#facc15",
    "LINKE": "#db2777",
    "Parteilos": "#a8a29e",
    "AfD": "#60a5fa",
    "BSW": "#9333ea",
    "Freie Wähler": "#57534e",
}
defaultColors = {
    dark: "#334155",
    light: "#94a3b8",
    highlight: "#f87171",
}

greetingsVis = async () => {

    loadData = async () => {
        let csvData = await d3.csv("js/data.csv").then(d => d);
        return csvData
    }

    initButtons = () => {
        d3.select("#greetingsVis")
            .selectAll("button")
            .join()
            .on("click", (event) => updateGreetingsVis(event.target.value));
    }

    handleBarClick = (_, d) => {
        var s = x(data[0].name) - 12
        var lineData = [
            [s, y(d.count)], [s - 8, y(d.count)]
        ];
        helper.attr("d", line(lineData))
        helperT.text(d.count)
            .attr("x", s - 10)
            .attr("y", y(d.count) + 3);
    }

    handleBarMouseover = (_, d) => {
    }

    handleBarMouseout = (_, d) => {

    }

    const margins = { top: 25, right: 0, bottom: 50, left: 25 };
    const width = 700;
    const height = 500;
    const n = 10;
    const csvData = await loadData();

    initButtons();

    var svg = d3.select("#greetingsVis")
        .append("svg")
        .attr("viewBox", [0, 0, width, height + margins.bottom])
        .attr("style", `max-width: ${width}px; height: auto; font: 10px sans-serif; overflow: visible;`);

    var x = d3.scaleBand()
        .range([margins.left, width - margins.right])
        .padding(0.2);
    var y = d3.scaleLinear()
        .range([height - margins.bottom, margins.top]);

    var gx = svg.append("g")
        .attr("id", "gx")
        .attr("transform", `translate(0,${height - margins.bottom})`);
    var gy = svg.append("g")
        .attr("id", "gy")
        .attr("transform", `translate(${margins.left},0)`);

    var helper = svg.append("path")
        .attr("id", "helper")
        .attr("stroke", defaultColors.highlight)
        .attr("stroke-width", 1.5)
    var helperT = svg.append("text")
        .attr("id", "helperT")
        .attr("font-weight", 600)
        .attr("fill", defaultColors.highlight)
        .style("text-anchor", "end")

    const line = d3.line()
        .x((d) => d[0])
        .y((d) => d[1]);

    updateGreetingsVis = (type) => {
        console.log(csvData);
        if (type == "guests") {
            data = d3.rollups(csvData, D => D.length, d => d["name"])
                .sort((a, b) => b[1] - a[1])
                .map(vals => { return { name: vals[0], count: vals[1] } })
                .slice(0, n);
        } else if (type == "genres") {
            data = d3.rollups(csvData, D => D.length, d => d["genre"])
                .sort((a, b) => b[1] - a[1])
                .map(vals => { return { name: vals[0], count: vals[1] } })
                .slice(0, n);
        } else if (type == "parties") {
            data = d3.rollups(
                csvData.filter((d) => d["party"].length > 0), D => D.length, d => d["party"])
                .sort((a, b) => b[1] - a[1])
                .map(vals => { return { name: vals[0], count: vals[1] } })
                .slice(0, n);
        } else {  // type == media
            data = d3.rollups(
                csvData.filter((d) => d["pub_platform"].length > 0), D => D.length, d => d["pub_platform"])
                .sort((a, b) => b[1] - a[1])
                .map(vals => { return { name: vals[0], count: vals[1] } })
                .slice(0, n);
        }

        x.domain(data.map(d => d.name));
        y.domain([0, d3.max(data, d => d.count)]).nice();

        helper.attr("d", null);
        helperT.text(null);

        var bar = svg.selectAll("rect")
            .data(data);

        bar
            .enter()
            .append("rect") // Add new elements
            .merge(bar) // Merge with existing elements
            .attr("x", d => x(d.name))
            .attr("y", d => y(d.count))
            .on("click", (e, d) => handleBarClick(e, d))
            .on("mouseover", function () { d3.select(this).attr("fill-opacity", 0.9) })
            .on("mouseout", function () { d3.select(this).attr("fill-opacity", 1.0) })
            .transition()
            .duration(750)
            .attr("rx", 3)
            .attr("fill", d => d.name in colors ? colors[d.name] : defaultColors.light)
            .attr("height", d => y(0) - y(d.count))
            .attr("width", x.bandwidth());


        gx.transition()
            .duration(1000)
            .call(d3.axisBottom(x).tickSizeOuter(0))
            .call(g => g.select(".domain").remove())
            .selectAll("text")
            .attr("font-size", 12)
            .attr("font-weight", 600)
            .style("text-anchor", "end")
            .attr("dx", "-0.5em")
            .attr("dy", "-0.5em")
            .attr("transform", "rotate(-90)");

        gy.transition()
            .duration(1000)
            .call(d3.axisLeft(y))
            .call(g => g.select(".domain").remove());

    }

    updateGreetingsVis("guests")

}

greetingsVis();
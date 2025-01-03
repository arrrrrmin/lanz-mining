
colors = {
    SPD: "red-500",
    CDU: "stone-800",
    CSU: "stone-800",
    B90G: "green-600",
    FDP: "yellow-400",
    LINKE: "pink-600",
    Parteilos: "stone-400",
    AfD: "blue-400",
    BSW: "purple-600",
    "Freie Wähler": "stone-600",
}

greetingsVis = async () => {
    initButtons = () => {
        d3.select("#greetingsVis")
            .selectAll("button")
            .join()
            .on("click", (event) => updateGreetingsVis(event.target.value));
    }

    loadData = async () => {
        let data = await d3.csv("js/data.csv").then(d => d);
        return data
    }

    const margins = { top: 25, right: 25, bottom: 50, left: 25 };
    const width = 600;
    const height = width;
    const n = 10;
    const data = await loadData();

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
        .attr("transform", `translate(0,${height - margins.bottom})`);
    var gy = svg.append("g")
        .attr("transform", `translate(${margins.left},0)`);


    updateGreetingsVis = (type) => {
        console.log(type);
        if (type == "guests") {
            newData = d3.rollups(data, D => D.length, d => d["name"])
                .sort((a, b) => b[1] - a[1])
                .map(vals => { return { name: vals[0], count: vals[1] } })
                .slice(0, n);
        } else if (type == "genres") {
            newData = d3.rollups(data, D => D.length, d => d["genre"])
                .sort((a, b) => b[1] - a[1])
                .map(vals => { return { name: vals[0], count: vals[1] } })
                .slice(0, n);
        } else {
            newData = d3.rollups(
                data.filter((d) => d["party"].length > 0), D => D.length, d => d["party"])
                .sort((a, b) => b[1] - a[1])
                .map(vals => { return { name: vals[0], count: vals[1] } })
                .slice(0, n);
        }
        console.log(newData);

        x.domain(newData.map(d => d.name));
        y.domain([0, d3.max(newData, d => d.count)]).nice();

        var bar = svg.selectAll("rect")
            .data(newData);

        bar
            .enter()
            .append("rect") // Add new elements
            .merge(bar) // Merge with existing elements
            .transition() // Apply changes to all
            .attr("x", d => x(d.name))
            .attr("y", d => y(d.count))
            .attr("class", d => d.name in colors ? `fill-${colors[d.name]}` : "fill-stone-500")
            .duration(500)
            .attr("height", d => y(0) - y(d.count))
            .attr("width", x.bandwidth())

        gx.transition()
            .duration(1000)
            .call(d3.axisBottom(x).tickSizeOuter(0))
            .call(g => g.select(".domain").remove())
            .selectAll("text")
            .style("text-anchor", "end")
            .attr("dx", "-0.5em")
            .attr("dy", "0.5em")
            .attr("transform", "rotate(-60)");

        gy.transition()
            .duration(1000)
            .call(d3.axisLeft(y))
            .call(g => g.select(".domain").remove());

    }

    updateGreetingsVis("guests")

}

greetingsVis();
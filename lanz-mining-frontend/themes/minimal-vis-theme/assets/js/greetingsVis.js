
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

    getDate = (str) => {
        const tParser = d3.timeParse("%Y-%m-%d")
        return tParser(str.split('T')[0])
    }

    loadData = async () => {
        let csvData = await d3.csv("js/data.csv").then(d => d);
        csvData = csvData.map(d => {
            d["date"] = d3.timeParse("%Y-%m-%d")(d["date"].split('T')[0])
            return d
        });
        return csvData
    }

    initButtons = () => {
        d3.select("#greetingsVis")
            .selectAll("#greeting-vis-button")
            .join()
            .on("click", (event) => updateGreetingsVis(event.target.value, year));

        d3.select("#greetings-vis-option-button")
            .join()
            .on("click", (_) => {
                var div = document.getElementById("greetings-vis-options-div");
                if (div.style.display == "none") {
                    div.style.display = "block";
                }
                else {
                    div.style.display = "none";
                }
            });

        const all_years = new Set([...csvData.map(d => d.date.getFullYear())]);
        all_years.add("Alle");
        d3.select("#greetings-vis-option-list").selectAll("button")
            .data(all_years)
            .join("button")
            .attr("type", "button")
            .attr("name", d => d)
            .attr("value", d => d)
            .attr("id", (_, i) => `menu-item-${i}`)
            .attr("class", "block px-4 py-2 text-sm text-gray-700lock")
            .attr("role", "menuitem")
            .attr("tabindex", -1)
            .on("click", event => updateGreetingsVis(type, event.target.value))
            .html(d => d)

    }

    dataFilter = (year) => {
        var filteredData = csvData;
        if (year != "Alle") {
            var r = [new Date(`${year}-01-01`), new Date(`${parseInt(year) + 1}-01-01`)]
            console.log(r)
            filteredData = d3.filter(csvData, d => (r[0] <= d.date && d.date < r[1]))
        }
        console.log(filteredData);

        return filteredData;
    }

    dataSlice = (iType, iYear) => {
        console.log(iType, iYear)
        type = iType;
        year = iYear;
        var filteredData = dataFilter(year)
        if (type == "guests") {
            data = d3.rollups(filteredData, D => D.length, d => d["name"])
                .sort((a, b) => b[1] - a[1])
                .map(vals => { return { name: vals[0], count: vals[1] } })
                .slice(0, n);
        } else if (type == "genres") {
            data = d3.rollups(filteredData, D => D.length, d => d["genre"])
                .sort((a, b) => b[1] - a[1])
                .map(vals => { return { name: vals[0], count: vals[1] } })
                .slice(0, n);
        } else if (type == "parties") {
            data = d3.rollups(
                filteredData.filter((d) => d["party"].length > 0), D => D.length, d => d["party"])
                .sort((a, b) => b[1] - a[1])
                .map(vals => { return { name: vals[0], count: vals[1] } })
                .slice(0, n);
        } else if (type == "media") {
            data = d3.rollups(
                filteredData.filter((d) => d["pub_platform"].length > 0), D => D.length, d => d["pub_platform"])
                .sort((a, b) => b[1] - a[1])
                .map(vals => { return { name: vals[0], count: vals[1] } })
                .slice(0, n);
        }
        return data;
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

    handleYearSelection = (event) => {
        year = event.target.value

    }

    const margins = { top: 25, right: 0, bottom: 50, left: 25 };
    const width = 900;
    const height = 500;
    const n = 16;
    const csvData = await loadData();
    var year = "Alle";
    var type = "guests"
    // var data = dataSlice(type, year)

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


    updateGreetingsVis = (iType, iYear) => {
        year = iYear;
        type = iType;
        var data = dataSlice(type, year)
        console.log(data);

        x.domain(data.map(d => d.name));
        y.domain([0, d3.max(data, d => d.count)]).nice();

        helper.attr("d", null);
        helperT.text(null);

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

        var bar = svg.selectAll("rect")
            .data(data)

        bar
            .join("rect") // Add new elements
            .on("click", (e, d) => handleBarClick(e, d))
            .on("mouseover", function () { d3.select(this).attr("fill-opacity", 0.9) })
            .on("mouseout", function () { d3.select(this).attr("fill-opacity", 1.0) })
            .transition()
            .duration(750)
            .attr("x", d => x(d.name))
            .attr("y", d => y(d.count))
            .attr("rx", 3)
            .attr("fill", d => d.name in colors ? colors[d.name] : defaultColors.light)
            .attr("height", d => y(0) - y(d.count))
            .attr("width", x.bandwidth());

        bar
            .exit()
            .remove();

    }

    updateGreetingsVis(type, year)

}

greetingsVis();
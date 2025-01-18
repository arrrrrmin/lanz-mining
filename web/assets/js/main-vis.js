mainVisualization = async (targetId, dataPath) => {

    initializeButtons = (targetId) => {

        /** Applying functionality */
        d3.selectAll("#greeting-vis-button")
            .join()
            .on("click", (event) => updateMainVisualization(event.target.value, year));

        d3.select("#greetings-vis-option-button")
            .join()
            .on("click", (_) => {
                triggerDisplayStyle(
                    document.getElementById("greetings-vis-options-div"),
                    "none",
                    "block"
                )
            });

        var all_years = new Set([...csvData.map(d => d.date.getFullYear())]);
        all_years.add("Alle");

        d3.select("#greetings-vis-option-list").selectAll("button")
            .data(all_years)
            .join("button")
            .attr("type", "button")
            .attr("name", d => d)
            .attr("value", d => d)
            .attr("id", (_, i) => `menu-item-${i}`)
            .attr("class", "block px-4 py-2 text-sm text-gray-700")
            .attr("role", "menuitem")
            .attr("tabindex", -1)
            .on("click", event => updateMainVisualization(type, event.target.value))
            .html(d => d)

    };

    filterDataByYear = (year) => {
        var filteredData = csvData; // Reset to all data by default
        if (year != "Alle") {
            var r = [new Date(`${year}-01-01`), new Date(`${parseInt(year) + 1}-01-01`)]
            filteredData = d3.filter(csvData, d => (r[0] <= d.date && d.date < r[1]))
        }
        return filteredData;
    };

    sliceDataByTypeAndYear = (iType, iYear) => {
        type = iType;
        year = iYear;
        var filteredData = filterDataByYear(year)
        if (type == "gäste") {
            data = d3.rollups(filteredData, D => D.length, d => d["name"])
                .sort((a, b) => b[1] - a[1])
                .map(vals => { return { name: vals[0], count: vals[1] } })
                .slice(0, n);
        } else if (type == "genres") {
            data = d3.rollups(filteredData, D => D.length, d => d["genre"])
                .sort((a, b) => b[1] - a[1])
                .map(vals => { return { name: vals[0], count: vals[1] } })
                .slice(0, n);
        } else if (type == "parteien") {
            data = d3.rollups(
                filteredData.filter((d) => d["party"].length > 0), D => D.length, d => d["party"])
                .sort((a, b) => b[1] - a[1])
                .map(vals => { return { name: vals[0], count: vals[1] } })
                .slice(0, n);
        } else if (type == "medien") {
            data = d3.rollups(
                filteredData.filter((d) => d["pub_platform"].length > 0), D => D.length, d => d["pub_platform"])
                .sort((a, b) => b[1] - a[1])
                .map(vals => { return { name: vals[0], count: vals[1] } })
                .slice(0, n);
        }
        return data;
    };

    getContextString = (iType, iYear) => {
        return year == "Alle" ? `Top ${n} ${iType} über ${iYear} Jahre` : `Top ${n} ${iType} in ${iYear}`;
    };

    clickMainBarAction = (_, d) => {
        var start = x(data[0].name) - 10;
        var lineData = [[start, y(d.count)], [start - 7, y(d.count)]];
        helper
            .attr("d", line(lineData));
        helperText
            .text(d.count)
            .attr("x", start - 10)
            .attr("y", y(d.count) + 3);
    };

    const margins = { top: 25, right: 0, bottom: 50, left: 25 };
    const width = 900;
    const height = 500;
    const n = 16;
    const csvData = await loadData(dataPath);
    var year = "Alle";
    var type = "gäste"

    initializeButtons(targetId);

    var svg = d3.select(`div#${targetId}`)
        .append("svg")
        .attr("viewBox", [0, 0, width, height + margins.bottom])
        .attr("style", `max-width: ${width}px; height: auto; font: 10px sans-serif; overflow: visible;`);

    var x = d3.scaleBand()
        .range([margins.left, width - margins.right])
        .padding(0.2);
    var y = d3.scaleLinear()
        .range([height - margins.bottom, margins.top]);

    var gx = svg
        .append("g")
        .attr("id", "gx")
        .attr("transform", `translate(0,${height - margins.bottom})`);
    var gy = svg
        .append("g")
        .attr("id", "gy")
        .attr("transform", `translate(${margins.left},0)`);

    var helper = svg
        .append("path")
        .attr("id", "helper-greetings-path")
        .attr("stroke", defaultColors.highlight)
        .attr("stroke-width", 1.15);

    var helperText = svg
        .append("text")
        .attr("id", "helper-greetings-text")
        .attr("fill", defaultColors.highlight)
        .style("text-anchor", "end");

    applyFontConfig(helperText);

    var context = svg
        .append("g")
        .attr("id", "context-text")
        .attr("transform", `translate(${width / 2 - 120}, 40)`)
        .append("text");

    const line = d3.line()
        .x((d) => d[0])
        .y((d) => d[1]);

    updateMainVisualization = (iType, iYear) => {
        year = iYear;
        type = iType;
        var data = sliceDataByTypeAndYear(type, year)

        x.domain(data.map(d => d.name));
        y.domain([0, d3.max(data, d => d.count)]).nice();

        helper.attr("d", null);
        helperText.text(null);

        gx.transition()
            .duration(1000)
            .call(d3.axisBottom(x).tickSizeOuter(0))
            .call(g => g.selectAll(".tick").select("line").remove())
            .call(g => g.select(".domain").remove())
            .selectAll("text")
            .style("text-anchor", "end")
            .attr("transform", "rotate(-70)");

        applyFontConfig(gx, true);
        applyTextOffset(gx, "-0.5em", "-0.25em", true);

        gy.transition()
            .duration(1000)
            .call(d3.axisLeft(y))
            .call(g => g.select(".domain").remove());

        applyFontConfig(gy, true);

        context
            .transition()
            .duration(750)
            .attr("font-size", 20)
            .attr("font-weight", 400)
            .style("text-transform", "capitalize")
            .text(getContextString(type, year));

        var bar = svg.selectAll("rect")
            .data(data)

        bar
            .join("rect")
            .on("click", (e, d) => clickMainBarAction(e, d))
            .on("mouseover", function () { d3.select(this).attr("fill-opacity", 0.9) })
            .on("mouseout", function () { d3.select(this).attr("fill-opacity", 1.0) })
            .transition()
            .delay((_, i) => i * 100)
            .attr("x", d => x(d.name))
            .attr("y", d => y(d.count))
            .attr("rx", 3)
            .attr("fill", d => d.name in colors ? colors[d.name] : defaultColors.light)
            .attr("height", d => y(0) - y(d.count))
            .attr("width", x.bandwidth());

        bar
            .exit()
            .remove();

        context
            .exit()
            .remove();
    }

    updateMainVisualization(type, year)

}

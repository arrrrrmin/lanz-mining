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

getDate = (str) => {
    const tParser = d3.timeParse("%Y-%m-%d")
    return tParser(str.split('T')[0])
}

loadData = async (file) => {
    let csvData = await d3.csv(file).then(d => d);
    csvData = csvData.map(d => {
        d.date = getDate(d.date)
        return d
    });
    return csvData
}

triggerDisplayStyle = (element, from = "none", to = "block") => {
    if (element.style.display == from) {
        element.style.display = to;
    } else {
        element.style.display = from;
    }
}

applyFontConfig = (element, selectText = false) => {
    if (selectText) {
        element
            .selectAll("text")
            .attr("font-size", 16)
            .attr("font-weight", 400)
            .attr("fill", defaultColors.dark)
    } else {
        element
            .attr("font-size", 16)
            .attr("font-weight", 400)
            .attr("fill", defaultColors.dark)
    }
}

applyTextOffset = (element, x, y, selectText = false) => {
    if (selectText) {
        element
            .selectAll("text")
            .attr("dx", x)
            .attr("dy", y)
    } else {
        element
            .attr("dx", x)
            .attr("dy", y)
    }
}
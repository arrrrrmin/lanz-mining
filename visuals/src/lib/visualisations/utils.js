import * as d3 from "d3";


export const bg = "#EFE9DF";    // For paper aestetics

export const showKeyToColour = {
    "markuslanz": "#FBBF24",    //amber
    "maybritillner": "#FB7185", // rose
    "carenmiosga": "#10B981",   // emerald
    "maischberger": "#8B5CF6",  // violet
    "hartaberfair": "#06B6D4",  // cyan
};

export const mapShowNames = {
    "markuslanz": "Markus Lanz",
    "maybritillner": "Maybrit Illner",
    "carenmiosga": "Caren Miosga",
    "maischberger": "Maischberger",
    "hartaberfair": "Hart aber fair",
}

export const partyToColour = {
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

export const partyToInnerColor = {
    "SPD": "#0c0a09",
    "CDU": "#fff",
    "CSU": "#fff",
    "CDU/CSU": "#fff",
    "B90G": "#0c0a09",
    "FDP": "#0c0a09",
    "LINKE": "#0c0a09",
    "Parteilos": "#0c0a09",
    "AfD": "#0c0a09",
    "BSW": "#0c0a09",
    "Freie Wähler": "#0c0a09",
}

export const pairwiseCumsum = (_d) => {
    var values = d3.pairs([0, ...d3.cumsum(_d, (d) => d.values.length)]);
    return _d.map((d, i) => ({
        ...d,
        start: values[i][0],
        end: values[i][1],
    }));
};

export const dateContext = {
    full: new Date(2024, 1, 1),
    btw: new Date(2024, 10, 6),
};

export const setText = (elements, fontSize, fontWeight, textAnchor = undefined) => {
    elements
        .attr("font-size", fontSize)
        .attr("font-weight", fontWeight)
    textAnchor ? elements.attr("text-anchor", textAnchor) : elements.attr("text-anchor", "start")

    return elements
}

export const createSvg = (id, width, height, overflow = "visible") => {
    var svg = d3
        .select(`div#${id}`)
        .append("svg")
        .attr("viewBox", [0, 0, width, height])
        .attr("style", `max-width: ${width}px; overflow: ${overflow};`);
    return svg
}

export const uniformStart = (data, s = new Date(2024, 1, 1)) => {
    return data.filter((d) => d.date >= s);
}

export const normalizeParties = (partyStr) => {
    let result = partyStr;
    if (["CDU", "CSU"].includes(partyStr)) {
        result = "CDU/CSU";
    }
    return result;
};

export const getId = (id, ...suffixes) => {
    return `${id}-${suffixes.join("-")}`
}
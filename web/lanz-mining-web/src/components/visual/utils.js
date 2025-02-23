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

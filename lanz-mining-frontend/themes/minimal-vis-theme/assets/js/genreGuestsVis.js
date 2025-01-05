

genreGuestsVis = async () => {

    loadData = async () => {
        let csvData = await d3.csv("js/data.csv").then(d => d);
        return csvData
    }

    getDate = (str) => {
        const tParser = d3.timeParse("%Y-%m-%d")
        return tParser(str.split('T')[0])
    }

    transform = (inData) => {
        var datedData = inData.map(D => {
            D["date"] = getDate(D["date"])
            return D
        });
        var outData = d3.groups(datedData, D => D["genre"])
            .map(d => ({
                genre: d[0],
                series: d3.rollups(d[1], D => D.length, d => d["date"])
                    .sort((a, b) => b[0] - a[0])
                    .map(e => ({ date: e[0], value: e[1] }))
            }));
        return outData;
    }

    transform2 = (inData, y) => {
        var datedData = inData.map(D => {
            D["date"] = getDate(D["date"])
            return D
        });
        const timeRange = [new Date(`${y}-01-01`), new Date(`${y + 1}-01-01`)];
        var outData = datedData.filter(function (d) { return timeRange[0] <= d.date && d.date < timeRange[1] });
        return outData
    }

    const margins = { top: 25, right: 25, bottom: 25, left: 0 };
    const width = 700;
    const height = 500;
    const n = 10;
    const year = 2024;
    const csvData = await loadData();

    console.log(csvData);
    var data = transform2(csvData, year);
    console.log(data);
}

genreGuestsVis();
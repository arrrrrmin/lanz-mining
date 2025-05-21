<script>
    import { onMount } from "svelte";
    import * as utils from "./utils.js";
    import * as d3 from "d3";

    export const pairwiseCumsumPercentage = (_d, denom) => {
        var values = d3.pairs([
            0,
            ...d3.cumsum(_d, (d) => (d.values.length / denom) * 100),
        ]);
        return _d.map((d, i) => ({
            ...d,
            start: values[i][0],
            end: values[i][1],
            percentage: values[i][1] - values[i][0],
        }));
    };

    export const pairwiseCumsum = (_d) => {
        var values = d3.pairs([0, ...d3.cumsum(_d, (d) => d.count)]);
        return _d.map((d, i) => ({
            ...d,
            start: values[i][0],
            end: values[i][1],
        }));
    };

    let { data, id, formatOrder } = $props();

    // Fair data start for all talkshows
    // let start = utils.dateContext.full;
    // let end = undefined;
    let start = new Date(2024, 10, 6);
    let end = new Date(2025, 1, 23);

    const transformData = (originalData) => {
        let _data = originalData.filter((d) => d.date >= start);
        if (end) {
            _data = _data.filter((d) => d.date < end);
        }
        _data = _data.filter((d) => d.group == "Politik");
        _data = _data.map((d) => ({ ...d, party: utils.normalizeParties(d.party) }));
        _data = d3
            .rollups(
                _data,
                (D) => ({
                    talkshow: D[0].talkshow,
                    count: D.length,
                    parties: d3
                        .groups(D, (e) => e.party)
                        .map((E) => ({
                            party: E[0],
                            count: E[1].length,
                            values: E[1],
                            talkshow: E[1][0].talkshow,
                        })),
                }),
                (d) => d.talkshow,
            )
            .map((d) => d[1]);

        // Sort before cumsum!
        _data = _data.sort((a, b) => b.count - a.count);
        _data = _data.map((d) => ({
            talkshow: d.talkshow,
            count: d.count,
            parties: d.parties.sort((a, b) => b.count - a.count),
        }));

        _data = _data.map((d) => ({
            ...d,
            // parties: pairwiseCumsum(d.parties).map((d) => ({
            parties: pairwiseCumsumPercentage(d.parties, d.count).map((d) => ({
                party: d.party,
                count: d.count,
                start: d.start,
                end: d.end,
                talkshow: d.talkshow,
                percentage: d.percentage,
            })),
        }));

        return _data;
    };

    let _data = transformData(data.data);

    onMount(() => {
        const width = 1600;
        const height = 600;
        const gapSize = 4;
        const animDelay = 50;

        const svg = utils.createSvg(id, width, height, "visible");

        var x = d3.scaleLinear().range([0, width]).domain([0, 100]);
        var y = d3
            .scaleBand()
            .range([30, height])
            .domain(_data.map((d) => d.talkshow))
            .padding(0.35)
            .paddingOuter(0);

        const percentageLabel = (d) => {
            if (d.end - d.start < 3.5) {
                return "";
            }
            return `${Math.round(d.end - d.start)}%`;
        };

        const partyLabel = (d) => {
            if (d.end - d.start < 3.5) {
                return "";
            }
            if (d.party === "Freie Wähler") {
                d.party = "FW";
            }
            return d.party;
        };

        var showTitles = svg.append("g").attr("id", "party-dist-showlabels-g");

        const update = () => {
            var bars = svg
                .selectAll("g#party-dist-g")
                .data(_data)
                .join("g")
                .attr("id", "party-dist-g")
                .selectAll("rect#party-dist-g-rect")
                .data((d) => d.parties)
                .join("rect")
                .attr("id", "party-dist-g-rect")
                .attr("y", (d) => y(d.talkshow))
                .transition()
                .delay((_, i) => i * animDelay)
                .attr("x", (d) => x(d.start))
                .attr("rx", 8)
                .attr("fill", (d) => utils.partyToColour[d.party])
                .attr("fill-opacity", 0.9)
                .attr("stroke", (d) => utils.partyToColour[d.party])
                .attr("stroke-opacity", 0.9)
                .attr("stroke-width", 2)
                .attr("width", (d, i) => x(d.end - d.start) - gapSize)
                .attr("height", y.bandwidth());

            var barValues = svg
                .selectAll("g#party-dist-values-g")
                .data(_data)
                .join("g")
                .attr("id", "party-dist-values-g")
                .selectAll("text#party-dist-values-text")
                .data((d) => d.parties)
                .join("text")
                .attr("id", "party-dist-values-text")
                .attr("y", (d) => y(d.talkshow) + gapSize * 4)
                .transition()
                .delay((_, i) => i * animDelay)
                .attr("x", (d) => x(d.start) + gapSize / 2)
                .attr("fill", "white")
                .attr("text-anchor", "start")
                .text((d) => percentageLabel(d));

            utils.setText(barValues, 20, 600, "start");

            var barLabels = svg
                .selectAll("g#party-dist-labels")
                .data(_data)
                .join("g")
                .attr("id", "party-dist-labels")
                .selectAll("text#party-dist-labels-text")
                .data((d) => d.parties)
                .join("text")
                .attr("y", (d) => y(d.talkshow) + y.bandwidth() - gapSize)
                .transition()
                .delay((_, i) => i * animDelay)
                .attr("x", (d) => x(d.start) + gapSize / 2)
                .attr("fill", "white")
                .text((d) => partyLabel(d));

            utils.setText(barLabels, 20, 600, "start");

            showTitles
                .selectAll("text#party-dist-showlabels-g")
                .data(_data)
                .join("text")
                .attr("x", (d) => x(50))
                .attr("y", (d) => y(d.talkshow) - gapSize * 2)
                .text((d) => utils.mapShowNames[d.talkshow]);

            utils.setText(showTitles, 20, 600, "middle");
        };

        update();
    });
</script>

<div {id}></div>

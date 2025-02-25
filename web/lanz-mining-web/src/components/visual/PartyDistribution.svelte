<!-- PartyDistribution.svelte -->
<script>
    // Import necessary Svelte functions and D3 library
    import { onMount } from "svelte";
    import * as utils from "./utils.js";
    import * as d3 from "d3";

    const pairwiseCumsumPercentage = (_d, denom) => {
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

    let { data: data, formatOrder } = $props();

    // Fair data start for all talkshows
    let start = utils.dateContext.full;

    const changeTimeRange = (currentMinDate) => {
        if (currentMinDate === utils.dateContext.full) {
            start = utils.dateContext.btw;
        } else {
            start = utils.dateContext.full;
        }
    };
    const transformData = (originalData) => {
        let _data = originalData.filter((d) => d.date >= start);
        _data = _data.filter((d) => d.group == "Politik");
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
            parties: pairwiseCumsumPercentage(d.parties, d.count).map((d) =>
                // Remove values in d[n].parties[n].values
                ({
                    party: d.party,
                    count: d.count,
                    start: d.start,
                    end: d.end,
                    talkshow: d.talkshow,
                    percentage: d.percentage,
                }),
            ),
        }));
        _data = _data.sort(
            (a, b) => formatOrder[a.talkshow] - formatOrder[b.talkshow],
        );

        return _data;
    };

    let _data = transformData(data.data);

    onMount(() => {
        const width = 1200;
        const height = 600;
        const gapSize = 8;
        const animDelay = 50;

        var svg = d3
            .select("#talkshow-party-distribution")
            .append("svg")
            .attr("viewBox", [0, 0, width, height])
            .attr("style", `max-width: ${width}px; overflow: visible;`);

        var x = d3.scaleLinear().range([0, width]).domain([0, 100]);
        var y = d3
            .scaleBand()
            .range([70, height])
            .domain(_data.map((d) => d.talkshow))
            .padding(0.35)
            .paddingOuter(0);

        const percentageLabel = (d) => {
            if (d.end - d.start < 3.5) {
                return "";
            }
            return `${Math.round(d.end - d.start)}`;
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

        const findTitle = () => {
            if (start == utils.dateContext.full) {
                return "Parteien in ÖRR-Talkshows in 2024 (% je Format)";
            }
            return "Parteien in ÖRR-Talkshows in Nov. 24 bis Feb. 25 (% je Format)";
        };

        const findAlterButtonText = () => {
            if (start == utils.dateContext.full) {
                return "Seit Koalitionsbruch 👈";
            }
            return "Seit Februar 2024 👈";
        };

        var title = svg
            .append("g")
            .attr("id", "party-dist-title-g")
            .append("text")
            .attr("id", "party-dist-title-text")
            .attr("x", width / 2)
            .attr("y", 20)
            .attr("font-size", 24)
            .attr("font-weight", 600)
            .attr("text-anchor", "middle");

        var showTitles = svg.append("g").attr("id", "party-dist-showlabels-g");

        var alterButton = svg
            .append("g")
            .attr("id", "party-dist-alternate")
            .append("text")
            .attr("id", "party-dist-alternate-text")
            .attr("x", width)
            .attr("y", 20)
            .attr("fill", "gray")
            .attr("text-anchor", "end")
            .text(findAlterButtonText())
            .style("text-decoration", "underline")
            .on("mouseover", function (event) {
                d3.select("#party-dist-alternate-text").attr("fill", "black");
            })
            .on("mouseout", function (event) {
                d3.select("#party-dist-alternate-text").attr("fill", "gray");
            })
            .on("click", function (event) {
                changeTimeRange(start);
                _data = transformData(data.data);
                update();
            });

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
                .attr("y", (d) => y(d.talkshow) + gapSize * 2)
                .transition()
                .delay((_, i) => i * animDelay)
                .attr("x", (d) => x(d.start) + gapSize / 2)
                .attr("fill", "white")
                .attr("text-anchor", "start")
                .text((d) => percentageLabel(d));

            var barLabels = svg
                .selectAll("g#party-dist-labels")
                .data(_data)
                .join("g")
                .attr("id", "party-dist-labels")
                .selectAll("text#party-dist-labels-text")
                .data((d) => d.parties)
                .join("text")
                .attr("id", "party-dist-labels-text")
                .attr("y", (d) => y(d.talkshow) + y.bandwidth() - gapSize)
                .transition()
                .delay((_, i) => i * animDelay)
                .attr("x", (d) => x(d.start) + gapSize / 2)
                .attr("fill", "white")
                .attr("text-anchor", "start")
                .text((d) => partyLabel(d));

            showTitles
                .selectAll("text#party-dist-showlabels-g")
                .data(_data)
                .join("text")
                .attr("id", "party-dist-showlabels-g")
                .attr("x", (d) => x(50))
                .attr("y", (d) => y(d.talkshow) - gapSize * 2)
                .attr("font-weight", 600)
                .attr("text-anchor", "middle")
                .text((d) => utils.mapShowNames[d.talkshow]);

            title.text(findTitle());

            alterButton.text(findAlterButtonText());
        };

        update();
    });
</script>

<div id="talkshow-party-distribution" class="pt-8"></div>

<style></style>

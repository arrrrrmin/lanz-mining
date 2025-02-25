<!-- MainSpeakers.svelte -->
<script>
    // Import necessary Svelte functions and D3 library
    import { onMount } from "svelte";
    import * as utils from "./utils.js";
    import * as d3 from "d3";

    // Get props
    let { data: data, numGuests = $bindable(numGuests) } = $props();

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

        _data = d3
            .groups(_data, (d) => d.name)
            .map((d) => ({
                name: d[0],
                invites: d3
                    .groups(d[1], (d) => d.talkshow)
                    .map((d) => ({ talkshow: d[0], values: d[1] })),
            }));
        _data = _data.map((d) => ({
            name: d.name,
            invites: d.invites,
            total_invites: d3.sum(d.invites, (D) => D.values.length),
        }));
        // Sort befor cumulative sum!
        _data = _data
            .map((d) => ({
                ...d,
                invites: d.invites.sort(
                    (a, b) => b.values.length - a.values.length,
                ),
            }))
            .sort((a, b) => b.total_invites - a.total_invites);
        _data = _data.map((d) => ({
            ...d,
            invites: utils.pairwiseCumsum(d.invites),
        }));

        numGuests = _data.length;
        _data = _data.slice(0, 20);

        return _data;
    };

    let _data = transformData(data.data);

    onMount(() => {
        const width = 1200;
        const height = 1000;
        const gapSize = 8;
        const animDelay = 350;

        var x = d3
            .scaleLinear()
            .range([0, width])
            .domain([0, d3.max(_data, (d) => d.total_invites)]);

        var y = d3
            .scaleBand()
            .range([40, height])
            .padding(0.175)
            .paddingOuter(0.02)
            .domain(_data.map((d) => d.name));

        var svg = d3
            .select("#talkshow-main-speakers")
            .append("svg")
            .attr("viewBox", [0, 0, width, height])
            .attr("style", `max-width: ${width}px; overflow: visible;`);

        var title = svg
            .append("g")
            .attr("id", "main-speakers-title-g")
            .append("text")
            .attr("id", "main-speakers-title-text")
            .attr("x", width / 2)
            .attr("y", 20)
            .attr("font-size", 24)
            .attr("font-weight", 600)
            .attr("text-anchor", "middle");

        var nameGroups = svg.append("g").attr("id", "main-speakers-names-g");

        var legendRects = svg
            .append("g")
            .attr("id", "main-speakers-legend-g")
            .selectAll("rect")
            .data(Object.keys(utils.showKeyToColour))
            .join("rect")
            .attr("x", (d, i) => width - y.bandwidth())
            .attr("y", (d, i) => y(_data[_data.length - 1 - i].name))
            .attr("rx", 4)
            .attr("width", y.bandwidth())
            .attr("height", y.bandwidth())
            .attr("fill", "none")
            .attr("stroke", (d) => utils.showKeyToColour[d])
            .attr("stroke-width", 2);

        var legendTexts = svg
            .select("g#main-speakers-legend-g")
            .selectAll("text")
            .data(Object.keys(utils.mapShowNames))
            .join("text")
            .attr("x", (d, i) => width - y.bandwidth() - gapSize)
            .attr(
                "y",
                (d, i) =>
                    y(_data[_data.length - 1 - i].name) + y.bandwidth() / 2 + 5,
            )
            .attr("text-anchor", "end")
            .text((d) => utils.mapShowNames[d]);

        const findTitle = () => {
            if (start == utils.dateContext.full) {
                return "Auftritte Talkender der ÖR-Talkshows in 2024";
            }
            return "Auftritte Talkender der ÖR-Talkshows von Nov. 24 bis Feb. 25 (% je Format)";
        };

        const findAlterButtonText = () => {
            if (start == utils.dateContext.full) {
                return "Seit Koalitionsbruch 👈";
            }
            return "Seit Februar 2024 👈";
        };

        var alterButton = svg
            .append("g")
            .attr("id", "party-distribution-alternate")
            .append("text")
            .attr("id", "party-distribution-alternate-text")
            .attr("x", width)
            .attr("y", 20)
            .attr("fill", "gray")
            .attr("text-anchor", "end")
            .text(findAlterButtonText())
            .style("text-decoration", "underline")
            .on("mouseover", function (event) {
                d3.select("#party-distribution-alternate-text").attr(
                    "fill",
                    "black",
                );
            })
            .on("mouseout", function (event) {
                d3.select("#party-distribution-alternate-text").attr(
                    "fill",
                    "gray",
                );
            })
            .on("click", function (event) {
                changeTimeRange(start);
                _data = transformData(data.data);
                update();
            });

        const update = () => {
            x.domain([0, d3.max(_data, (d) => d.total_invites)]);
            y.domain(_data.map((d) => d.name));
            var barGroups = svg
                .selectAll("g#main-speakers-bars-g")
                .data(_data)
                .join("g")
                .attr("id", "main-speakers-bars-g")
                .attr("transform", (d) => `translate(0,${y(d.name)})`);

            var bars = barGroups
                .selectAll("rect#main-speakers-rect")
                .data((d) => d.invites)
                .join("rect") // per bar in series
                .attr("id", "main-speakers-rect")
                .transition()
                .delay((_, i) => i * animDelay)
                .attr("x", (d) => x(d.start))
                .attr("y", 0)
                .attr("fill-opacity", 0)
                .attr("stroke", (d) => utils.showKeyToColour[d.talkshow])
                .attr("stroke-width", 2)
                .attr("rx", 4)
                .attr("width", (d) => x(d.end - d.start) - gapSize)
                .attr("height", y.bandwidth());

            var nameLabels = nameGroups
                .selectAll("text#main-speakers-names-g-text")
                .data(_data)
                .join("text")
                .attr("id", "main-speakers-names-g-text")
                .attr("x", (d) => x(d.invites[0].start) + gapSize * 1.75)
                .attr("y", (d) => y(d.name) + y.bandwidth() / 2 + 5)
                .text((d) => d.name);

            var barValues = barGroups
                .selectAll("text#main-speakers-values-text")
                .data((d) => d.invites)
                .join("text")
                .attr("id", "main-speakers-values-text")
                .transition()
                .delay((_, i) => i * animDelay)
                .attr("x", (d) => x(d.end) - gapSize * 2)
                .attr("y", y.bandwidth() / 2 + 5)
                .attr("text-anchor", "end")
                .text((d) => `${d.end - d.start}`);

            var partyBadge = nameGroups
                .selectAll("circle#main-speakers-party-circle")
                .data(
                    _data.filter(
                        (d) => d.invites[0].values[0].party.length > 0,
                    ),
                )
                .join("circle")
                .attr("id", "main-speakers-party-circle")
                .transition()
                .delay((_, i) => animDelay)
                .attr("cx", (d) => x(d.invites[0].start) + gapSize)
                .attr("cy", (d) => y(d.name) + gapSize + 2)
                .attr("r", 3)
                .attr("fill-opacity", 0)
                .attr(
                    "stroke",
                    (d) => utils.partyToColour[d.invites[0].values[0].party],
                )
                .attr("stroke-width", 2);

            alterButton.text(findAlterButtonText());
            title.text(findTitle());
        };

        update();
    });
</script>

<!-- Container for the chart -->
<div id="talkshow-main-speakers" class="pt-8"></div>

<style></style>

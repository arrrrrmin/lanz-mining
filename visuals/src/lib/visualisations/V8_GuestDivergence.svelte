<script>
    import { onMount } from "svelte";
    import * as utils from "./utils.js";
    import * as d3 from "d3";

    let { data, id } = $props();

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
        if (start === utils.dateContext.btw) {
            _data = _data.filter((d) => d.date <= new Date(2025, 1, 23));
        }
        _data = _data.filter((d) => d.group.length > 0);

        const tSizesArr = d3
            .groups(_data, (d) => d.talkshow)
            .map((D) => ({ talkshow: D[0], size: D[1].length }));

        const leftDenominator = _data.filter((d) =>
            ["maischberger", "carenmiosga", "hartaberfair"].includes(
                d.talkshow,
            ),
        ).length;
        const rightDenominator = _data.filter((d) =>
            ["markuslanz", "maybritillner"].includes(d.talkshow),
        ).length;
        const ardzdfCounts = {
            left: leftDenominator,
            right: rightDenominator,
        };

        const tSizes = {
            maischberger: leftDenominator,
            carenmiosga: leftDenominator,
            hartaberfair: leftDenominator,
            markuslanz: rightDenominator,
            maybritillner: rightDenominator,
        };

        const splitLeftRight = (d) => {
            let result = { left: [], right: [] };
            d.forEach((D) => {
                if (
                    ["maischberger", "carenmiosga", "hartaberfair"].includes(
                        D.talkshow,
                    )
                ) {
                    result.left.push({ ...D, percentage: -D.percentage });
                } else {
                    result.right.push({ ...D, percentage: D.percentage });
                }
            });
            return result;
        };

        _data = d3
            .rollups(
                _data,
                (D) =>
                    d3
                        .groups(D, (e) => e.talkshow)
                        .map((E) => ({
                            talkshow: E[0],
                            percentage: E[1].length / tSizes[E[0]],
                            values: E[1],
                        })),
                (d) => d.group,
            )
            .map((d) => ({ group: d[0], ...splitLeftRight(d[1]) }));

        const sortCriteria = {
            markuslanz: 1,
            maybritillner: 2,
            carenmiosga: 5,
            maischberger: 4,
            hartaberfair: 3,
        };

        const sumLeftRight = (d) => {
            return (
                -1 * d3.sum(d.left.map((D) => D.percentage)) +
                d3.sum(d.right.map((D) => D.percentage))
            );
        };
        const sortInnerLeftRight = (d, descending) => {
            if (descending) {
                return d.sort(
                    (a, b) =>
                        sortCriteria[b.talkshow] - sortCriteria[a.talkshow],
                );
            }
            return d.sort(
                (a, b) => sortCriteria[a.talkshow] - sortCriteria[b.talkshow],
            );
        };
        _data = _data.sort((a, b) => sumLeftRight(b) - sumLeftRight(a));
        _data = _data.map((d) => ({
            ...d,
            left: sortInnerLeftRight(d.left, false),
            right: sortInnerLeftRight(d.right, false),
        }));

        const getStartEnd = (d) => {
            var values = d3.pairs([0, ...d3.cumsum(d, (D) => D.percentage)]);
            return d.map((d, i) => ({
                ...d,
                start: values[i][0],
                end: values[i][1],
            }));
        };

        _data = _data.map((d) => ({
            ...d,
            left: getStartEnd(d.left),
            right: getStartEnd(d.right),
        }));

        // return _data;
        return _data.slice(2);
    };

    let _data = transformData(data.data);
    let allGroups = _data.map((d) => d.group);
    let xMin = d3.min(
        _data.filter((d) => d.left.length > 0),
        (d) => d.left[d.left.length - 1].end,
    );
    let xMax = d3.max(
        _data.filter((d) => d.right.length > 0),
        (d) => d.right[d.right.length - 1].end,
    );
    let outerBound = d3.max([xMin, xMax], (d) => Math.abs(d));

    onMount(() => {
        const width = 1400;
        const height = 950;
        const gapSize = 5;
        const margins = { bottom: 40 };
        const animDelay = 75;
        const headRoom = 65;
        const minPerc = _data.length == 16 ? 1.7: 0.25; // 0.25; // 0.5;

        var x = d3
            .scaleLinear()
            .range([100, width - 50])
            .domain([-outerBound, outerBound]);
        var y = d3
            .scaleBand()
            .range([headRoom, height])
            .padding(0.175)
            .paddingOuter(0.02)
            .domain(allGroups);

        var svg = utils.createSvg(id, width, height, "visible");

        const getValueLabel = (d, minPercentage = minPerc) => {
            var result = Number.parseFloat(
                Math.abs(d.percentage) * 100,
            ).toFixed(1);
            if (result < minPercentage) {
                result = "";
            }
            return result;
        };

        var nameGroups = svg.append("g").attr("id", "groups-diverging-names-g");

        var formats = svg.append("g").attr("id", "groups-diverging-formats-g");

        const findTitle = () => {
            if (start == utils.dateContext.full) {
                return "Branchen der Talkenden, pro Show und Sender in 2024";
            }
            return "Branchen der Talkenden, pro Show und Sender (Nov. 24 bis Feb. 25)";
        };

        const findAlterButtonText = () => {
            if (start == utils.dateContext.full) {
                return "Seit Koalitionsbruch 👈";
            }
            return "Seit Februar 2024 👈";
        };

        var legendRects = svg
            .append("g")
            .attr("id", "main-speakers-legend-g")
            .selectAll("rect")
            .data(Object.keys(utils.showKeyToColour))
            .join("rect")
            .attr("x", (d, i) => width - y.bandwidth())
            .attr("y", (d, i) => y(_data[_data.length - 2 - i].group))
            .attr("rx", 4)
            .attr("width", y.bandwidth())
            .attr("height", y.bandwidth())
            .attr("fill", (d) => utils.showKeyToColour[d])
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
                    y(_data[_data.length - 2 - i].group) +
                    y.bandwidth() / 2 +
                    5,
            )
            .attr("text-anchor", "end")
            .text((d) => utils.mapShowNames[d]);

        utils.setText(legendTexts, 20, 500, "end");

        var gx = svg
            .append("g")
            .attr("id", "groups-diverging-axis-g")
            .attr("transform", `translate(0,${headRoom})`)
            .call(
                d3
                    .axisTop(x)
                    .tickFormat((d) => Math.round(Math.abs(d) * 100) + "%"),
            )
            .call((g) => g.select(".domain").remove())
            .call((g) =>
                utils
                    .setText(g.selectAll(".tick text"), 20, 500, "middle")
                    .attr("x", 5),
            );

        var alterButton = svg
            .append("g")
            .attr("id", "groups-diverging-alternate")
            .append("text")
            .attr("id", "groups-diverging-alternate-text")
            .attr("x", width)
            .attr("y", 20)
            .attr("fill", "gray")
            .attr("text-anchor", "end")
            .text("Seit Koalitionsbruch")
            .style("text-decoration", "underline")
            .on("mouseover", function (event) {
                d3.select("text#groups-diverging-alternate-text").attr(
                    "fill",
                    "black",
                );
            })
            .on("mouseout", function (event) {
                d3.select("text#groups-diverging-alternate-text").attr(
                    "fill",
                    "gray",
                );
            })
            .on("click", function (event) {
                changeTimeRange(start);
                _data = transformData(data.data);
                outerBound = d3.max([xMin, xMax], (d) => Math.abs(d));
                xMin = d3.min(
                    _data.filter((d) => d.left.length > 0),
                    (d) => d.left[d.left.length - 1].end,
                );
                xMax = d3.max(
                    _data.filter((d) => d.right.length > 0),
                    (d) => d.right[d.right.length - 1].end,
                );
                update();
            });

        const update = () => {
            var barGroups = svg
                .selectAll("g#groups-diverging-g")
                .data(_data)
                .join("g")
                .attr("id", (_, i) => `groups-diverging-g`)
                .attr("transform", (d) => `translate(0,${y(d.group)})`);

            var barsRight = barGroups
                .selectAll("rect#rect-right")
                .data((d) => d.right)
                .join("rect") // per bar in series
                .attr("id", "rect-right")
                .transition()
                .delay((_, i) => i * animDelay)
                .attr("x", (d, i) => x(d.start) + i * gapSize + 2)
                .attr("y", 0)
                .attr("fill", (d) => utils.showKeyToColour[d.talkshow])
                .attr("stroke-width", 2)
                .attr("rx", 4)
                .attr("width", (d) => x(d.end) - x(d.start))
                .attr("height", y.bandwidth());

            var barLabelsRight = barGroups
                .selectAll("text#right-bar-label-text")
                .data((d) => d.right)
                .join("text")
                .attr("id", "right-bar-label-text")
                .transition()
                .delay((_, i) => i * animDelay)
                .attr("x", (d, i) => x(d.end) + i * gapSize)
                .attr("y", y.bandwidth() - gapSize)
                .text((d) => getValueLabel(d));

            utils.setText(barLabelsRight, 18, 500, "end");

            // Todo add a tooltip per rect to hint more contextual information
            var barsLeft = barGroups
                .selectAll("rect#rect-left")
                .data((d) => d.left)
                .join("rect") // per bar in series
                .attr("id", "rect-left")
                .transition()
                .delay((_, i) => i * animDelay)
                .attr("x", (d, i) => x(d.end) - i * gapSize - 2)
                .attr("y", 0)
                .attr("fill", (d) => utils.showKeyToColour[d.talkshow])
                .attr("rx", 4)
                .attr("width", (d) => x(d.start) - x(d.end))
                .attr("height", y.bandwidth());

            var barLabelsLeft = barGroups
                .selectAll("text#left-bar-label-text")
                .data((d) => d.left)
                .join("text")
                .attr("id", "left-bar-label-text")
                .transition()
                .delay((_, i) => i * animDelay)
                .attr("x", (d, i) => x(d.end) - +i * gapSize)
                .attr("y", y.bandwidth() - gapSize)
                .text((d) => getValueLabel(d));

            utils.setText(barLabelsLeft, 18, 500, "start");

            nameGroups
                .selectAll("text#groups-diverging-name-text")
                .data(_data)
                .join("text")
                .attr("id", (_, i) => "groups-diverging-name-text")
                .attr("x", (d) => {
                    if (d.left.length > 0) {
                        return x(d.left[d.left.length - 1].end) - 20;
                    } else {
                        return x(0) - 20;
                    }
                })
                .attr("y", (d) => y(d.group) + y.bandwidth() / 1.75)
                .attr("text-anchor", "end")
                .text((d) => d.group);

            utils.setText(nameGroups.selectAll("text"), 24, 500, "end");

            formats
                .selectAll("text")
                .data([
                    { format: "ARD", x: width * 0.25 },
                    { format: "ZDF", x: width * 0.75 },
                ])
                .join("text")
                .attr("id", `groups-diverging-format-texts`)
                .attr("x", (d) => d.x)
                .attr("y", height * 0.5)
                .attr("font-size", 30)
                .attr("font-weight", 600)
                .attr("text-anchor", "middle")
                .text((d, i) => d.format);

            alterButton.text(findAlterButtonText());
        };
        update();
    });
</script>

<!-- Container for the chart -->
<div {id} class="pt-8"></div>

<style></style>

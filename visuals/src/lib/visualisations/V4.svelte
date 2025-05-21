<script>
    import { onMount } from "svelte";
    import * as utils from "./utils.js";
    import * as d3 from "d3";

    let { data } = $props();

    let start = utils.dateContext.full;

    d3.selection.prototype.first = function () {
        return d3.select(this._groups[0][0]);
    };
    d3.selection.prototype.last = function () {
        var last = this.size() - 1;
        return d3.select(this._groups[0][last]);
    };

    export const pairwiseCumsum = (_d, sumVal) => {
        var values = d3.pairs([0, ...d3.cumsum(_d, (d) => d[sumVal])]);
        return _d.map((d, i) => {
            var resultObj = { ...d };
            resultObj[`${sumVal}_start`] = values[i][0];
            resultObj[`${sumVal}_end`] = values[i][1];
            return resultObj;
        });
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
            .sort((a, b) => a.total_invites - b.total_invites);
        _data = _data.map((d) => ({
            ...d,
            invites: utils.pairwiseCumsum(d.invites),
        }));

        var dataBinned = d3
            .groups(_data, (d) => d.total_invites)
            .map((D) => ({ freq: D[0], size: D[1].length, values: D[1] }));
        dataBinned = {
            allAppears: d3.sum(dataBinned, (d) => d.freq * d.size),
            allGuests: d3.sum(dataBinned, (d) => d.size),
            bins: dataBinned,
        };
        dataBinned.bins = dataBinned.bins.map((d) => ({
            ...d,
            percAppears: ((d.freq * d.size) / dataBinned.allAppears) * 100,
            percGuests: (d.size / dataBinned.allGuests) * 100,
        }));
        dataBinned.bins = pairwiseCumsum(dataBinned.bins, "percAppears");
        dataBinned.bins = pairwiseCumsum(dataBinned.bins, "percGuests");

        return dataBinned;
    };

    var _data = transformData(data.data);

    onMount(() => {
        const width = 1600;
        const height = 250;
        const gapSize = 8;
        const margins = { top: 50, bottom: 50 };
        const animDelay = 50;

        var allFreq = _data.bins.map((d) => d.freq);
        var allSizes = _data.bins.map((d) => d.size);

        var y = d3
            .scaleBand()
            .range([margins.top, height - margins.bottom])
            .domain([0])
            .padding(0.35)
            .paddingOuter(0);

        var x = d3.scaleLinear().range([0, width]).domain([0, 100]);

        const svg1 = utils.createSvg(
            "talkshow-freq-compare-1",
            width,
            height,
            "visible",
        );

        const labelsRect1g = svg1
            .append("g")
            .attr("id", "freq-compare-labels-rect1");

        const gx1 = svg1
            .append("g")
            .attr("id", "freq-compare-axis-g")
            .attr("transform", `translate(0,70)`)
            .call(d3.axisTop(x).tickFormat((d) => `${d}%`))
            .call((g) => g.select(".domain").remove())
            .call((g) =>
                utils
                    .setText(g.selectAll(".tick text"), 22, 600, "middel")
                    .attr("x", 4),
            )
            .call((g) =>
                g.selectAll(".tick text").first().attr("text-anchor", "start"),
            )
            .call((g) =>
                g.selectAll(".tick text").last().attr("text-anchor", "end"),
            );

        const helper1 = svg1.append("g").attr("id", "freq-compare-helper1");

        const svg2 = utils.createSvg(
            "talkshow-freq-compare-2",
            width,
            height,
            "visible",
        );
        const gx2 = svg2
            .append("g")
            .attr("id", "freq-compare-axis-g")
            .attr("transform", `translate(0,70)`)
            .call(d3.axisTop(x).tickFormat((d) => `${d}%`))
            .call((g) => g.select(".domain").remove())
            .call((g) =>
                utils
                    .setText(g.selectAll(".tick text"), 18, 600, "middel")
                    .attr("x", 4),
            )
            .call((g) =>
                g.selectAll(".tick text").first().attr("text-anchor", "start"),
            )
            .call((g) =>
                g.selectAll(".tick text").last().attr("text-anchor", "end"),
            );

        const labelsRect2g = svg2
            .append("g")
            .attr("id", "freq-compare-labels-rect2");

        const helper2 = svg2.append("g").attr("id", "freq-compare-helper2");

        const lineDataFnGuests = (dataPoint, targetVal) => {
            return [
                [
                    [
                        x(dataPoint.percGuests_end),
                        height / 2 + y.bandwidth() / 2 + 5,
                    ],
                    [x(dataPoint.percGuests_end), height - 20],
                ],
                [
                    [x(dataPoint.percGuests_end), height - 20],
                    [0, height - 20],
                ],
            ];
        };

        const lineDataFnAppears = (dataPoint, targetVal) => {
            return [
                [
                    [
                        x(dataPoint.percAppears_end),
                        height / 2 + y.bandwidth() / 2 + 5,
                    ],
                    [x(dataPoint.percAppears_end), height - 20],
                ],
                [
                    [x(dataPoint.percAppears_end), height - 20],
                    [width, height - 20],
                ],
            ];
        };

        const contextColors = {
            light: "#A3A3A3",
            dark: "#171717",
        };

        const update = () => {
            var rects1 = svg1
                .selectAll("rect")
                .data(_data.bins)
                .join("rect")
                .attr("id", (_, i) => `freq-compare-g-rect-${i}`)
                .attr("x", (d, i) => x(d.percGuests_start))
                .transition()
                .delay((_, i) => i * animDelay)
                .attr("y", y(0))
                .attr("width", (d) => x(d.percGuests_end - d.percGuests_start))
                .attr("height", (d) => y.bandwidth())
                .attr("fill-opacity", 0)
                .attr("stroke", (d) =>
                    d.freq <= 3 ? contextColors.light : contextColors.dark,
                )
                .attr("stroke-width", 2)
                .attr("rx", 4);

            var rects2 = svg2
                .selectAll("rect")
                .data(_data.bins)
                .join("rect")
                .attr("id", (_, i) => `freq-compare-g-rect-${i}`)
                .attr("x", (d) => x(d.percAppears_start))
                .transition()
                .delay((_, i) => i * animDelay)
                .attr("y", (d) => y(0))
                .attr("width", (d, i) =>
                    x(d.percAppears_end - d.percAppears_start),
                )
                .attr("height", (d) => y.bandwidth())
                .attr("fill-opacity", 0)
                .attr("stroke", (d) =>
                    d.freq <= 3 ? contextColors.light : contextColors.dark,
                )
                .attr("stroke-width", 2)
                .attr("rx", 4);

            var filteredData1 = _data.bins.filter((d) => d.freq <= 3);
            var lt = filteredData1[filteredData1.length - 1];

            const line = d3
                .line()
                .x((d) => d[0])
                .y((d) => d[1]);

            var lineData1 = lineDataFnGuests(lt);

            helper1
                .selectAll("path")
                .data(lineData1)
                .join("path")
                .attr("d", (d) => line(d))
                .attr("stroke", contextColors.light)
                .attr("stroke-width", 4)
                .style("stroke-dasharray", "3 5");

            helper1
                .append("text")
                .attr("x", lineData1[lineData1.length - 1][1][0])
                .attr("y", lineData1[lineData1.length - 1][1][1] - 5)
                .text(
                    `${Math.round(lt.percGuests_end)}% der Talkenden hatten ${lt.freq} oder weniger Auftritte`,
                );

            utils.setText(helper1.selectAll("text"), 24, 600, "start");

            var filteredData2 = _data.bins.filter((d) => d.freq > 3);
            var lineData2 = lineDataFnAppears(lt);
            helper2
                .selectAll("path")
                .data(lineData2)
                .join("path")
                .attr("d", (d) => line(d))
                .attr("stroke", contextColors.dark)
                .attr("stroke-width", 4)
                .style("stroke-dasharray", "3 5");

            helper2
                .append("text")
                .attr("x", lineData2[lineData2.length - 1][1][0])
                .attr("y", lineData2[lineData2.length - 1][1][1] - 5)
                .text(
                    `${100 - Math.round(lt.percGuests_end)}% der Talkenden absolvieren ${Math.round(100 - filteredData2[0].percAppears_start)}% der Auftritte`,
                );

            utils.setText(helper2.selectAll("text"), 20, 600, "end");

            var labelsRect1 = labelsRect1g
                .selectAll("text")
                .data(filteredData1)
                .join("text")
                .attr("x", (d) => x(d.percGuests_start) + gapSize / 2)
                .attr("y", (d) => y(0) + gapSize * 2.5)
                .attr("fill", contextColors.light)
                .text((d) => d.freq);

            utils.setText(labelsRect1, 20, 600, "start");

            var labelsRect2 = labelsRect2g
                .selectAll("text")
                .data(filteredData2)
                .join("text")
                .attr("x", (d) => x(d.percAppears_start) + gapSize / 2)
                .attr("y", (d) => y(0) + gapSize * 2.5)
                .attr("text-anchor", "start")
                .text((d) => d.freq);
        };

        update();
    });
</script>

<div id="talkshow-freq-compare-1" class="pt-8"></div>
<div id="talkshow-freq-compare-2" class="pt-8"></div>

<style></style>

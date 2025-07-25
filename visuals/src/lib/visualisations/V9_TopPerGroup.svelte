<script>
    import { onMount } from "svelte";
    import * as utils from "./utils.js";
    import * as d3 from "d3";

    let { data, id, groupOrder = $bindable(groupOrder) } = $props();
    let start = utils.dateContext.full;

    const sortGuests = (a, b) => {
        if (a.values.length != b.values.length) {
            return a.values.length - b.values.length;
        } else {
            return b.name.localeCompare(a.name);
        }
    };

    const transformData = (originalData) => {
        let _data = originalData.filter(
            (d) => d.date >= start && d.group != "",
        );

        let _groups = d3
            .groups(_data, (d) => d.group)
            .map((D) => ({
                name: D[0],
                values: d3
                    .groups(D[1], (e) => e.name)
                    .map((E) => ({ name: E[0], values: E[1] }))
                    .sort(sortGuests),
            }));

        _groups = _groups.map((d) => ({
            ...d,
            values: utils
                .pairwiseCumsum(d.values)
                .map((D) => ({ ...D, size: D.end - D.start })),
        }));
        _groups = _groups
            .map((d) => ({
                ...d,
                size: d3.sum(d.values, (e) => e.size),
            }))
            .sort((a, b) => b.size - a.size);

        return _groups.slice(2);
    };

    let _data = transformData(data.data);

    // Define the found order of groups, by frequency
    new Array(...new Set(_data.map((d) => d.name))).forEach((grp, i) => {
        groupOrder[grp] = _data.findIndex((d) => d.name === grp);
    });

    const maxAppearences = d3.max(_data, (d) => d.size);

    const mostInvitedGuests = _data.map((d) => ({
        ...d,
        winners: d.values
            .filter((D) =>
                D.size > 1 ? D.size === d3.max(d.values, (e) => e.size) : false,
            )
            .slice(-3),
    }));

    onMount(() => {
        const width = 1500;
        const height = 950;
        const margins = { left: 210, top: 0, right: 200, bottom: 30 };

        const x = d3
            .scaleLinear()
            .range([0 + margins.left, width - margins.right])
            .domain([0, maxAppearences]);
        const y = d3
            .scaleBand()
            .range([margins.top, height - margins.bottom])
            .padding(0.05)
            .paddingOuter(0.001)
            .domain(_data.map((d) => d.name));

        const svg = utils.createSvg(id, width, height, "hidden");

        var gx = svg
            .append("g")
            .attr("id", "x-axis")
            .attr("transform", `translate(0, ${height - margins.bottom})`)
            .call(d3.axisBottom(x))
            .call((g) => g.select(".domain").remove())
            .call((g) =>
                utils.setText(g.selectAll(".tick text"), 20, 500, "middle"),
            );

        var gxLabel = gx
            .append("text")
            .attr("y", -2)
            .attr("x", x(100))
            .attr("fill", "black")
            .text("Anzahl der Auftritte");

        utils.setText(gxLabel, 18, 400, "start");

        var rects = svg
            .append("g")
            .attr("id", "rect-container")
            .selectAll("g#rect-sequence")
            .data(_data)
            .join((enter) => {
                let rects = enter
                    .append("g")
                    .attr("transform", (d) => `translate(0, ${y(d.name)})`)
                    .selectAll("rect")
                    .data((d, i) => d.values.map((D) => ({ ...D, id: i })))
                    .join("rect")
                    .attr("x", (d) => x(d.start))
                    .attr("y", (d) => y(d.name))
                    .attr("height", y.bandwidth())
                    .attr("width", (d) => x(d.end) - x(d.start))
                    .attr("stroke", "white")
                    .attr("rx", 3)
                    .attr("fill", (d) =>
                        mostInvitedGuests[d.id].winners
                            .map((d) => d.name)
                            .includes(d.name)
                            ? "#ef4444"
                            : "#a8a29e",
                    );
            });

        var guests = svg
            .append("g")
            .attr("id", "g-guests-container")
            .selectAll("text#guest-labeltext")
            .data(
                mostInvitedGuests.map((d) => ({
                    ...d,
                    winners: d.winners.map((D) => ({
                        ...D,
                        //start: d.winners[d.winners.length - 1].start,
                        alignEnd: d.winners[d.winners.length - 1].end,
                        parentLength: d.winners.length,
                    })),
                })),
            )
            .join((enter) => {
                const findY = (d, i) => {
                    return d.parentLength > 1
                        ? (d.parentLength - i) * 20
                        : y.bandwidth() / 2 + 2;
                };

                const findX = (d, i) => {
                    return x(d.alignEnd) + i * 75 + 20;
                };

                var g = enter
                    .append("g")
                    .attr("id", "group-winner-labels")
                    .attr("transform", (d) => `translate(0, ${y(d.name)})`);

                g.selectAll("text#guest-labeltext")
                    .data((d) => d.winners)
                    .join("text")
                    .attr("id", "guest-labeltext")
                    .attr("x", findX)
                    .attr("y", findY)
                    .text((d) => d.name);

                utils.setText(enter.selectAll("text"), 20, 500, "start");

                let drawer = d3
                    .line()
                    .x((d) => d[0])
                    .y((d) => d[1]);

                g.selectAll("path")
                    .data((d) => d.winners)
                    .join("path")
                    .attr("stroke", "#000")
                    .attr("stroke-width", 2)
                    .attr("stroke-dasharray", 4)
                    .attr("d", (d, i) =>
                        drawer([
                            [
                                x(d.start) + (x(d.end) - x(d.start)) / 2,
                                findY(d, i) - 8,
                            ],
                            [findX(d, i), findY(d, i) - 8],
                        ]),
                    );

                g.selectAll("circle")
                    .data((d) => d.winners)
                    .join("circle")
                    .attr("cx", (d) => x(d.start) + (x(d.end) - x(d.start)) / 2)
                    .attr("cy", (d, i) => findY(d, i) - 8)
                    .attr("r", 3);
            });

        var labels = svg
            .append("g")
            .attr("id", "label-container")
            .selectAll("text")
            .data(_data)
            .join("text")
            .attr("id", "y-label")
            .attr("x", (d) => margins.left - 10)
            .attr("y", (d) => y(d.name) + y.bandwidth() / 2 + 2)
            .text((d) => d.name);

        utils.setText(d3.selectAll("text#y-label"), 20, 500, "end");
    });
</script>

<div {id} class="pt-8"></div>

<script>
    import { onMount } from "svelte";
    import * as utils from "$lib/visualisations/utils.js";
    import * as d3 from "d3";

    let { data, id } = $props();

    let formatOrder = {
        markuslanz: 0,
        maischberger: 1,
        maybritillner: 2,
        carenmiosga: 3,
        hartaberfair: 4,
    };

    let start = utils.dateContext.full;
    let current = $state(0);
    let n = 20;
    let forward = true;

    const transformData = (originalData, n) => {
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
                invites: d.invites
                    .sort(
                        (a, b) =>
                            formatOrder[a.talkshow] - formatOrder[b.talkshow],
                    )
                    .sort((a, b) => b.values.length - a.values.length),
            }))
            .sort((a, b) => b.total_invites - a.total_invites);
        _data = _data.map((d) => ({
            ...d,
            invites: utils.pairwiseCumsum(d.invites),
        }));

        return _data;
    };

    let dataMain = transformData(data.data, n);
    let _data = dataMain.slice(0, n);

    /** When mounting this component! */
    onMount(() => {
        function arrowfn(event) {
            if (
                event.currentTarget.value === "forward" &&
                current + n < dataMain.length
            ) {
                current += n;
                forward = true;
            }
            if (event.currentTarget.value === "backward" && current - n >= 0) {
                current -= n;
                forward = false;
            }
            _data = dataMain.slice(current, current + n);
            update();
        }

        /** Apply button function to buttons */
        d3.select(`button#${id}-forward`).on("click", arrowfn);
        d3.select(`button#${id}-backward`).on("click", arrowfn);

        /** Ok, now we can go on with the standard stuff */
        const width = 1200;
        const height = n * 45;
        const gapSize = 6;
        const transitSpeed = 100;
        const margins = { top: 10 };

        var x = d3
            .scaleLinear()
            .range([1, width])
            .domain([0, d3.max(_data, (d) => d.total_invites)]);

        var y = d3
            .scaleBand()
            .range([margins.top, height])
            .padding(0.175)
            .paddingOuter(0.02)
            .domain(_data.map((d) => d.name));

        const svg = utils.createSvg(id, width, height, "visible");

        // Build a legend
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
            .attr("fill", (d) => utils.showKeyToColour[d]);

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
            .text((d) => utils.mapShowNames[d]);

        utils.setText(legendTexts, 22, 500, "end");

        const textAlign = (d) => {
            return x(d.invites[0].start) + gapSize * 1.75;
        };
        const update = () => {
            y.domain(_data.map((d) => d.name));

            var barGroups = svg
                .selectAll("g#main-speakers-bars-g")
                .data(_data)
                .join(
                    (enter) =>
                        enter
                            .append("g")
                            .attr("id", "main-speakers-bars-g")
                            .attr(
                                "transform",
                                (d) => `translate(0,${y(d.name)})`,
                            ),
                    (update) =>
                        update.attr(
                            "transform",
                            (d) => `translate(0,${y(d.name)})`,
                        ),
                    (exit) => exit.remove(),
                );
            //.call((exit) => exit.remove());

            /** Handle all bar sequences states */
            var barUpdate = barGroups
                .selectAll("rect#main-speakers-rect")
                .data((d) => d.invites)
                .join(
                    (enter) =>
                        enter
                            .append("rect")
                            .attr("id", "main-speakers-rect")
                            .attr("x", (d) => x(d.start))
                            .attr("y", 0)
                            .attr(
                                "fill",
                                (d) => utils.showKeyToColour[d.talkshow],
                            )
                            .attr("rx", 4)
                            .attr("width", (d) => x(d.end - d.start) - gapSize)
                            .attr("height", y.bandwidth()),
                    (update) => {
                        update
                            .attr("x", (d) => x(d.start))
                            .transition()
                            //.delay((_, i) => transitSpeed)
                            //.ease(d3.easeBackIn)
                            .attr(
                                "fill",
                                (d) => utils.showKeyToColour[d.talkshow],
                            )
                            .attr("width", (d) => x(d.end - d.start) - gapSize);
                    },
                    (exit) => exit.remove(),
                );

            var nameGroups = svg
                .selectAll("g#main-speakers-names-g")
                .data(_data)
                .join(
                    (enter) =>
                        enter
                            .append("g")
                            .attr("id", "main-speakers-names-g")
                            .attr(
                                "transform",
                                (d) => `translate(0,${y(d.name)})`,
                            ),
                    (update) =>
                        update.attr(
                            "transform",
                            (d) => `translate(0,${y(d.name)})`,
                        ),
                    (exit) => exit.remove(),
                );

            let nameLabels = nameGroups
                .selectAll("text#main-speakers-names-g-text")
                .data((d) => [d])
                .join(
                    (enter) => {
                        enter
                            .append("text")
                            .attr("id", "main-speakers-names-g-text")
                            .attr("x", textAlign)
                            .attr("y", (d) => y.bandwidth() / 2 + 5)
                            .text((d) => d.name);
                        utils.setText(
                            enter.selectAll("text"),
                            22,
                            500,
                            "start",
                        );
                    },
                    (update) => update.attr("x", textAlign).text((d) => d.name),
                    (exit) => exit.remove(),
                );
        };
        update();
    });
</script>

<div class="grid grid-cols-1">
    <div class="pt-4 flex gap-4">
        <button
            aria-label="Up the list"
            class="flex hover:text-stone-400"
            id={`${id}-backward`}
            value="backward"
            ><svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                class="size-6"
            >
                <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="m4.5 15.75 7.5-7.5 7.5 7.5"
                />
            </svg>
        </button>
        <button
            aria-label="Forward"
            class="flex hover:text-stone-400"
            id={`${id}-forward`}
            value="forward"
            ><svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                class="size-6"
            >
                <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="m19.5 8.25-7.5 7.5-7.5-7.5"
                />
            </svg>
        </button>
        <p>Talkende {current} - {current + n}</p>
    </div>
    <div {id} class="pt-2 pb-12"></div>
</div>

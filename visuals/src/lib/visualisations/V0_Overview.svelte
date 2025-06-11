<script>
    import { onMount } from "svelte";
    import * as d3 from "d3";
    import * as utils from "./utils";
    import { timeFormatDeLocale, tickFormat } from "./formatting";

    // Local utility
    Date.prototype.addDays = function (days) {
        var date = new Date(this.valueOf());
        date.setDate(date.getDate() + days);
        return date;
    };

    let { data, id } = $props();
    let _data = utils.uniformStart(data.data);

    let startDate = d3.min(_data.map((d) => d.date));
    let endDate = d3.max(_data.map((d) => d.date));
    let timeRangeStart = timeFormatDeLocale.format("%Y/%m/%d")(startDate);
    let timeRangeEnd = timeFormatDeLocale.format("%Y/%m/%d")(endDate);
    let timeRangeDays = Math.floor(
        (endDate - startDate) / (1000 * 60 * 60 * 24),
    );
    let uniqueTalkDates = new Array(
        ...new Set(
            _data.map((d) => timeFormatDeLocale.format("%Y/%m/%d")(d.date)),
        ),
    )
        .map((strD) => new Date(strD))
        .sort((a, b) => a - b);

    let uniqueEpisodes = new Array(
        ...new Set(_data.map((d) => d.episode_name)),
    );
    let uniqueGuests = new Array(...new Set(_data.map((d) => d.name)));
    let uniqueRoles = new Array(...new Set(_data.map((d) => d.role)));

    // Log some basic information for the dataset
    console.log("Time range:", `${timeRangeStart} - ${timeRangeEnd}`);
    console.log("Time range in days:", timeRangeDays);
    console.log("Days with a show:", uniqueTalkDates.length);
    console.log("Episodes:", uniqueEpisodes.length);
    console.log("Guests:", uniqueGuests.length);
    console.log("Roles", uniqueRoles.length, "/", "Appearences", data.data.length);

    onMount(() => {
        const width = 1600;
        const height = 300;
        const margins = { top: 20, bottom: 20 };

        var x = d3
            .scaleTime()
            .range([0, width - 20])
            .domain([startDate, endDate.addDays(1)]);

        const svg = utils.createSvg(id, width, height, "visible");

        var gx = svg
            .append("g")
            .call(
                d3
                    .axisBottom(x)
                    .tickSizeOuter(0)
                    .tickFormat(d3.timeFormat("%b %y")),
            )
            .call((g) => utils.setText(g.selectAll("text"), 20, 500, "start"))
            .call((g) => g.selectAll("line").attr("stroke-width", 2))
            .attr("id", "v0-gX")
            .attr(
                "transform",
                `translate(0,${height - margins.bottom - margins.top})`,
            );

        var rectsContainer = svg.append("g").attr("id", "v0-g1");

        var rects = rectsContainer
            .selectAll("rect")
            .data(uniqueTalkDates)
            .join("rect")
            .attr("id", "v0-g1-r")
            .attr("x", (d) => x(d))
            .attr("y", 0)
            .attr("width", (d) => x(d.addDays(1)) - x(d) - 0.5)
            .attr("height", height - margins.bottom - margins.top);
    });
</script>

<div {id}></div>

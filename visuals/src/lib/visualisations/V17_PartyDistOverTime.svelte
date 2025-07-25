<script>
    import { onMount } from "svelte";
    import * as utils from "./utils.js";
    import * as d3 from "d3";

    import { timeFormatDeLocale } from "./formatting.js";

    const fixId = utils.partyToId;

    /** Helper functions */
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

    /** Passed data and id */
    let { data, id } = $props();

    // Earliest day when news of BfV report on AfD were released
    // -> https://www.tagesschau.de/inland/innenpolitik/verfassungsschutz-afd-102.html
    let start = new Date(2025, 4, 2);
    let allParties = new Array(
        ...new Set(data.data.filter((d) => d.party != "").map((d) => d.party)),
    );
    let partySelection = allParties
        .map((p) => ({ party: p, selected: true }))
        .sort((a, b) => a.party.localeCompare(b.party));

    const transformData = (originalData) => {
        var _data = originalData.filter((d) => d.party != "");
        _data = _data.map((d) => ({
            ...d,
            ym: new Date(d.date.getFullYear(), d.date.getMonth(), 1),
        }));

        var allMonths = new Array(
            ...new Set(_data.map((d) => d.ym.toISOString())),
        );

        let monthData = d3
            .groups(_data, (d) => d.party)
            .map((partyData) => ({
                party: partyData[0],
                children: allMonths
                    .map((ym) => {
                        var values = partyData[1].filter(
                            (D) => D.ym.toISOString() == ym,
                        );
                        return {
                            ym: new Date(ym),
                            party: partyData[0],
                            children: values.sort((a, b) => b.ym - a.ym),
                            value: values.length,
                        };
                    })
                    .sort((a, b) => b.ym - a.ym),
            }));
        return monthData;
    };

    const buildFlatPoints = (grouped, xFn, yFn, xMargin) => {
        const points = new Array();
        grouped.forEach((group) => {
            group.children.forEach((child) => {
                points.push([
                    xFn(child.ym) + xMargin,
                    yFn(child.value),
                    child.party,
                ]);
            });
        });
        return points;
    };

    let partyData = transformData(data.data);
    const filterFn = (data) =>
        data.filter(
            (d) =>
                d.date < new Date(2025, 3, 1) &&
                new Date(2025, 2, 1) <= d.date &&
                d.talkshow == "markuslanz",
        );

    onMount(() => {
        /** Highlight button function */
        function highlightFn(event) {
            let targetData = event.target.__attributes.data;
            partySelection[targetData.party] = !targetData.selected;
            event.target.__attributes.data.selected = !targetData.selected;
            const new_html = partySelection[targetData.party]
                ? `✔️${targetData.party}`
                : targetData.party;
            d3.select(event.target).html(new_html);
            highlightToggle(event.target.__attributes.data);
        }

        /** Apply button function to buttons */
        d3.selectAll(`button#${id}-select-btn`).on("click", highlightFn);

        const width = 1600;
        const height = 700;
        const margins = { left: 50, top: 30, right: 90, bottom: 40 };

        const gapSize = 4;

        const yMax = d3.max(
            partyData.map((d) => d3.max(d.children, (D) => D.value)),
        );
        const xMin = d3.min(partyData[0].children.map((d) => d.ym));
        const xMax = d3.max(partyData[0].children.map((d) => d.ym));

        var x = d3
            .scaleLinear()
            .range([0, width - margins.right])
            .domain([xMin, xMax]);
        var y = d3
            .scaleLinear()
            .range([margins.top, height - margins.bottom])
            .domain([yMax, 0]);

        let points = buildFlatPoints(partyData, x, y, margins.left);

        const svg = utils.createSvg(id, width, height, "visible");

        var gx = svg
            .append("g")
            .attr("id", `${id}-axis-gx`)
            .attr(
                "transform",
                `translate(${margins.left},${height - (margins.bottom)})`,
            )
            .call(
                d3
                    .axisBottom(x)
                    .tickFormat((d) => timeFormatDeLocale.format("%b %y")(d))
                    .tickValues(partyData[0].children.map((d) => d.ym)),
            )
            .call((g) => g.select(".domain").remove())
            .call((g) => {
                utils.setText(g.selectAll(".tick text"), 22, 500, "middle");
                //g.selectAll(".tick text").first().attr("text-anchor", "end");
            });

        var gy = svg
            .append("g")
            .attr("id", `${id}-axis-gy`)
            .attr("transform", `translate(${margins.left - 10},0)`)
            .call(d3.axisLeft(y))
            .call((g) => g.select(".domain").remove())
            .call((g) =>
                utils.setText(g.selectAll(".tick text"), 22, 500, "end"),
            );

        var gyLabel = gy
            .append("text")
            .attr("y", margins.top + 20)
            .attr("x", 0)
            .attr("fill", "black")
            //.attr("dy", ".75em")
            .text("Anzahl der Auftritte");

        utils.setText(gyLabel, 22, 500, "start");

        const line = d3
            .line()
            .x((d) => x(d.ym))
            .y((d) => y(d.value))
            .curve(d3.curveCardinal.tension(0.2));

        var mainGroup = svg
            .append("g")
            .attr("id", `${id}-main-g`)
            .attr("transform", `translate(${margins.left},0)`);

        var lines = mainGroup
            .selectAll("path")
            .data(partyData)
            .join("path")
            .attr("id", (d) => `${id}-${fixId(d.party)}-line`)
            .attr("stroke", (d) => utils.partyToColour[d.party])
            .attr("stroke-width", 4)
            .style("mix-blend-mode", "multiply")
            .attr("d", (d) => line(d.children))
            .attr("fill", "none");

        var circleGroups = mainGroup
            .selectAll("g")
            .data(partyData)
            .join("g")
            .attr("id", `${id}-circles-g`);

        var circles = circleGroups
            .selectAll("circle")
            .data((d) => d.children)
            .join("circle")
            .attr("id", (d) => `${id}-circle-${fixId(d.party)}`)
            .attr("cx", (d) => x(d.ym))
            .attr("cy", (d) => y(d.value))
            .attr("r", "4")
            .attr("fill", (d) => utils.partyToColour[d.party])
            .attr("display", (d) => "block");

        // Tooltip group
        const dot = svg.append("g").attr("display", "none");
        dot.append("circle").attr("r", 4);
        dot.append("text").attr("text-anchor", "middle").attr("y", -8);
        utils.setText(dot.selectAll("text"), 20, 500, "middle");

        /** Functions to handle filter line highlighting */
        function highlightToggle({ party, selected }) {
            const t = d3.easePoly.exponent(2);
            d3.select(`#${id}-${fixId(party)}-line`)
                .transition(d3.easePoly(t))
                .style(
                    "stroke",
                    selected ? utils.partyToColour[party] : "#ddd",
                );
            d3.selectAll(`#${id}-circle-${fixId(party)}`)
                .transition(d3.easePoly(t))
                .attr("fill", selected ? utils.partyToColour[party] : "#ddd");
        }

        /** Functions to handle nearest line to mouse hover event */
        function pointermoved(event) {
            const [xm, ym] = d3.pointer(event);
            const i = d3.leastIndex(points, ([x, y]) =>
                Math.hypot(x - xm, y - ym),
            );
            const [x, y, k] = points[i];
            lines.style("stroke", ({ party }) => {
                return party === k ? utils.partyToColour[party] : "#ddd";
            });
            circles.attr("display", ({ party }) => {
                return party === k ? "block" : "none";
            });
            dot.attr("transform", `translate(${x},${y})`).attr(
                "fill",
                utils.partyToColour[k],
            );
            dot.select("text").text(k);
            svg.property("value", points[i]).dispatch("input", {
                bubbles: true,
            });
        }

        function pointerentered() {
            lines.style("mix-blend-mode", null).style("stroke", "#ddd");
            dot.attr("display", null);
        }

        function pointerleft() {
            lines.style("mix-blend-mode", "multiply").style("stroke", null);
            dot.attr("display", "none");
            svg.node().value = null;
            circles.attr("display", "none");
            svg.dispatch("input", { bubbles: true });
        }

        // svg.on("pointerenter", pointerentered)
        //     .on("pointermove", pointermoved)
        //     .on("pointerleave", pointerleft)
        //     .on("touchstart", (event) => event.preventDefault());
    });
</script>

<div>
    <div id={`${id}-btn-section`} class="flex flex-wrap gap-2">
        {#each partySelection as selection}
            <button
                aria-label="Selected"
                id={`${id}-select-btn`}
                data={selection}
                class="flex px-1 rounded-sm hover:text-stone-400 border-1 whitespace-nowrap"
            >
                {#if selection.selected}✔️{/if}{selection.party}
            </button>
        {/each}
    </div>
    <div {id}></div>
</div>

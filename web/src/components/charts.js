import * as d3 from "npm:d3";
import * as Plot from "npm:@observablehq/plot";

import * as utils from "./utils.js";
import { timeFormatDeLocale } from "./formatting.js";


const defaultMargins = { marginTop: 30, marginLeft: 0, marginRight: 0, marginBottom: 0 };

export function marginX(margin) {
    return { marginLeft: margin, marginRight: margin };
}

export function marginY(margin) {
    return { marginTop: margin, marginBottom: margin };
}

export function overviewChart(data, width) {
    const dates = d3.groups(data, (d) => d.date).map(grp => grp[0]);
    return Plot.plot({
        title: "Sendefrequenz von ÖRR-Talkshows",
        subtitle: "Wann erscheinen Talkshows in ARD und ZDF über das Jahr gesehen?",
        ...marginX(12),
        width,
        height: 160,
        marks: [
            Plot.ruleX(dates),
            Plot.tip(
                [`Sommerpause`],
                { x: new Date("2024-08-01"), dy: 1, anchor: "bottom" }
            ),
            Plot.tip(
                [`Weihnachten/Neujahr`],
                { x: new Date("2024-12-27"), dy: 1, anchor: "bottom" }
            )
        ]
    });
}

export function episodesPerFormat(data, width) {
    const episodes = d3.groups(data, (d) => d.talkshow).map(
        grp => ({
            talkshow: utils.mapShowNames[grp[0]],
            count: d3.groups(grp[1], (d) => d.episode_name).length,
            fill: utils.showKeyToColour[grp[0]]
        })
    );
    return Plot.plot({
        title: "Sendungen im Datenzeitraum",
        subtitle: "Markus Lanz sendet mit der stärksten Dominanz im ÖRR",
        marginLeft: 82,
        marginRight: 12,
        ...marginY(0),
        x: { axis: null },
        y: { label: null },
        width,
        marks: [
            Plot.barX(episodes, {
                x: "count",
                y: "talkshow",
                r: 3,
                sort: { y: "x", reverse: true },
                fill: "fill",
            }),
            Plot.text(episodes, {
                text: (d) => d.count,
                y: "talkshow",
                x: "count",
                textAnchor: "end",
                dx: -3,
                fill: "white"
            })
        ]
    })
}

export function talkingMinutesPerMonth(data, width) {
    let episodeData = d3.groups(data, (d) => d.episode_name)
        .map(D => ({
            episode_name: D[0],
            date: D[1][0].date,
            len: D[1][0].len,
            talkshow: D[1][0].talkshow,
            month: new Date(D[1][0].date.getFullYear(), D[1][0].date.getMonth(), 1)
        }));
    let __data = [];
    const labels = [];
    d3.groups(episodeData, d => d.month).forEach(D => {
        const showData = d3.groups(D[1], e => e.talkshow);
        const formatTime = d3.timeFormat("%Y, %B");
        labels.push({
            month: D[0],
            minutesSum: d3.sum(D[1], e => e.len),

        })
        showData.forEach(E => {
            __data.push({
                month: D[0],
                talkshow: E[0],
                show: utils.mapShowNames[E[0]],
                minutes: d3.sum(E[1], e => e.len),
                Monat: formatTime(D[0]),
                fill: utils.showKeyToColour[E[0]],
            })
        });
    });

    return Plot.plot({
        title: "Sendefrequenz pro Format",
        subtitle: "Im Juli machen die ARD-Talkshow Urlaub, die ZDF Shows im August",
        ...marginX(4),
        ...marginY(12),
        marginBottom: 30,
        width,
        x: {
            type: "band",  // interval: "month",
            label: null
        },
        y: { axis: null },
        marks: [
            Plot.barY(__data, {
                x: "month", y: "minutes", fill: "fill", sort: d => utils.showSortOrder[d.talkshow], r: 3,
                inset: 0.5,
                channels: {
                    "Talkminuten": "minutes", "Show": "show", "x": "month", "y": "minutes", "Monat": "Monat",
                },
                tip: {
                    format: { Talkminuten: true, Show: true, Monat: true, x: false, y: false, stroke: false }
                }
            }),
            Plot.text(labels, {
                text: "minutesSum",
                y: "minutesSum",
                x: "month",
                textAnchor: "middle",
                dx: 0,
                dy: -8,
            })
        ]
    });
}

export function talkersList(data, width) {
    const guestFrequencies = d3.groups(data, d => d.name).map(
        d => ({ name: d[0], children: d[1] })
    ).sort(
        (a, b) => b.children.length - a.children.length
    )
    let _data = [];
    guestFrequencies.forEach(({ name, children }, i) => {
        const guestPerTalkshow = d3.groups(children, d => d.talkshow);
        if (i < 30) {
            guestPerTalkshow.forEach(([talkshow, grp]) => {
                _data.push({
                    name: name,
                    total: children.length,
                    talkshow: talkshow,
                    show: utils.mapShowNames[talkshow],
                    count: grp.length,
                    fill: utils.showKeyToColour[talkshow]
                });
            });
        }
    });
    _data = _data.sort((a, b) => b.total - a.total);

    return Plot.plot({
        title: "Top Talkende nach Auftritten und Formaten",
        subtitle: "Der 'Elmar Theveßen-Effekt' kommt fast im Alleingang durch die Redaktion von Lanz zustande",
        marginLeft: 110,
        marginRight: 20,
        marginTop: 0,
        marginBottom: 30,
        width,
        x: { grid: true },
        y: { label: null },
        color: {
            type: "ordinal",
            domain: new Array(...new Set(_data.map(d => d.talkshow))),
            range: new Array(...new Set(_data.map(d => d.fill))),
            legend: true
        },
        marks: [
            Plot.barX(_data, {
                x: "count",
                y: "name",
                fill: "talkshow",
                r: 3,
                inset: 0.5,
                channels: { "Name": "name", "Auftritte": "count", "Gesamt": "total" },
                sort: {
                    y: { value: "Gesamt", reduce: "max", order: "descending" },
                },
                tip: {
                    format: { x: false, y: false }
                },
                order: "count",
            })
        ]
    });
}

export function talkersVsAppearences1(data, width) {
    const guests = d3.groups(data, d => d.name)
        .map(([name, grp]) => ({ name: name, count: grp.length, children: grp }));
    const numTotalGuests = guests.length;
    const binsForGuests = d3.groups(guests, d => d.count)
        .map(([count, grp]) => {
            const percGuests = grp.length / numTotalGuests * 100;
            return {
                count: count,
                nGuests: grp.length,
                percGuests: percGuests,
                children: grp.map(g => ({ name: g.name })),
                // note: `Anzahl Talkender mit ${count} Auftritte(n), machen ${Math.round(percGuests, 2)}% aller Talkenden aus.`,
                fill: count <= 3 ? "lightgray" : "darkgray"
            }
        })
        .sort((a, b) => b.count - a.count);
    return Plot.plot({
        title: "#Talkender vs. #Auftritte (1)",
        subtitle: "Die Mehrheit der Talkenden wird seltener in Talkshows eingeladen.",
        marginLeft: 10,
        marginRight: 10,
        width: width,
        height: 100,
        x: { round: true, label: "% aller Talkenden" },
        marks: [
            Plot.barX(binsForGuests, {
                x: "percGuests",
                fill: "fill",
                r: 3,
                inset: 0.2,
                channels: { "Anzahl Auftritte": "count", "Anzahl Personen": "nGuests", "% an allen Talkenden": "percGuests" },
                tip: {
                    format: { x: false, y: false }, dy: 8,
                }
            }),
            Plot.textX(binsForGuests, Plot.stackX({
                x: "percGuests",
                text: "count",
                fill: "black",
                fontWeight: "bold",
                inset: 0.2,
            }))
        ]
    });
}

export function talkersVsAppearences2(data, width) {
    const numTotalSeats = data.length;
    const guests = d3.groups(data, d => d.name)
        .map(([name, grp]) => ({ name: name, count: grp.length, children: grp }));
    const binsForSeats = d3.groups(guests, d => d.count)
        .map(([count, grp]) => {
            const percSeats = grp.length * count / numTotalSeats * 100;
            return {
                count: count,
                nGuests: grp.length,
                percSeats: percSeats,
                children: grp.map(g => ({ name: g.name })),
                fill: count <= 3 ? "lightgray" : "darkgray"
            }
        })
        .sort((a, b) => b.count - a.count);

    return Plot.plot({
        title: "#Talkender vs. #Auftritte (2)",
        subtitle: "Die Mehrheit der Auftritte wird von der Minderheit der Talkenden absolviert.",
        marginLeft: 10,
        marginRight: 10,
        width: width,
        height: 100,
        x: { round: true, label: "% aller Auftritten" },
        marks: [
            Plot.barX(binsForSeats, {
                x: "percSeats",
                fill: "fill",
                r: 3,
                inset: 0.2,
                channels: { "Anzahl Auftritte": "count", "Anzahl Personen": "nGuests", "% an allen Auftritte": "percSeats" },
                tip: { format: { x: false, y: false }, dy: 8, }
            }),
            Plot.textX(binsForSeats, Plot.stackX({
                x: "percSeats",
                text: "count",
                fill: "black",
                fontWeight: "bold",
                inset: 0.2,
            }))
        ]
    });
}

export function groupAnalysis1(data, mode, width) {
    let _data = data;
    if (mode !== "Ganzer Zeitraum") {
        _data = utils.uniformStart(_data, utils.dateContext["btw"])
        _data = _data.filter((d) => d.date <= new Date(2025, 1, 23));
    }

    _data = _data.map((d) => (
        { ...d, fill: utils.showKeyToColour[d.talkshow] }
    ));

    return Plot.plot({
        title: "Gruppen pro Format",
        subtitle: "Welche Shows laden gerne Talkende aus welchen Gruppen?",
        marginTop: 0,
        marginLeft: 100,
        marginRight: 10,
        width: width,
        height: 500,
        x: { label: "Anzahl Auftritte" },
        fy: { label: null },
        marks: [
            Plot.waffleX(_data, Plot.groupZ(
                { x: "sum" },
                // {fx: "date_of_birth", }
                { fy: "group", unit: 1, fill: "fill", sort: { fy: "x", reverse: true } }
            )),
        ],
        color: {
            type: "ordinal",
            domain: new Array(...new Set(_data.map(d => d.talkshow))),
            range: new Array(...new Set(_data.map(d => d.fill))),
            legend: true,
        }
    })
}

export function groupAnalysis2(data, mode, width) {
    let _data = data;
    if (mode !== "Ganzer Zeitraum") {
        _data = utils.uniformStart(_data, utils.dateContext["btw"]);
        _data = _data.filter((d) => d.date <= new Date(2025, 1, 23));
    }
    _data = _data.filter((d) => d.group !== "Sonstige" && d.role.length > 0);
    let groups = d3.groups(_data, d => d.group)
        .map(([groupName, grp]) => ({ group: groupName, children: grp }));

    let groupSpeakers = [];
    groups.forEach(({ group, children }) => {
        d3.groups(children, d => d.name)
            .sort((a, b) => b[1].length - a[1].length)
            .forEach(([name, grp], i) => {
                const isGroupSpeaker = i == 0 ? "Top" : "Talkende";
                groupSpeakers.push(({
                    group,
                    name,
                    count: grp.length,
                    type: isGroupSpeaker,
                    roles: grp.map(d => d.role)
                }))
            })
    });
    return Plot.plot({
        title: "Gruppesprecher:innen",
        subtitle: "Wer sind die am häufigsten geladenen Personen, pro Gruppe?",
        marginTop: 0,
        marginLeft: 100,
        marginRight: 10,
        width: width,
        height: 500,
        y: { label: null },
        x: { label: "Auftritte pro Talkende & Gruppe" },
        color: {
            type: "ordinal",
            domain: ["Top", "Talkende"],
            range: ["darkgray", "lightgray"],
            legend: true,
        },
        marks: [
            Plot.barX(
                groupSpeakers, {
                y: "group", x: "count", fill: "type", r: 3, inset: 0.2, sort: {
                    y: "x", reverse: true
                }, channels: {
                    "Name": "name", "Auftritte": "count", "Rollen": "roles"
                },
                tip: {
                    format: { Name: true, Auftritte: true, Rollen: true, x: false, y: false, stroke: false }
                }
            }
            )
        ]
    });
}


export function mediaAndJournalism(data, width) {
    const dateEnd = d3.extent(data, d => d.date)[1]
    let _data = data.filter(d => d.media.length > 0 && d.group === "Journalismus")

    const journalists = [];
    d3.groups(_data, d => d.media).forEach(([media, grpMedia]) => {
        d3.groups(grpMedia, d => d.name).forEach(([name, grpName]) => {
            const lastSeen = d3.extent(grpName, d => d.date)[1];
            journalists.push({
                name,
                Medienhaus: media,
                count: grpName.length,
                seenDaysAgo: Math.round(Math.abs((dateEnd - lastSeen) / (24 * 60 * 60 * 1000)))
            })
        })
    });

    return Plot.plot({
        title: "Wer ordnet Talkshowgeschehen ein?",
        subtitle: "Journalist:innen der Medienhäuser, nach Häufigkeit und letzem Auftritt",
        marginLeft: 100,
        width,
        height: 800,
        x: { grid: true, label: "Tage seit letztem Auftritt" },
        fy: { grid: false, label: null },
        color: { legend: false },
        marks: [
            Plot.dot(journalists,
                Plot.dodgeY("middle", {
                    fy: "Medienhaus",
                    x: "seenDaysAgo",
                    r: "count",
                    fill: "Medienhaus",
                    //strokeWidth: 2.5,
                    channels: { "Name": "name", "Auftritte": "count", "Tage seit letztem Auftritt": "seenDaysAgo" },
                    tip: {
                        format: { Name: true, Auftritte: true, count: false, x: false, r: false }
                    }
                }),
            )
        ]
    })
}

export function partyDistribution(data, width) {
    const _data = data.filter((d) => d.party);
    const numPoliticians = _data.length;
    const start = d3.extent(data, d => d.date)[0];
    let politics = d3.groups(_data, (d) => d.party)
        .map(([party, grp]) => ({
            party,
            count: grp.length,
            perc: (grp.length / numPoliticians * 100).toFixed(2),
            roles: grp.map(d => d.role),
            fill: utils.partyToColour[party]
        }));
    return Plot.plot({
        title: "Auftritte von Parteipolitker:innen in ÖRR Talkshows",
        subtitle: `Über alle ${numPoliticians} Auftritte von Parteipolitiker:innen seit ${d3.timeFormat("%d. %b %Y")(start)}`,
        marginTop: 10,
        marginBottom: 0,
        width,
        x: { label: null },
        y: { label: "Auftritte" },
        marks: [
            Plot.barY(politics, {
                x: "party",
                y: "count",
                fill: "fill",
                r: 3,
                sort: { x: "y", reverse: true }
            }),
            Plot.text(politics, {
                x: "party",
                y: "count",
                text: "perc",
                textAnchor: "middle",
                dy: -8,
            })
        ]
    })
}

export function partyDistributionOverTime(data, width, height) {
    let _data = data.filter((d) => d.party.length > 0 && d.date > new Date(2024, 1, 1));
    const parties = new Array(...new Set(_data.map((d) => d.party)));
    const colours = parties.map(party => utils.partyToColour[party]);

    return Plot.plot({
        title: "Parteivertretungen in Talkshows über die Zeit",
        subtitle: "Welche Parteien wurden wann in Talkshows geladen?",
        marginBottom: 20,
        width,
        height,
        x: {
            interval: "month",
            tickFormat: (d) => d.toLocaleString("de", { month: "short" }),
            label: null,
        },
        y: { label: "Auftritte" },
        color: {
            type: "ordinal",
            domain: parties,
            range: colours,
            legend: true,
        },
        marks: [
            Plot.lineY(_data,
                Plot.groupX(
                    { y: "sum" }, {
                    x: "date",
                    stroke: "party",
                    sort: "date",
                    curve: "catmull-rom",
                })
            ),
            Plot.dot(_data,
                Plot.groupX(
                    { y: "sum" }, {
                    x: "date",
                    fill: "party",
                    channel: { "Auftritte": "count" },
                    tip: { format: { x: true, y: true, z: false } },
                }),
            )
        ]
    })
}

export function encounterMatrix(data, width, cutoffFreq = 10) {
    const guests = d3.groups(data, d => d.name)
        .map(([name, grp]) => ({ name, count: grp.length, children: grp }))
        .filter((d) => d.count >= cutoffFreq);
    const numGuests = guests.length;
    const name2id = guests.reduce((elements, item, index) => {
        elements[item.name] = index;
        return elements;
    }, {});

    let guestMatrix = [...Array(numGuests)].map(_ => Array(numGuests).fill(0))
    guests.forEach(({ name, children }) => {
        const guestEpisodes = children.map((d) => d.episode_name);
        const episodes = data.filter((d) => guestEpisodes.includes(d.episode_name));
        const encounters = d3.groups(episodes, d => d.name).map(([encounterName, grp]) => ({ name: encounterName, count: grp.length }))
        encounters.forEach((encounter) => {
            if (!encounter.name in name2id) return;
            const i = name2id[name];
            const j = name2id[encounter.name];
            guestMatrix[i][j] = guestMatrix[i][j] + encounter.count;
        });
    })
    const encounters = guestMatrix.reduce((elements, item, index) => {
        item.forEach((d, j) => {
            elements.push({ name: guests[index].name, encounter: guests[j].name, count: index != j ? d : 0 });
        });
        return elements;
    }, []);

    return Plot.plot({
        title: "ÖRR-Talkshow Begegnungsmatrix",
        subtitle: `Wer begegnet wem in Talkshowformaten wie häufig? (Berücksichtigt Talkende mit ${cutoffFreq} oder mehr Auftritten)`,
        width: width,
        height: width,
        marginLeft: 100,
        marginTop: 100,
        x: { axis: "top", tickRotate: -90, label: null },
        y: { label: null },
        color: { scheme: "OrRd", legend: true },
        marks: [
            Plot.cell(
                encounters, {
                x: "name",
                y: "encounter",
                fill: "count",
                r: 3,
                sort: { x: "fill", y: "fill", reverse: true },
                channels: { "Talkende A": "name", "Talkende B": "encounter", "Begegnungen": "count" },
                tip: { format: { x: false, y: false, fill: false } }
            }),
        ]
    })
}
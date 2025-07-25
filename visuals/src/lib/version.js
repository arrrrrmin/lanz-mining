const projectVersions = [
    {
        "name": "GPN23",
        "date": new Date("2025-05-30T00:00"),
        "isCurrent": false,
        "changes": [
            "Initiales projekt release, auf der GPN23.",
            "Plots, Repo, Design, ..."
        ],
        "slug": "/archive/gpn23",
    },
    {
        "name": "TDF4",
        "date": new Date("2025-06-30T00:00"),
        "isCurrent": true,
        "changes": [
            "Einige Diagramme haben ein paar interaktive Möglichkeiten dazu bekommen",
            "'Parteibücher über die Zeit' fasst die Auftritte von Politiker:innen über die Zeit zusammen",
            "Ein Datenleck von zwei Wochen im März 2024 bei Lanz wurde geschlossen. (Sehr viel mehr Elmar)",
            "Kleine kosmentische Änderungen an Diagrammen"
        ],
        "slug": "/",
    }
].sort((a, b) => b.date - a.date);

export default projectVersions;
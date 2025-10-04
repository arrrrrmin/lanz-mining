---
title: LanzMining
---

```js
import * as d3 from "npm:d3";

import { configuration } from "./assets/config.js";
import { fetchLanzMining } from "./data/fetchLanzMining.js";

import * as charts from "./components/charts.js";
```

```js
const dateFormatFn = d3.utcFormat("%Y/%m/%d")
let data = await fetchLanzMining(configuration.datahost, "lanz-mining-2025-6-30.csv");
let [start, end] = d3.extent(data, d => d.date);
let numDaysWithShow = d3.groups(data, d => d.date).length;
let numEpisodes = d3.groups(data, d => d.episode_name).length;
let numTalkers = d3.groups(data, d => d.name).length;
let numRoles = d3.groups(data, d => d.role).length;
let numTalkerSeats = data.length;
let allRoles = new Array(...new Set(data.filter(d => d.role.length > 0).map(d => d.role)));
let allGroups = new Array(...new Set(data.filter(d => d.group.length > 0).map(d => d.group)))
```

LanzMining ist ein Datenprojekt, um die mediale Teilhabe in deutschen Talkshows des öffentlich-rechtlichen Rundfunks zu erkunden. 
Es werden gesammelte Daten aus mehr als einem Jahr untersucht und visualisiert. Der Fokus ist dabei mehr auf den Personen als auf den Themen, da das Projekt keine Aufzeichnungen von Talkshowsendungen selbst analysiert, sondern lediglich die _Metadaten_.
- Von: [@arrrrrmin@chaos.social](https://chaos.social/@arrrrrmin), [@arrrrrmin.bsky.social](https://bsky.app/profile/arrrrrmin.bsky.social)
- Code: [[codeberg](https://codeberg.org/arrrrrmin/lanz-mining), [github](https://github.com/arrrrrmin/lanz-mining)]/arrrrrmin/lanz-mining
- Talk auf der GPN23: [media.ccc.de](https://media.ccc.de/v/gpn23-213-lanzmining-wer-spricht-denn-da-)


## Datenblatt
- Zeitraum: ${dateFormatFn(start)} - ${dateFormatFn(end)} über ${numDaysWithShow} Tage.
- Episoden: ${numEpisodes}
- Talkende: ${numTalkers}
- Rollen: ${numRoles}
- Talkshowplätze: ${numTalkerSeats}

---

## Daten im Überblick
Jeder Strich ist ein betalkter Tag im Datenzeitraum. Das regelmäßige Sendemuster wird nur von der Sommerpause in Juli und August unterbrochen. Auch Talkshow-Redaktionen wollen Urlaub haben.

<div class="card">
    ${resize((width) => charts.overviewChart(data, width))}
</div>

Wenn wir wissen, dass Markus Lanz als einziges Format drei Sendungen die Woche aufzeichnet, ergibt der die nächste Visualisierung Sinn. Sie zeigt die Episoden die pro Format im Datenzeitraum aufgezeichnet wurden.
<div class="card">
    ${resize((width) => charts.episodesPerFormat(data, width))}
</div>

Wir können die letzten beiden Diagramme auch kombinieren, um zu sehen welche Formate in welchen Monaten des Jahres wie häufig senden. In der Spitze kommt man in einem Monat auf ~2200 Minuten Talkshow Content. Das ist viel und bezeugt das es einen rentablen Markt für Polit-Unterhaltung gibt.

<div class="card">
    ${resize((width) => charts.talkingMinutesPerMonth(data, width))}
</div>

Um diese Zahlen in ein Verhältnis zu setzen, sieht man im nächsten Diagramm, wie viele erste Staffeln von SquidGame ein durchschnittlicher Talk-Content Monat betragen würde. So ein durchschnittlicher Monat kommt auf \~3.7 erste Staffeln von SquidGame.

## Wer spricht denn da?
Endlich kommen wir zur eigentlichen Frage "Wer spricht denn da?". 

<div class="card">
    ${resize((width) => charts.talkersList(data, width))}
</div>

Elmar Theveßen ist der am häufigsten geladene Gast. Alleine durch die Auftritte bei Markus Lanz schaft er es auch ohne andere Formate auf Platz 1. Herr Theveßen ist USA-Korrpspondent beim ZDF und damit ist sehr schnell klar warum er so häufig geladen wird: Trump hat irgendetwas getan, oder erzählt, oder gepostet. Medial gibt es ohnehin kein Entkommen vor Trump, deshalb gibt dies auf für die Talkshow-Landschaft. Im Übrigen besteht die List hauptsächlich aus Politiker:innen und Journalist:innen, wobei die paritätische Verteilung unter Journalist:innen deutlich feirer ist als sie es unter Berufspolitiker:innen ist.
So nett diese Grafik sein mag, sie zeigt nur die Top 30 der ${numTalkers} Talkenden. In der nächsten Grafik erhalten wir ein Gefühl für die Verteilung der Gäst:innen zu Auftritten.

## Werden Talkende öfter geladen?
Talkende gruppiert nach der Anzahl wie häufig sie im Datenzeitraum aufgetreten sind. 
Beispielsweise sind alle Talkenden die 2 mal aufgetreten sind n Prozent aller Talkenden.
Die überwiegende Mehrheit der Talkenden wird 1-3 mal eingeladen. Nur eine geringe Anzahl
Personen tritt häufiger in diesen Sendungen auf.

<div class="card">
    ${resize((width) => charts.talkersVsAppearences1(data, width))}
</div>

Wenn wir diese Gruppen jetzt aber den prozentual Anteil jeder Gruppe an den Auftritten
über alle Formate insgesamt betrachten, sieht das Bild umgekehrt aus: Die Minderheit die 
häufiger als drei Auftritte wahrnimmt, absolviert den Großteil aller Auftritte.

<div class="card">
    ${resize((width) => charts.talkersVsAppearences2(data, width))}
</div>

## Thematische Gruppen 

Damit wir jetzt nicht ${numRoles} visualisieren müssen - man wird ohnehin nichts erkennen - 
gruppieren wir die Rollen in Gruppen. Insgesamt sind es ${allGroups.length} Gruppen, die Thematisch - man könnte auch sagen - Kompetenz aufgeteilt sind. Wichtig zum Verständnis, Personen werden nicht zwingend in einer Gruppe verortet. Wer in unterschiedlichen Rollen in unterschiedlichen Formaten angekündigt wird, wird jeweils mit der einzelnen Rolle gruppiert. So können Talkende in unterschiedlichen Gruppen auftauchen, je nachdem wie sie angekündigt werden.

<div class="card" style="padding: 0; max-width: 640;">

```js
const groupCounts = d3.groups(data, d => d.group).map(([group, grp]) => ({group, count: grp.length}));
const groupTable = Inputs.table(groupCounts, {header: {group: "Gruppe", count: "Auftritte"}, rows: 10});
view(groupTable)
```

</div>

Wenig verwunderlich werden die Gruppen _Politik_ und _Journalismus_ am häufigsten eingeladen. Polittalk eben.
Spannender wird es in den kleineren Gruppen. Überraschend liegt die Kultur direkt nach der Wirtschaft. Das ist Frau Maischberger zu verdanken. Wer jetzt allerdings glaubt das es sich hier verstärkt um Schriftsteller:innen und Autor:innen handelt, irrt. Es werden oft fachfremde Kabaretist:innen und Comedians geladen, um das Geschehen mit Journalisten und/oder Sachverständigen zu kommentieren. Daher der Ausschlag. _Hart aber fair_ hat eine Tendez zur _Sonstigen_-Gruppe, denn es werden häufig Betroffene eingeladen, die ihre Perspektive besteuern können. 

```js
const groupMode1 = view(
    Inputs.radio(["Ganzer Zeitraum", "Seit Koalitionsbruch (6.11.24)"], {value: "Ganzer Zeitraum"})
);
```
<div class="card">
${resize((width) => charts.groupAnalysis1(data, groupMode1, width))}
</div>

Die Gruppe _Inneres_ wird von Markus Lanz am häufigsten bespielt. Talkende bei _Maybrit Illner_ sind vermehrt aus der Gruppe _Internationales_, was für die Redaktion von _Caren Miosga_ weniger interessant scheint.

## Talkende nach Gruppen

In der nächsten Grafik sehen wir, welche Talkenden zu welcher Gruppe gehören und pro Gruppe die meist geladene Person. Beispielsweise wird zum Thema Migration (dem _Inneren_ zugehörend) verstärkt [Gerald Knaus](https://de.wikipedia.org/wiki/Gerald_Knaus) eingeladen.

```js
const groupMode2 = view(
    Inputs.radio(["Ganzer Zeitraum", "Seit Koalitionsbruch (6.11.24)"], {value: "Ganzer Zeitraum"})
);
```

<div class="card">
${resize((width) => charts.groupAnalysis2(data, groupMode2, width))}
</div>


## Der Journalismus™

> Kurzer Disclaimer: Das wird hier keine Pauschale Journalismuskritik. Jede kann ihre eigene Haltung zu journalistischer Bereichterstattung oder dem ÖRR entwickelt haben, die Daten sollen nur zeigen, welche Medien und Journalist:innen aus den Daten herausstechen, keine Urteile fällen. Wer das machen möchte, soll sich mit den Publikationen der Schreibenden beschäftigen und auf deren Inhalt eine Haltung entwickeln.

Der folgende Plot zeigt welche Journalisten (aus welchen Medienhäusern) in ÖRR Talkshows das gesprochene Einordnen. Die Farben wiederholen sich weil es zu viele Häuser für die Farbpalette gibt. Pro Zeile ein journalistisches Medium, pro Kreis eine Journalist:in. Je größer ein Kreis, desto häufiger war die Person in einem oder mehreren Formaten aufgetreten und je weiter links, desto kürzer ist der letzte Auftritt her. 
Bekannte große Medien wie der _Spiegel_, _Zeit_, _TAZ_, _Welt_ oder das _Redaktions Netzwerk Deutschland (RND)_ sind mit einigen Vertretungen sehr weit links in der Grafik, meist jenseits der 50 Tage Marke. Diese Vertretungen finden wir auch in [Top Talkende nach Auftritten und Formaten](#wer-spricht-denn-da) wieder.

<div class="card">
${resize((width) => charts.mediaAndJournalism(data, width))}
</div>

Im Gegensatz zu den meisten Formaten, hat die _Zeit_ eine hohe viele einzelne Vertretungen in Talkshows, die aber nicht so häufig auftreten wie die Top Journalisten von z.B. der _Welt_, _Spiegel_ oder _Table.Media_ mit [Robin Alexander](https://de.wikipedia.org/wiki/Robin_Alexander), [Melanie Amann](https://de.wikipedia.org/wiki/Melanie_Amann) oder [Michael Bröcker](https://de.wikipedia.org/wiki/Michael_Bröcker).

## Parteibücher in Talkshow

Zum Ende noch ein wenig Inhalt zur letzten großen Gruppe: Politiker:innen. Am stärksten über den Datenzeitraum sind mit Abstand SPD und CDU. Das liegt vermutlich auch daran, das diese Parteien die meisten Mitglieder haben und daher die Wahrscheinlichkeit hoch ist, auf eine Anfrage eine passende Person zu finden. Aus heutiger (Mitte 2025) Sicht erscheint die Stärke der FDP etwas ungewöhnlich. In den Daten ist 2024 enthalten und in dieser Zeit hab es nicht wenige Auseinandersetzungen in der Ampel mit der FDP. Die Partei hat besonders im Mai 2024 und im Herbst 2024 sehr viel Gesprächsstoff geliefert.

<div class="grid grid-cols-4">
<div class="card grid-colspan-2 grid-rowspan-3">
${resize((width) => charts.partyDistribution(data, width))}
</div>

<div class="card grid-colspan-2 grid-rowspan-3">
${resize((width) => charts.partyDistributionOverTime(data, width))}
</div>
</div>

## Wer trifft sich, wie oft?

<div>

Nach einigen Talks zu dem Thema, habe ich Feedback bekommen, das man sich wünscht zu erfahren, _wer, mit dem, wie oft_. Das ist wirklich interessant und deshalb gibt es folgende Darstellung als Nachtrag. 

Aus der Matrix können wir erkennen, wer wen in Talkshows trifft und wie häufig das geschieht. Die Daten reichen leider nur über knapp 1,5 Jahre und deshalb ist die Matrix nur mäßig ergiebig. Mit der Zeit könnte es aber sein das sich hier Muster ergeben werden, also ist es gut diese Darstellung zu haben. 

Die Matrix könnt ihr mit dem Regler übersichtlicher machen, er legt fest wie viele Auftritte eine Person gehabt haben muss um als Zeile (und Spalte) in die Matrix aufgenommen zu werden.

```js
const cutoffFreq = view(Inputs.range([5, 13], {step: 1, value: 10}));
```

</div>
<div class="grid grid-cols-4">
<div class="card grid-colspan-3" style="overflow: hidden;">
${resize((width) => charts.encounterMatrix(data, width, cutoffFreq))}
</div>
</div>

--- 

## Mehr

Wer mehr zu dem Thema wissen möchte, der Spiegel hat sich 10 Jahre der Daten vorgenommen und in einen Artikel gegossen: [Talkshow-König Karl, Berlins Balzac und der ewige TV-Schattenkanzlerkandidat](https://www.spiegel.de/kultur/tv/sandra-maischberger-markus-lanz-und-caren-miosga-talkshows-in-der-datenanalyse-a-b7e46530-d826-4424-95c5-6c2f220595b1) (leider nur mit Spiegel+ verfügbar).

Zur Zeit läuft ein Migrationsprojekt um diese Analyse anhand von WikiData-Informationen nachzubauen. So könnte man einige unschöne Eigenschaften von z.B. Gruppen-Analysen bereinigen, weil man die Gruppen bestimmt besser anhand der WikiData-Eigenschaften von Personen bestimmen kann als wenn man versucht sie mit String Pattern Matching zu finden. Die Methode ist jetzt schon nicht perfekt und wird bei größeren Datenmengen sicher zu pflegeintensiv.

## Kontakt

Wer mit mir Kontakt aufnehmen möchte, kann das gerne via Mastodon: [@arrrrrmin@chaos.social](https://chaos.social/@arrrrrmin) oder Bluesky: 
[@arrrrrmin.bsky.social](https://bsky.app/profile/arrrrrmin.bsky.social) machen. 

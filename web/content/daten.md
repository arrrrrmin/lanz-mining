---
title: "Daten"
date: "2025-01-17T15:14:33+01:00"
draft: false
---

Der Code zum Projekt ist auf GitHub veröffentlicht. Hier versuch ich eine Non-Techi-Einsicht zu geben.

## Kann ich diesen Daten trauen?

An den Daten ist nichts verändert worden. Lanz Mining interpretiert lediglich die vom ZDF veröffentlichten 
Daten. Wenn man sich fragt, wo die Daten genau herkommen, die kommen aus der 
[ZDF-Mediathek](https://www.zdf.de/gesellschaft/markus-lanz/). In einigen Außnahmen, wurden Daten 
nachgereicht. Das ist aber nur der Fall, wenn die Informationen in der Mediathek nicht verfügbar waren.
Ein Beispiel: *"Rafael Laguna de la Vera"* hatte in einer Sendung keine Rolle, da wird dann eine 
(*"SPRIN-D Direktor"*) vergeben.

Der Quellcode ist öffentlich verfügbar und kann gerne überprüft werden. Wir sind alle Menschen, man kann 
nicht ausschließen das es Fehler im Code oder der Nachverarbeitung gibt. In dem Fall wäre ich sehr Dankbar
wenn ein dazu ein <a href="https://github.com/arrrrrmin/lanz-mining/issues">Issue</a> angelegt wird.

## Welche Daten werden benutzt?

Eine Sendung besteht aus:
* `Titel`
* `Beschreibung`
* `Länge`
* `Datum`
* `N` Gäste

Eine geladene Person, besteht in den Daten aus:
* `Name`
* `Rolle`, in welcher Funktion ist eine Person geladen
* `Beschreibung/Aussage`, Beschreibung der Person bzw. wozu sich diese äußert

## Was ist ein Genre

Da in den Daten nur die unverarbeiteten Rollen, verfügbar sind, gibt es arbiträr viele Rollen.
Damit lässt sich kein Überblick über die Daten geben. Deshalb werden Rollen in Genre zusammengefasst.
Technisch ist das eine einfache Gruppierung.

Als Beispiel werden die Rollen "CDU-Politikerin", "Vizekanzler" oder "Landrätin (parteilos)" im Genre
`Politik` zusammengefasst. Das wird von der [*Circle-Packing*-Visualisierung](/) auch graphisch 
dargestellt.

## Woher kommen Infos zu Medien und Parteien

### Medien

Informationen zu Medien werden nur für Personen des Genres `Journalismus` vergeben. Nicht jede Journalist*in
kann einem Medium zugeordnet werden. Die Information kann in `Rolle` und `Beschreibung/Aussage` gefunden werden,
das ist aber nicht immer der Fall. Die Daten der Mediathek sind nur phasenweise konsistent.
Beispiel: "Die Journalistin des "Spiegel", außert sich zu ...", deutet auf den "Spiegel" als Publikationsmedium 
hin.

### Parteien

Für Parteimitgliedschaften gibt es ein Register, das sich hauptsächlich aus der Wikipedia bedient. 
Eine Parteimitgliedschaften hat in einigen Fällen auch ein Start und End-Datum um Fälle wie "Fabio De Masi" 
oder "Boris Palmer" zu jedem Zeitpunkt eine korrekte Mitgliedschaft zuzuordnen. Beide Politiker haben ihre jeweilige
Partei zu einem Zeitpunkt verlassen. Auch das Register ist
im Code verfügbar.


## Warum fehlen die neusten Sendungen?

Leider sind noch nicht alle Schritte, von Daten werden gefunden, bis zur Veröffentlichung auf Lanz-Mining
durchautomatisiert. Einige Schritte sind leider (noch) manuell, deshalb muss für eine gute Datenqualität
noch jemand düber schauen. Dafür ist auch nicht immer Zeit. 

Wer Ideen hat Parteimitgliedschaften zu automatisieren, bitte schreib mir in einer DM auf Mastodon, oder 
öffne ein Issue auf Github. Würd mich freuen.

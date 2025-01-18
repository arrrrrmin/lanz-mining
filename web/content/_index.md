---
title: "Lanz Mining"
date: 2023-01-01T08:00:00-07:00
draft: false
preview: og-lanz-mining-img.png
previewAlt: "Eine cicle packing Visualisierung der Markus Lanz Daten. Kreise zeigen die Genres der Lanz-Gäste. Politik, Journalismus usw."
---

*Die Person ist aber ständig bei Lanz!?* - Hier kannst du das Gefühl mit den Fakten abgleichen. Lanz-Mining ist ein kleiner Service der dir hilft deine Vermutung mit realen Daten abzugleichen. Mit gesammelten Daten aus der Mediathek kann man nachsehen, wer, welche Parteien oder Medienhäuser bei Lanz sitzen. Aus Platzgründen werden hier nur die Top 16 nach Auftritten angezeigt.

<div class="flex flex-col xs:flex-row justify-between py-2"><span class="isolate inline-flex roundd-md shadow-sm"><button type="button" value="gäste" id="greeting-vis-button" class="relative inline-flex items-center rounded-l-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-10">
Top Gäste
</button>
<button type="button" value="parteien" id="greeting-vis-button" class="relative -ml-px inline-flex items-center bg-white px-3 py-2 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-10">
Top Parteien
</button>
<button type="button" value="medien" id="greeting-vis-button" class="relative -ml-px inline-flex items-center bg-white px-3 py-2 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-10">
Top Medien
</button>
<button type="button" value="genres" id="greeting-vis-button" class="relative -ml-px inline-flex items-center rounded-r-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-10">
Top Genres</button></span><div class="relative inline-block text-right"><div><button type="button" class="inline-flex w-full justify-center gap-x-1.5 rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50" id="greetings-vis-option-button" aria-expanded="true" aria-haspopup="true">
<svg class="-mr-1 size-5 text-gray-400" viewBox="0 0 20 20" fill="currentcolor" aria-hidden="true" data-slot="icon"><path fill-rule="evenodd" d="M5.22 8.22a.75.75.0 011.06.0L10 11.94l3.72-3.72a.75.75.0 111.06 1.06l-4.25 4.25a.75.75.0 01-1.06.0L5.22 9.28a.75.75.0 010-1.06z" clip-rule="evenodd"></path></svg>
Jahr</button></div><div id="greetings-vis-options-div" class="absolute right-0 z-10 mt-2 origin-top-right rounded-sm bg-white shadow-lg ring-1 ring-black/5 focus:outline-none" style="display:none" role="menu" aria-orientation="vertical" aria-labelledby="menu-button" tabindex="-1"><div id="greetings-vis-option-list" class="py-1"><button type="button" name="2024" value="2024" id="menu-item-0" class="block px-4 py-2 text-sm text-gray-700" role="menuitem" tabindex="-1">2024</button><button type="button" name="2023" value="2023" id="menu-item-1" class="block px-4 py-2 text-sm text-gray-700" role="menuitem" tabindex="-1">2023</button><button type="button" name="2022" value="2022" id="menu-item-2" class="block px-4 py-2 text-sm text-gray-700" role="menuitem" tabindex="-1">2022</button><button type="button" name="Alle" value="Alle" id="menu-item-3" class="block px-4 py-2 text-sm text-gray-700" role="menuitem" tabindex="-1">Alle</button></div></div></div></div>
{{< js id="main-vis" src="js/main-vis.js" class="pb-10" >}}
    mainVisualization("main-vis", "data.csv");
{{< /js >}}

Warum ein Genre? Bei Lanz werden viele unterschiedliche Menschen in verschiedenen Rollen eingeladen. Damit das Ganze visualisierbar wird, werden die Rollen, die den Gästen einer Sendung zugeschrieben werden, zu Genren zusammengefasst. So gewinnt man eine bessere Übersicht über die Rollen, in denen die Gäste eingeladen sind. Die Circle Packing-Visualisierung zeigt die Größe der Cluster basierend darauf, wie oft eine Rolle für eine Person vergeben wurde. Nicht wundern, Gäste können in unterschiedlichen Rollen zu unterschiedlichen Sendungen eingeladen worden sein.

{{< js id="genre-vis" src="js/genre-circle.js" class="border border-slate-300 rounded-md my-2" >}}
    genreVisualization("genre-vis", "data.csv")
{{< /js >}}

Wenn man weiter in die Daten hinein schaut, gibt es dort auch Beschreibungen zu jeder geladenen Person. In dieser Beschreibung, wir die Person kurz vorgestellt und wozu sie sich äußern möchte. Dabei merkt man schnell das das Wort Expert*in häufig auftritt. Also kann man auch das analysieren. Expert*innen werden je nach Ankündigung in der Mediathek einem Thema zugeordnet. Auch hier kann eine Person über die Zeit für mehr als nur ein Thema geladen werden.

{{< js id="experts-vis" src="js/experts-vis.js" class="my-2" >}}
    expertsVisualization("experts-vis", "data.csv")
{{< /js >}}

Die Visualisualisierung der Expert*innen pro Themngebiet, ist beschränkt auf die Top 16, sonst wird das Ganze zu lang und unübersichtlich. Funfakt an dieser Stelle, der Award als Expert*in der der Expert*innen, wird zur Zeit von Sascha Lobo gehalten. Er hat die meisten Themengebiete abgedenkt.
Das Projekt ist auf [GitHub](https://github.com/arrrrrmin/lanz-mining) verfügbar, würde mich also über Ideen oder Erweiterungen freuen. Sonstige Ideen, Kommentare und alles Andere gerne auch auf [Mastodon](@arrrrrmin@chaos.social) oder wenn es sein muss auch [Bluesky](https://bsky.app/profile/arrrrrmin.bsky.social).
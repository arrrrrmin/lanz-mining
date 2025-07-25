const requestedFeatures = [
    { name: "Häufig angeführte Fakten & Formulierungen", done: false, description: "Welche Fakten werden zum Einordnen von Aussagen häufig herangezogen & gibt es gleichförmige Formulierungspattern." },
    { name: "Parteien vs. Faktenchecks", done: false, description: "Gibt es Tendenzen zu messen, ob einige Parteien vermehrt Fakten checks produzieren?" },
    { name: "Themen Verteilungen", done: false, description: "Beschreibung der Episoden enthalten ein oder mehrere Themen." },
    { name: "Redezeit analysieren", done: false, description: "Videos herunterladen, durch ein $SpeechToTextModel (whisper) und Redezeiten messen." },
    { name: "Talkenden-Liste", done: true, description: "'Top N Talkende' vollständige Liste in navigierbar.", slug: "talkers" },
    { name: "Parteiauftritte über die Zeit", done: true, description: "Trends zu eingeladenen Parteien über die Zeit visualisieren." }
].sort((a, b) => b.done - a.done)

export default requestedFeatures;
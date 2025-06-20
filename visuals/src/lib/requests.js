const requestedFeatures = [
    { name: "Häufig angeführte Fakten & Formulierungen", exists: false, description: "Welche Fakten werden zum Einordnen von Aussagen häufig herangezogen & gibt es gleichförmige Formulierungspattern." },
    { name: "Parteien vs. Faktenchecks", exists: false, description: "Gibt es tendenzen zu messen, ob einige Parteien vermehrt Fakten checks produzieren?" },
    { name: "Themen Verteilungen", exists: true, description: "Beschreibung der Episoden enthalten ein oder mehrere Themen." },
    { name: "Redezeit von Politiker:innen", exists: false, description: "Videos herunterladen, durch ein $SpeechToTextModel (whisper) und Redezeiten messen." },
    { name: "Talkenden-Liste in durchsuchbar", exists: true, description: "TopTalkers plot in durchsuchbar und navigierbar." },
]

export default requestedFeatures;
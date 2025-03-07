<script>
    import HeaderNav from "../../components/HeaderNav.svelte";
    import Meta from "../../components/Meta.svelte";
    import SocialMediaFrequency from "../../components/visual/SocialMediaFrequency.svelte";

    let meta = {
        image: {
            url: "https://arrrrrmin.github.io/lanz-mining/web-app-manifest-512x512.png",
            width: 512,
            height: 512,
            alt: "Rectangle of different sizes, symbolizing the market share of main german talkshow formats analysed by the project.",
        },
    };
    let openGraph = {
        type: "website",
        title: "Lanz Mining, Faktenchecks",
        description:
            "Daten der fünf großen ÖR-Talkshows. Ein kleiner Umweg zum Thema Faktenchecks in öffentlich rechtlichen Talkshows.",
        url: "https://arrrrrmin.github.io/lanz-mining/faktenchecks",
    };

    let { data } = $props();
</script>

<Meta
    title="Lanz Mining, Faktenchecks"
    description="Daten der fünf großen ÖR-Talkshows. Ein kleiner Umweg zum Thema Faktenchecks in öffentlich rechtlichen Talkshows."
    image={meta.image}
    url="https://arrrrrmin.github.io/lanz-mining/faktenchecks"
    siteUrl="https://arrrrrmin.github.io/lanz-mining/"
    {openGraph}
    twitter="true"
/>
<HeaderNav />
<main>
    <h2>Ein wenig über Faktenchecks</h2>
    <p>
        Wie viele andere, war auch ich Ende Januar bzw. Anfang Februar oft auf
        der Straße demonstrieren. Gegen die Zusammenarbeit der CDU/CSU mit der
        AfD, Rechtsruck, ungleiche Behandlung von Menschen aufgrund ihrer
        Herkunft und gegen so Vieles mehr. Mein Telefon explodierte aber umso
        mehr, als an einem dieser Demowochenenden
        <b>Caren Miosga</b> eine Sendung mit Alice Weidel machte.
    </p>
    <p>
        Zwischenanmerkung zu den Daten: Aus Gründen ... werden Code und Daten
        mit der Zeit zu <a target="_blank" href="https://codeberg.org/"
            >Codeberg.org</a
        >
        wandern. Der Code für diese Auswertung ist
        <a
            target="_blank"
            href="https://codeberg.org/arrrrrmin/factchecking-vs-attention/"
            >hier</a
        > zu finden. Dort liegen auch die Rohdaten.
    </p>
    <p>
        Seit dem interessierte mich, auch im Kontext der Wahldebatten, eine
        Frage:
        <i
            >"Wie lange hat man wohl Zeit um als Redaktion einen Faktencheck
            nachzuliefern"</i
        >.
        <b
            >Disclaimer: Ich habe nie in einer Redaktion gearbeitet und stelle
            keine Vermutungen über die Arbeit von FaktencheckerInnen an</b
        >
        Die Antwort können also nur professionelle JournalistInnen final liefern.
        Mich hat es aber gereizt diese Frage auf der Basis von Daten zu beantworten.
        Wenn man ein wenig in der Bluesky- oder Mastodon-API herumstochert, kommt
        man tatsächlich schnell an Informationen und kann sich einen Überblick verschaffen:
    </p>
    <SocialMediaFrequency {data} />
    <p>
        Die Sendung wurde um 22:15 Uhr ausgestrahlt, und hat eine Stunde
        gedauert. In diesem Bereich sind die meisten Kommentare getippt worden.
        Hier ist die Aufmerksamkeit also besonders hoch. Bis nach ca 2:00 Uhr
        hält sie weiter an und dünnt dann schnell aus. Erst ab 6 Uhr am Morgen
        beginnt der Zyklus, wenn auch abgeschwächt, wieder. Irre Erkenntnis:
        "Viele Menschen schlafen Nachts". Ab 6 Uhr beginnen Menschen wohl,
        Themen des Vortags, vielleicht auch mit Verspätung erneut zu
        kommentieren. Das geht mit niedriger Frequenz bis ca. 18 Uhr weiter.
        <b
            >Der eingezeichnete Zeitpunkt der Veröffentlichung des Faktenchecks,
            ist die frühest anzunehmende Veröffentlichung.</b
        >
        Sie beruht auf einer Anmerkung im Faktencheck selbst. Um ein Zitat von A.
        Weidel zu checken, musste die Redaktion von Miosga die NZZ konsultieren.
        <i
            >"Auf Anfrage unserer Redaktion erklärte die NZZ Weidels Vorwurf zu
            prüfen. Bis Montagnachmittag, 16:00Uhr, lag unserer Redaktion noch
            kein Ergebnis vor"</i
        >
        <a
            target="_blank"
            href="https://www.daserste.de/information/talk/caren-miosga/sendung/was-fuer-ein-deutschland-wollen-sie-frau-weidel-100.html"
            >(Stand 6.3.2025)</a
        >.
    </p>
    <p>
        Im Zeitstrahl kann man sehen wie das Aufmerksamtkeitspotential Stunde
        für Stunde geringer wird und zerfasert. In diesem konkreten Fall, kann
        man also davon ausgehen, das ein Faktencheck bis spätestens 6 bzw. 7 Uhr
        am Folgetag verfügbar sein sollte. Diese Zeit wäre nötig, um in die
        Aufmerksamkeitsspanne von sozialen Medien (hier Bluesky / Mastodon) vor
        zu dringen. Während die Sendung läuft ist ein vollständiger Faktencheck
        vermutlich nur mit ausreichenden Ressourcen möglich. Für jede dieser
        Shows einen "Live"-Faktencheck anzubieten wäre ziemlich aufwändig, aber
        sicher die einzige Garantie dafür zu sorgen, das potentiell gefährliches
        Gedankengut zumindest eingeordnet wird.
    </p>
    <p>
        Soziale Medien sind nur ein Indikator für das Aufmerksamkeitspotential,
        das einem Faktencheck gewidmet wird. Die wichtigste Metrik wären die
        direkte Aufmerksamkeit für den Faktencheck selbst. Ob ein Faktencheck
        rechtzeitig veröffentlicht wird oder nicht, ist unerheblich wenn er
        ohnehin niemanden erreicht. Sendungen wie Maischberger oder Hart aber
        Fair verlinken auf der Webseite ihres Formats auf einen seperaten
        Faktencheck. Damit lassen sich die Klickzahlen bequem erheben. Wir
        kennen die Klickzahlen nicht und wir wissen nicht wer diese Klicks sind.
        Es existiert also die Möglichkeit, dass diese Fakten nie gelesen werden
        und lediglich redaktioneller Überhang sind.
    </p>
</main>

<style lang="postcss">
    @reference "tailwindcss/theme";
</style>

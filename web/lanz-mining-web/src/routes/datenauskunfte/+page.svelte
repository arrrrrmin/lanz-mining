<script>
    import HeaderNav from "../../components/HeaderNav.svelte";
    import Meta from "../../components/Meta.svelte";

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
        title: "Lanz Mining, Datenauskünfte",
        description:
            "Daten der ÖR-Talkshows, Markus Lanz, Maischberger, Maybrit Illner, Caren Miosga und Hart aber fair. Die Datenauskünfte zeigen dir welche Daten vorhanden und wo die so her kommen.",
        url: "https://arrrrrmin.github.io/lanz-mining/datenauskunfte",
    };
</script>

<Meta
    title="Lanz Mining, Datenauskünfte"
    description="Daten der ÖR-Talkshows, Markus Lanz, Maischberger, Maybrit Illner, Caren Miosga und Hart aber fair. Die Datenauskünfte zeigen dir welche Daten vorhanden und wo die so her kommen."
    image={meta.image}
    url="https://arrrrrmin.github.io/lanz-mining/datenauskunfte"
    siteUrl="https://arrrrrmin.github.io/lanz-mining/"
    {openGraph}
    twitter="true"
/>
<HeaderNav />
<main>
    <h1>Datenauskünfte</h1>
    <p>
        Lanz Mining beschäftigt sich damit Daten zu den geladenen Personen der
        Talkshows (Talkende) aufzuzeichnen und in Visualisierungen
        bereitzustellen. Vorläufig ist der Zeitraum von Februar 2024 bis Februar
        2025 verfügbar. Jede Sendung besteht aus mehreren Informationshäufchen
        und orientiert sich an den Talkenden. Je nach Format sind
        unterschiedliche Informationen verfügbar. Die Crawler können nur die
        Daten finden, die auch veröffentlicht sind. Es gibt also leider
        <strong
            >keine Informationen darüber welche Personen für eine Sendung
            angefragt wurden</strong
        >. Diese Daten haben nur die Redaktionen von ZDF und ARD selbst. Dieses
        Projekt ist privat entstanden und die Resourcen sind begrenzt, also
        wurde auch darauf verzichtet die Sendungen selbst herunterzuladen und zu
        analysieren. Da würde es vermutlich auch rechtliche Probleme geben. Lanz
        Mining <strong>gespeichert also keine Videodaten der Sendungen</strong>.
    </p>
    <h2>Open Source</h2>
    <p>
        Lanz Mining ist vollständig open source und auf <a
            href="https://github.com/arrrrrmin/lanz-mining"
            target="_blank">Github</a
        >
        verfügbar. Für technisch Interessierte gibt es dort auch eine Anleitung,
        um selbst Daten zu sammeln und eigene analysen zu starten.
    </p>

    <h2>Übersicht</h2>
    <p>
        Die folgende Tabelle zeigt welche Informationen auf den Webseiten der
        Talkshowformate verfügbar ist, welche nicht und welche für Lanz Mining
        genutzt werden.
    </p>
    <table class="table-auto">
        <thead>
            <tr>
                <th></th>
                <th>Markus Lanz</th>
                <th>Maischberger</th>
                <th>Maybrit Illner</th>
                <th>Caren Miosga</th>
                <th>Hart aber fair</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <!---->
                <td>Beschreibung der Sendung</td>
                <td>+</td>
                <td>+</td>
                <td>+</td>
                <td>+</td>
                <td>+</td>
            </tr>
            <tr>
                <td>Länge der Sendung</td>
                <td>+</td>
                <td>+</td>
                <td>+</td>
                <td>+</td>
                <td>+</td>
            </tr>
            <tr>
                <td>Datum der Sendung</td>
                <td>+</td>
                <td>+</td>
                <td>+</td>
                <td>+</td>
                <td>+</td>
            </tr>
            <tr>
                <td>Faktencheck</td>
                <td>-</td>
                <td>(+)</td>
                <td>+</td>
                <td>+</td>
                <td>+</td>
            </tr>
            <tr>
                <td>Name der Talkenden</td>
                <td>+</td>
                <td>+</td>
                <td>+</td>
                <td>+</td>
                <td>+</td>
            </tr>
            <tr>
                <td>Rolle der Talkenden</td>
                <td>+</td>
                <td>(-)</td>
                <td>+</td>
                <td>+</td>
                <td>+</td>
            </tr>
            <tr>
                <td>Ankündigung Talkender</td>
                <td>+</td>
                <td>(-)</td>
                <td>-</td>
                <td>+</td>
                <td>-</td>
            </tr>
        </tbody>
    </table>
    <p>
        Bei Maischberger fehlen die meisten Daten, weil es hier nicht ohne
        zusätzliches speichern von Bildern und OCR möglich ist diese Daten zu
        befreien. Dafür fehlt allerdings gerade noch die Kapazität um diese
        zusätzlichen Features zu bauen.
        <br />
        Faktenchecks werden im übrigen noch nicht ausgewertet, das ist ein zukünftiges
        Projekt, das wird sich dann aber auch nur mit dem Überprüfen von Fakten beschäftigen.
    </p>
    <h2>Anmerkungen</h2>
    <p style="padding-bottom: 0;">
        Aus den oben genannten Informationen werden weitere herausgelesen,
        sodass am Ende folgendes genutzt werden kann.
    </p>
    <table class="table-auto">
        <thead>
            <tr>
                <th style="text-align: left">Variable</th>
                <th style="text-align: left">Description</th>
                <th style="text-align: left">Data type</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="text-align: left"><code>episode_name</code></td>
                <td style="text-align: left">Name der Sendung</td>
                <td style="text-align: left"><code>string</code></td>
            </tr>
            <tr>
                <td style="text-align: left"><code>date</code></td>
                <td style="text-align: left">Datum der Veröffentlichung</td>
                <td style="text-align: left"><code>date</code></td>
            </tr>
            <tr>
                <td style="text-align: left"><code>description</code></td>
                <td style="text-align: left">Beschreibung der Sendung</td>
                <td style="text-align: left"><code>string</code></td>
            </tr>
            <tr>
                <td style="text-align: left"><code>factcheck</code></td>
                <td style="text-align: left"
                    >Existiert ein zugehöriger Faktencheck</td
                >
                <td style="text-align: left"><code>boolean</code></td>
            </tr>
            <tr>
                <td style="text-align: left"><code>length</code></td>
                <td style="text-align: left">Länge der Sendung</td>
                <td style="text-align: left"><code>number</code></td>
            </tr>
            <tr>
                <td style="text-align: left"><code>name</code></td>
                <td style="text-align: left">Name der Talkenden</td>
                <td style="text-align: left"><code>string</code></td>
            </tr>
            <tr>
                <td style="text-align: left"><code>role</code></td>
                <td style="text-align: left"
                    >Rolle der Talkenden, wie vom Format veröffentlicht</td
                >
                <td style="text-align: left"><code>string</code></td>
            </tr>
            <tr>
                <td style="text-align: left"><code>message</code></td>
                <td style="text-align: left">Ankündigung einer Talkenden</td>
                <td style="text-align: left"><code>string</code></td>
            </tr>
            <tr>
                <td style="text-align: left"><code>talkshow</code></td>
                <td style="text-align: left">Name der Talkshow</td>
                <td style="text-align: left"><code>string</code></td>
            </tr>
            <tr>
                <td style="text-align: left"><code>party</code></td>
                <td style="text-align: left">Parteimitgliedschaft</td>
                <td style="text-align: left"><code>string</code></td>
            </tr>
            <tr>
                <td style="text-align: left"><code>group</code></td>
                <td style="text-align: left">Gruppen zugehörigkeit</td>
                <td style="text-align: left"><code>string</code></td>
            </tr>
            <tr>
                <td style="text-align: left"><code>media</code></td>
                <td style="text-align: left">
                    Medienhaus wenn Talkende teil der Gruppe "Journalismus"
                </td>
                <td style="text-align: left"><code>string</code></td>
            </tr>
        </tbody>
    </table>
</main>

<style lang="postcss">
    @reference "tailwindcss/theme";
    h1 {
        @apply max-w-2xl mx-auto pt-10 pb-6 font-bold text-3xl text-gray-800;
    }
    table {
        @apply block overflow-auto size-full divide-y divide-gray-300 max-w-2xl mx-auto py-6 text-base text-gray-800 leading-7;
    }
    th {
        @apply py-3.5 text-center text-base text-gray-900;
    }
    tbody {
        @apply divide-y divide-gray-200;
    }
    td {
        @apply whitespace-nowrap py-2 pl-2 pr-3 text-center text-base text-gray-900 sm:pl-0;
    }
</style>

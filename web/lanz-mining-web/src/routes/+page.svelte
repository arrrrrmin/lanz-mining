<script>
    import { base } from "$app/paths";
    import Meta from "../components/Meta.svelte";
    import HeaderNav from "../components/HeaderNav.svelte";
    import ReadingExample from "../components/ReadingExample.svelte";
    // import Quote from "../components/Quote.svelte";
    import Reference from "../components/Reference.svelte";

    import MarketShare from "../components/visual/MarketShare.svelte";
    import MainSpeakers from "../components/visual/MainSpeakers.svelte";
    import PartyDistribution from "../components/visual/PartyDistribution.svelte";
    import GroupsDiverging from "../components/visual/GroupsDiverging.svelte";
    import MediaShare from "../components/visual/MediaShare.svelte";
    import TalkDurations from "../components/visual/TalkDurations.svelte";
    import FrequencyCompare from "../components/visual/FrequencyCompare.svelte";

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
        title: "Lanz Mining, öffentlich rechtliche Talkshow Daten",
        description:
            "Daten der ÖR-Talkshows, Markus Lanz, Maischberger, Maybrit Illner, Caren Miosga und Hart aber fair. Ein Projekt zum transparenten Umgang mit Informationen des öffentlich Rechtlichen Rundfunks.",
        url: "https://arrrrrmin.github.io/lanz-mining/",
    };
    // Get data from +page.server.js
    let { data } = $props();
    let formatOrder = $state({});
    let numGuests = $state(0); // Value is filled by MainSpeaker component
    let appearsTotal = $state(0); // Value is filled by FrequencyCompare component
    let afdPercentage = $state(0); // Value is filled by PartyDistribution component
</script>

<Meta
    title="Lanz Mining, öffentlich rechtliche Talkshow Daten"
    description="Daten der ÖR-Talkshows, Markus Lanz, Maischberger, Maybrit Illner, Caren Miosga und Hart aber fair. Ein Projekt zum transparenten Umgang mit Informationen des öffentlich Rechtlichen Rundfunks."
    image={meta.image}
    url="https://arrrrrmin.github.io/lanz-mining/"
    siteUrl="https://arrrrrmin.github.io/lanz-mining/"
    {openGraph}
    twitter="true"
/>
<HeaderNav />
<main>
    <h2>
        Daten zu öffentlich Rechtlichen Talkshows
        <br />
        verfügbar machen, denn die gehören uns allen. Öffentliches Geld, öffentliche
        Daten!
    </h2>
    <p>
        Aktuell (Februar 2025) haben wir keine Daten. Nichts. Wenn wir eine
        Antwort auf die Frage: "Brauchen wir diese Talkshows wirklich?"
        gesellschaftlich informiert diskutieren wollen, brauchen wir
        Bürger*innen die nötigen Daten. Im übrigen kann die Betonung auf 'diese'
        oder 'Talkshows' liegen.
    </p>
    <h3>Welche Daten?</h3>
    <p>
        Auf den Webseiten der Formate von <i>Markus Lanz</i>,
        <i>Maybrit Illner</i>, <i>Maischberger</i>, <i>Caren Miosga</i> und
        <i>Hart aber fair</i> werden unterschiedliche Informationen
        (Sendungsbeschreibungen, Name, Informationen oder Aussagen von Talkenden
        oder Sendungslängen) veröffentlicht und die kann man speichern. Für
        technische Details oder wo genau die Daten herkommen, gibt es
        <a href="{base}/datenauskunfte">Datenauskünfte</a>.
    </p>
    <h3>Hinweise zu den Grafiken</h3>
    <p>
        Die Grafiken beziehen sich auf den Zeitraum von Februar 2024 bis Februar
        2025. Jede Grafik hat darunter eine kleines "Lesebeispiel zur Grafik".
        Manche Grafiken enthalten einen Button (“Seit Koalitionsbruch”), um den
        Datenzeitraum von Februar 2024 auf November 2024 umzuschalten.
        Lesebeispiele beziehen sich auf den ganzen Datenzeitraum.
    </p>
    <h2>Talkshow-Markt des ÖR</h2>
    <p>
        Erst mal die banalen Informationen: <i>Lanz</i> veröffentlicht drei,
        Maischberger zwei und <i>Illner</i>, <i>Miosga</i> und
        <i>Hart aber fair</i> jeweils ein Mal die Woche. Also teilt sich der Talkshow-Markt
        im öffentlich rechtlichen Rundfunk wie folgt auf:
    </p>
    <MarketShare {data} bind:formatOrder />
    <ReadingExample>
        Markus Lanz veröffentlichte 122 Sendungen im Zeitraum zwischen Februar
        2024 und Februar 2025.
    </ReadingExample>
    <p>
        In der Spitze kann es im ÖR vorkommen, dass in einem einzelnen Monat
        zwischen 1,2 und 1,5 Tage reine Sendungslänge an Talkshows aufgezeichnet
        und ausgestrahlt werden. Zum Vergleich wären das in einem Monat 3,5 bis
        4,3 erste Staffeln von Squid Game. Die erste Staffel von Squid Game
        kommt auf 494 Minuten. <br />
        Im Sommer wird weniger geredet, hier wird Urlaub vom Sprechformat gemacht,
        während der Herbst die Talk-Hochsession zu sein scheint.
    </p>
    <TalkDurations {...{ data: data, formatOrder: formatOrder }} />
    <ReadingExample
        >September 2024 sendeten die fünf größten ÖR-Talkshows gemeinsam 2154
        Minuten, das sind 35,9 Stunden oder 1,5 Tage Sendezeit. Den größten
        Anteil daran hat Markus Lanz, gefolgt von Maischberger, Hart aber fair
        und Miosga.
    </ReadingExample>
    <h2>Parteibücher in Talkshows</h2>
    <p>
        Der Umgang mit der AfD ist auch in Talkshows ein Thema. Am Tag der bis
        dato größten Proteste in Deutschland gegen Rechts seit Januar 2024
        (Correctiv-Recherche zu Remigration), am 02.02.2025, lädt <i
            >Caren Miosga</i
        > Alice Weidel in ihre Talkshow ein und gibt ihrem Weltbild Raum. Dieser
        Teil des Projekts soll helfen, den Ist-Zustand zu beschreiben, damit wir
        uns als Bürger*innen Gedanken machen können, wie das weiter geht oder ob
        wir diese Formate überhaupt brauchen.
    </p>
    <PartyDistribution {...{ data: data, formatOrder: formatOrder }} />
    <ReadingExample>
        Die Grünen sind auf Platz 3 in der Sendung Maischberger und stellen 16%
        aller Politiker, die in der Sendung zwischen Februar 2024 und Februar
        2025 eingeladen wurden.
    </ReadingExample>
    <h3>Daten im Zeitraum seit Februar 2024</h3>
    <p>
        Die AfD kommt über das Jahr 2024 auf maximal 4% bei <i>Caren Miosga</i>.
        Etwas häufiger, obwohl jünger, kommt das BSW auf bis zu 8%, bzw 7%
        Anteil der politischen Vertreter*innen bei Hart aber fair. Doch in allen
        Formaten liegen SPD und CDU auf den ersten beiden Plätzen. Unabhängig
        vom Format kommen SPD und CDU/CSU gemeinsam auf 50% aller politischen
        Talker*innen.
    </p>
    <h3>Betrachtung seit Koalitionsburch</h3>
    <p>
        Betrachtet man nur den Zeitraum zwischen November 2024 und Februar 2025,
        kommt die AfD in fast jedem Format auf 7%. <i>Hart aber fair</i> bietet
        die ausgewogenste Darstellung der Parteien. Wobei die CSU keine Anteile
        hat. Die Gründe dafür sind nicht bekannt. Vielleicht wurden sie
        eingeladen und haben abgelehnt, vielleicht auch nicht. Während die CSU
        bei <i>Hart aber fair</i> zu kurz kommt, bekommt sie überraschend viel
        Raum bei <i>Maybrit Illner</i>. Gleichzeitig sind auch die Grünen häufig
        als Gegenpol bei <i>Illner</i> eingeladen. Etwas sehr unausgewogen gibt das
        ZDF bei Frau Illner 42% des politischen Raums in ihrer Sendung an die Union.
    </p>
    <h2>Wer spricht denn da?</h2>
    <p>
        Mit den Daten aus dem Projekt können wir uns ansehen, wer in den
        ÖR-Talkshow oft zu Wort kommt. Nachfolgend eine sortierte Liste der Top
        20 Gäste über alle Shows. Die vollständige Grafik würde {numGuests} Talkende
        umfassen, also werden nur die Top 20 dargestellt. Eine vollständige Liste
        wird bald durchsuchbar bereitgestellt. Inhaltlich sticht sofort Platz 1 Elmar
        Theveßen ins Auge. Der Fernsehjournalist vom ZDF ist Amerika-Korrospondent
        und führt die Rangliste fast ausschließlich durch Auftritte bei Markus Lanz
        an. Damit wird auch die erste Grafik noch einmal unterstützt und zeigt die
        Sendefrequenz, die dieses Format entwickelt hat.
        <br />
        Ebenso bemerkenswert, dass unter den Top 20 Talkenden nur eine einzige Person
        ist, die weder einer Partei zugehört, noch als Journalist*in arbeitet. Diese
        Person ist Carlo Marsala, der häufig als Militärexperte geladen wird, um
        geostrategische Überlegungen oder Situationen zu erklären. Wegen dem Ukraine-Krieg
        ein sehr gefragter Mann.
    </p>
    <MainSpeakers {data} bind:numGuests />
    <ReadingExample>
        Jede Zeile der Grafik entspricht einem Talkenden. Die Balken entsprechen
        den Formaten. Fabrige Kreise neben an den Namen zeigen die Farbe der
        Partei an. Jens Spahn ist also der Top Talkshow-Experte aus der CDU und
        trat sechs mal bei Lanz und drei mal bei Maybrit Illner auf.
    </ReadingExample>
    <p>
        Da es wie erwähnt schwierig ist alle Talkenden wie oben abzubilden,
        versuchen wir mal einen Überblick zu gewinnen. Dafür kann man alle in
        den Shows Auftretenden nach der Anzahl ihrer Auftritte (über alle
        Talkshows) gruppieren. Mit diesen Gruppen können wir jetzt sehen wieviel
        Prozent der Talkenden wie häufig auftreten. Um das ganze zu vereinfachen
        nehmen wir in der ersten Grafik alle Talkenden zusammen die ein, zwei
        oder drei Mal zwischen Februar 2024 und Februar 2025 auftraten. Danach
        alle die vier Mal oder häufiger die Gelegenheit hatten in deutschen
        Talkshows zu sprechen.
    </p>
    <FrequencyCompare {data} bind:appearsTotal />
    <ReadingExample>
        Jede Grafik zeigt die gleichen Daten, aber unterschiedlich Perspektiven.
        Jedes Rechteck beschreibt eine Gruppe von Talkenden, anhand der Frequenz
        wie oft sie auftraten. (Oben) ist das erste (helle) Rechteck an, das 59%
        aller Talkenden ein mal in einer Talkshow waren. (Unten) zeigt das erste
        Rechteck, das 12% der Auftritte von Talkenden absolviert wurde, die
        insgesamt vier mal eingeladen waren.
    </ReadingExample>
    <p>
        Zuerst lässt sich zeigen, das 60% der Talkenden nur ein einziges Mal
        auftreten konnten oder durften. Nimmt man alle Talkenden zusammen, die
        drei Mal oder seltener auftraten, sind das 82% aller Personen die über
        ein Jahr auftraten, aber nur 49% der Auftritte. Die andere Seite der
        Medallie sind alle die vier mal oder häufiger auftraten. Das sind, wie
        man in der obern Grafik sehen kann nur 18% aller Talkender. Diese 18%
        nehmen aber 51% alle Auftritte ein. Damit lässt sich nummerisch zeigen,
        das es eine Minderheit ist, die sehr häufig ihre Meinung in die
        Öffentlichkeit tragen darf, während andere das entweder nicht wollen
        oder dürfen. In absoluten Zahlen sind es in einem Jahr gerade ein mal
        106 Personen, die diese 18% in allen 5 großen Talkshows ausmachen und 51%
        der insgesamt {appearsTotal} Auftritte in deutschen Talkshows aus.

    </p>
    <h2>Politiker*innen und Öffentlichkeitsarbeit</h2>
    <!--Besserer TItel-->
    <p>
        Wenn man die geladen Personen ihrer Tätigkeit nach in Gruppen einteilt,
        gewinnen wir einen Überblick über die Hintergründe der Talkenden. Die
        folgende Grafik zeigt Talkshow-Formate nach ARD und ZDF getrennt. So
        wird ein Vergleich zwischen den Sendern möglich.
    </p>
    <GroupsDiverging {data} />
    <ReadingExample>
        Jede Zeile entspricht einer Gruppe von Talkenden, die Farbe dem
        Talkformat und die Zahlen sind der prozentuale Anteil am Sender. Zum
        Beispiel entsprecht der Anteil aller Journalist*innen bei Maischberger
        12,8% aller Talkender in der ARD.
    </ReadingExample>
    <p>
        Trotz kleiner Verschiebungen zwischen ARD und ZDF, zeigt sich ein
        ziemlich einheitliches Bild. Wenn man alle Balken der beiden stärksten
        Gruppen (Politik & Journalismus) zusammennimmt, entsprechen diese knapp
        65% (ca. zwei Drittel) aller Talkenden ein. Damit teilen sich die
        übrigen 14 Gruppen 35% (ca. ein Drittel) der geladenen Plätze in den
        Talkshows. Polittalk als Format lebt von der tagesaktuellen Politik. Das
        politische Geschehen wird traditionell von Regierung, Opposition und
        Berichterstatter*innen für die Bevölkerung kommentiert. Es ist also
        logisch, dass nur ein Drittel der Expert*innen aus der Praxis besetzt
        wird.
        <br />
        Damit zeigt das Format allerdings auch seine größte Schwäche. Es ist nur
        schwer möglich, tiefere Zusammenhänge aus der Betrachtung von tages- oder
        wochenaktueller Berichterstattung zu erkennen. Der Detailgrad ist zu hoch.
        Würden die Proportionen etwas verschoben, könnten mehr Expert*innen eine
        Plattform bekommen. Damit würden Themen seltener in den politischen Grabenkämpfen
        und stärker anhand der Perspektiven von Expert*innen erkundet werden.
    </p>
</main>

<style lang="postcss">
</style>

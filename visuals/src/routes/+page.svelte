<script>
    import V0_Overview from "$lib/visualisations/V0_Overview.svelte";
    import V1_EpisodesTotal from "$lib/visualisations/V1_EpisodesTotal.svelte";
    import V2_ContentPerMonth from "$lib/visualisations/V2_ContentPerMonth.svelte";
    import V3_TalkshowsVsSquidGame from "$lib/visualisations/V3_TalkshowsVsSquidGame.svelte";
    import V4_TopTalkers from "$lib/visualisations/V4_TopTalkers.svelte";
    import V4_TopTalkersInteractive from "$lib/visualisations/V4_TopTalkersInteractive.svelte";
    import V5_InviteRatio from "$lib/visualisations/V5_InviteRatio.svelte";
    import V6_LotsOfRoles from "$lib/visualisations/V6_LotsOfRoles.svelte";
    import V7_Experts from "$lib/visualisations/V7_Experts.svelte";
    import V8_GuestDivergence from "$lib/visualisations/V8_GuestDivergence.svelte";
    import V9_TopPerGroup from "$lib/visualisations/V9_TopPerGroup.svelte";
    import V10_MediaCycle from "$lib/visualisations/V10_MediaCycle.svelte";
    import V11_MediaRepresentatives from "$lib/visualisations/V11_MediaRepresentatives.svelte";
    import V12_MatchMaking from "$lib/visualisations/V12_MatchMaking.svelte";
    import V13_MatchMakingGroups from "$lib/visualisations/V13_MatchMakingGroups.svelte";
    import V14_MatchMakingMedia from "$lib/visualisations/V14_MatchMakingMedia.svelte";
    import V15_PartyDistOverview from "$lib/visualisations/V15_PartyDistOverview.svelte";
    import V16_PartyDistFormat from "$lib/visualisations/V16_PartyDistFormat.svelte";
    import V17_PartyDistOverTime from "$lib/visualisations/V17_PartyDistOverTime.svelte";
    import Head from "$lib/components/Head.svelte";
    import Requests from "$lib/components/Requests.svelte";
    import Versions from "$lib/components/Versions.svelte";

    let { data } = $props();
    let dataInfo = $state({});
    let formatOrder = $state({});
    let groupOrder = $state({});

    $inspect(dataInfo);
</script>

<Head />
<div>
    <div class="max-w-2xl m-auto py-8">
        <h1 class="font-black text-5xl">LanzMining</h1>
        <h2 class="font-semibold text-3xl">Wer spricht denn da?</h2>
        <div class="pt-10">
            <p>
                Ein Datenprojekt, um die mediale Teilhabe in deutschen Talkshows
                des öffentlich-rechtlichen Rundfunks zu erkunden. Es werden
                gesammelte Daten aus mehr als einem Jahr untersucht und
                visualisiert. Der Fokus ist dabei mehr auf den Personen als auf
                den Themen.
            </p>
        </div>
        <dl class="pt-8 text-lg">
            <div class="flex gap-2">
                <dt>Von:</dt>
                <dd>
                    <a
                        class="underline hover:text-stone-400"
                        target="_blank"
                        href="https://chaos.social/@arrrrrmin"
                        >@arrrrrmin@chaos.social</a
                    >,
                    <a
                        class="underline hover:text-stone-400"
                        target="_blank"
                        href="https://bsky.app/profile/arrrrrmin.bsky.social"
                        >@arrrrrmin.bsky.social</a
                    >,
                </dd>
            </div>
            <div class="flex gap-2">
                <dt>Source:</dt>
                <dd>
                    [<a
                        class="underline hover:text-stone-400"
                        target="_blank"
                        href="https://codeberg.org/arrrrrmin/lanz-mining"
                        >codeberg</a
                    >,
                    <a
                        class="underline hover:text-stone-400"
                        target="_blank"
                        href="https://github.com/arrrrrmin/lanz-mining"
                        >github</a
                    >]/arrrrrmin/lanz-mining
                </dd>
            </div>
            <div class="flex gap-2">
                <dt>Talk auf der GPN23:</dt>
                <dd>
                    <a
                        class="underline hover:text-stone-400"
                        target="_blank"
                        href="https://media.ccc.de/v/gpn23-213-lanzmining-wer-spricht-denn-da-"
                        >media.ccc.de</a
                    >
                </dd>
            </div>
        </dl>
        {#if Object.keys(dataInfo).length > 0}
            <dl class="pb-2">
                <h3 class="pt-8 pb-4 text-2xl font-bold">Datenblatt</h3>
                <div class="flex gap-2">
                    <dt>Zeitraum:</dt>
                    <dd>
                        {dataInfo.timeRange.start} - {dataInfo.timeRange.end},
                        with {dataInfo.timeRange.daysTalked} shows days.
                    </dd>
                </div>
                <div class="flex gap-2">
                    <dt>Episoden:</dt>
                    <dd>
                        {dataInfo.episodes}
                    </dd>
                </div>
                <div class="flex gap-2">
                    <dt>Talkende:</dt>
                    <dd>
                        {dataInfo.guests}
                    </dd>
                </div>
                <div class="flex gap-2">
                    <dt>Rollen:</dt>
                    <dd>
                        {dataInfo.roles}
                    </dd>
                </div>
                <div class="flex gap-2">
                    <dt>Talkshowplätze:</dt>
                    <dd>
                        {dataInfo.appearances}
                    </dd>
                </div>
            </dl>
        {/if}
        <Requests />
        <Versions />
    </div>
    <hr class="max-w-2xl m-auto" />
    <div class="max-w-2xl m-auto py-8">
        <p>
            Seit Februar 2024 werden Informationen der fünf großen Talkshow <i
                >Markus Lanz</i
            >,
            <i>Maybrit Illner</i>, <i>Maischberger</i>, <i>Caren Miosga</i> und
            <i>Hart aber fair</i> aufgezeichnet. Um eine Übersicht über die
            verfügbaren Daten zu gewinnen, visualisieren wir den Zeitraum, in
            dem wir uns befinden (Februar 2024 - Mai 2025). Im folgenden Plot it
            jeder Strich ein Tag, an dem ein oder mehrere Talkshows
            veröffentlicht wurden. Überschneidungen finden am häufigsten unter
            der Woche an Dienstag, Mittwoch und Donnerstag statt. Die Shows von
            <i>Markus Lanz</i>,
            <i>Maischberger</i>
            und <i>Illner</i> finden an diesen Tagen statt.
        </p>
    </div>

    <h3 id="v0-overview" class="max-w-2xl m-auto pt-8 pb-4 text-2xl font-bold">
        Datenzeitraum im Überblick
    </h3>
    <V0_Overview {data} id={"v0-overview"} bind:dataInfo />
    <div class="max-w-2xl m-auto py-8">
        <p>
            Das regelmäßige Sendemuster wird nur von der Sommerpause in Juli und
            August unterbrochen. Auch Talkshow-Redaktionen wollen Urlaub haben.
            Wenn wir wissen, dass Markus Lanz als einziges Format drei Sendungen
            die Woche aufzeichnet, ergibt der die nächste Visualisierung Sinn.
            Sie zeigt die Episoden die pro Format im Datenzeitraum aufgezeichnet
            wurden:
        </p>
    </div>

    <h3
        id="episodes-total"
        class="max-w-2xl m-auto pt-8 pb-4 text-2xl font-bold"
    >
        Episoden pro Format
    </h3>
    <V1_EpisodesTotal {data} id={"episodes-total"} bind:formatOrder />
    <div class="max-w-2xl m-auto py-8">
        <p>
            Diese <i>Lanz' Dominanz</i> zeiht sich durch alle Daten und wird uns
            im Verlauf noch häufiger Begegnen. Im nächsten Plot sehen wir das die
            Sendefrequenz von Lanz nur im August einen leichten Dämpfer bekommt.
            Weiter lässt sich über die Minuten an Content der einzelnen Formate beobachten,
            das ARD-Formate im Juli pausieren, während das ZDF im August eine auszeit
            nimmt. So muss in einem Monat nicht vollständig auf Talkshows verzichtet
            werden.
        </p>
    </div>

    <h3
        id="content-per-month"
        class="max-w-2xl m-auto pt-8 pb-4 text-2xl font-bold"
    >
        Produzierte talk content (in Min.) pro Monat
    </h3>
    <V2_ContentPerMonth {data} id={"content-per-month"} {formatOrder} />
    <div class="max-w-2xl m-auto py-8">
        <p>
            In der Spitze kommt man in einem Monat auf 2200 Minuten Talkshow
            Content. Das ist viel und bezeugt das es wohl bedarf für
            Polit-Unterhaltung gibt. Um diese Zahlen in ein Verhältnis zu
            setzen, sieht man im nächsten Diagramm, wie viele erste Staffeln von
            SquidGame ein durchschnittlicher Talk-Content Monat betragen würde.
            So ein durchschnittlicher Monat kommt auf 3.78 erste Staffeln von
            SquidGame.
        </p>
    </div>

    <h3
        id="talkshows-vs-squidgame"
        class="max-w-2xl m-auto pt-8 pb-4 text-2xl font-bold"
    >
        Durschnittlicher Talkmonat im Vergleich
    </h3>
    <V3_TalkshowsVsSquidGame
        {data}
        id={"talkshows-vs-squidgame"}
        {formatOrder}
    />
    <div class="max-w-2xl m-auto py-8">
        <p>
            So lässt sich auch gut verstehen, wie viel einfacher es ist eine
            Talkshow zu produzieren, als ein anderes Unterhaltungsformat zu
            bespielen. Für eine Talkshow braucht man eigentlich nur n
            Expert:innen, Journalistische Unterstützung, ein oder mehrere
            Themen, ein Studio und die Produktionsmittel, die im ÖRR sicher
            ohnehin vorhanden sind. <b>Anmerkung</b>: Ich stelle Vermutungen an,
            habe nie bei einer Fernsehproduktion mitgearbeitet.
            <br />
            Die eigentlich interessanten Daten beziehen sich auf die geladenen Personen
            die in den Shows auftreten. Die Talkenden-Volkszählung ergibt im Top
            15 Ranking der am häufigsten geladenen Gäst:innen:
        </p>
    </div>

    <h3 id="top-talkers" class="max-w-2xl m-auto pt-8 pb-4 text-2xl font-bold">
        Top Talkende nach Auftritten und Formaten
    </h3>
    <!-- <V4_TopTalkers {data} id={"top-talkers"} n={15} {formatOrder} /> -->
    <V4_TopTalkersInteractive id="v4-ia" {data} />
    <div class="max-w-2xl m-auto py-8">
        <p>
            Elmar Theveßen ist der am häufigsten geladene Gast. Alleine durch
            die Auftritte bei Markus Lanz schaft er es auch ohne andere Formate
            auf Platz 1. Herr Theveßen ist USA-Korrpspondent beim ZDF und damit
            ist sehr schnell klar warum er so häufig geladen wird: Trump hat
            irgendetwas getan, oder erzählt, oder angedeutet. Medial gibt es
            ohnehin kein Entkommen vor Trump, deshalb gibt dies auf für die
            Talkshow-Landschaft. Im Übrigen besteht die List hauptsächlich aus
            Politiker:innen und Journalist:innen, wobei die paritätische
            Verteilung unter Journalist:innen deutlich feirer ist als sie es
            unter Berufspolitiker:innen ist.
            <br />
            So nett diese Grafik sein mag, sie zeigt nur 15 der {dataInfo.guests}
            Talkenden. In der nächsten Grafik erhalten wir ein Gefühl für die Verteilung
            der Gäst:innen zu Auftritten.
        </p>
    </div>

    <h3 id="invite-ratio" class="max-w-2xl m-auto pt-8 pb-4 text-2xl font-bold">
        Talkende vs. Auftritte
    </h3>
    <V5_InviteRatio {data} id={"invite-ratio"} />
    <div class="max-w-2xl m-auto py-8">
        <p>
            Die Grafik gruppiert Talkende, nach der Anzahl ihrer Auftritte. Die
            obere Skala (100%) zeigt prozentuale Anteile an allen Personen. Die
            zweite Skala bezieht sich allerdings auf die Auftritte. Durch den
            Vergleich der Größenordnungen, können wir ermitteln, wieviele
            Talkenden wieviele Auftritte wahrnehmen. So sieht man, dass Personen
            mit mehr als drei Auftritten - obwohl die Minderheit der Talkenden -
            die Mehrheit der Auftritte absolviert.
        </p>
        <p>
            Abseits einzelner Personen, können wir uns auch mit den
            zugeschriebenen Rollen beschäftigen. Hier lässt sich erkunden welche
            Expertisen und Kompetenzbereiche den Talkenden zugeordnet sind.
            Implizit wird dadurch auch ein Teil der Thematik einer Sendung
            beschrieben.
        </p>
    </div>
    <h3
        id="lots-of-roles"
        class="max-w-2xl m-auto pt-8 pb-4 text-2xl font-bold"
    >
        Rollen der Talkenden
    </h3>
    <V6_LotsOfRoles {data} id={"lots-of-roles"} />
    <div class="max-w-2xl m-auto py-8">
        <p>
            Im Plot werden im Außenbereich einige Rollen, beispielhaft gezeigt
            und zu welchen Gruppen diese zugeordnet werden können. Gruppen,
            wurden manuell definiert, basierend darauf was in den Daten zu sehen
            war. Insgesamt sind es 14 Gruppen, die zusammen mit einer speziellen <i
                >Sonstige</i
            >
            Gruppe alle Rollen der Talkenden abdenken. Die meisten unterschiedlichen
            Rollen sind den Gruppen Politik und Journalismus zuzuordnen. Nicht alle
            Rollen sind so sauber eingepflegt worden wie man es erwarten würde. Beim
            durchsuchen der Rollen fällt häufig die Rolle <i>*-Experte</i> auf. Deshalb
            folgend die fünf wichtigsten geladenen Expert:innen in deutschen Talkshows.
        </p>
    </div>
    <h3 id="main-experts" class="max-w-2xl m-auto pt-8 pb-4 text-2xl font-bold">
        Expertentum
    </h3>
    <V7_Experts {data} id={"main-experts"} />
    <div class="max-w-2xl m-auto py-8">
        <p>
            Die Nachrichtenlage wird zur Zeit leider durch Kriege dominiert und
            daher ist es recht natürlich das die ersten drei Expert:innen die
            zwei großen Konflikte thematisieren. Militärexpertise und die
            Situation in Nahost, dominieren sogar noch vor Migration und
            Automobilindustrie. Zur Klarstellung, diese Expert:innen werden auch
            in anderen Rollen angekündigt. Oben sind nur Rollen aufgeführt, die
            das Wort 'Experte' oder 'Expertin' beinhalten. Die Vertretung
            einzelner Personen in einer Gruppe, wie zum Beispiel Inneres (viele
            Polizisten und Migration), können - abseits des <i>Expertentums</i>
            - über die oben genannten Rollen hinaus gehen.
            <br />
            Da wir nun die vielen einzelnen Rollen (dataInfo.groups) in Gruppen vereinfachen
            können wir jetzt messen, welche Gruppen welches Format und welcher Sender
            in die Shows einläd.
        </p>
    </div>

    <h3
        id="guest-divergence"
        class="max-w-2xl m-auto pt-8 pb-4 text-2xl font-bold"
    >
        Gastierenden-Divergenz (nach Sender)
    </h3>
    <V8_GuestDivergence {data} id={"guest-divergence"} />
    <div class="max-w-2xl m-auto py-8">
        <p>
            Diese bunte Grafik nennt man eine divergente Darstellung. Sie wird
            in der Datenvisualisierung zum Verleich zweier Seiten verwendet. In
            diesem Fall sind das die beiden Sender ARD und ZDF, unterteilt nach
            Gruppen. Jede seite summiert sich über alle Gruppen auf 100%. Als
            Lesebeispiel kann man so feststellen, das die von <i
                >Maybrit Illner</i
            >
            geladenen Talkenden der Gruppe Wirtschaft <i>p</i>-Prozent des
            Senders ZDF ausmacht.
            <br />
            <b>Anmerkung: </b> Es lässt sich beobachten, das
            <i>Caren Miosga</i>, obwohl sie ähnlich viele Episoden wie
            <i>Illner</i>
            oder
            <i>Hart aber Fair</i> veröffentlicht, weniger % Anteile in der
            Darstellung einnimmt. Grund ist der Fakt, das <i>Miosga</i> weniger Gäste
            pro Sendung einläd, als die anderen Formate, dadurch hat sie weniger
            repräsentation im Sender. Zur Erinnerung wir messen Rollen von Talkenden,
            nicht Themen von Sendungen.
        </p>
    </div>

    <h3
        id="group-representatives"
        class="max-w-2xl m-auto pt-8 pb-4 text-2xl font-bold"
    >
        Gruppensprecher:innen
    </h3>
    <V9_TopPerGroup {data} id={"group-representatives"} bind:groupOrder />
    <div class="max-w-2xl m-auto py-8">
        <p>
            Die Darstellung zeigt uns für jede Gruppe die wichtigsten Personen.
            Gemessen daran, wieviele Auftritte diese im Datenzeitraum hatten. So
            ist jede graue Box eine Person. Die Box ist breiter, je häufiger die
            Person aufgretreten ist. Sollten mehrere Personen die gleiche Anzahl
            an Auftritte haben, werden alle gelistet.
            <br />
            Die Visualisierung, nimmt die Gruppen Politik und Journalismus aus, da
            wir deren Topvertretungen bereits im Plot der 15 häufigsten Talkshowgäste
            gesehen haben. Weiter sind diese Gruppen sehr groß und es lohnt sich
            diese isoliert zu betrachten.
        </p>
    </div>

    <h3 id="media-cycle" class="max-w-2xl m-auto pt-8 pb-4 text-2xl font-bold">
        Medienrepräsentanz nach Formaten
    </h3>
    <V10_MediaCycle {data} id={"media-cycle"} {formatOrder} />
    <div class="max-w-2xl m-auto py-8">
        <p>
            Die Darstellung die wir hier sehen können, ist eine radiale
            Baumstruktur. Diese Darstellungsart eignet sich um Hirarchien
            aufzuzeigen. Zunächst haben wir nur zwei Stufen. Im inneren Kreis
            sind die Medienhäuser, die in Talkshows eingeladen wurden, im
            äußeren die einzelnen Sendungen, wieder farblich codiert. Je breiter
            der Anteil am äußere Kreis, desto mehr Auftritte wurden von Personen
            die diesem Medienhaus zugehören absolviert. An dieser Darstellung
            können wir unter Anderem ablesen, dass Journalist:innen des ZDF bei <i
                >Lanz</i
            >,
            <i>Illner</i>
            und <i>Maischberger</i> eingeladen werden. Umgekehrt werden aber
            ARD-Korrpspondent:innen nur bei ARD-Talkshows eingeladen. Hier kann
            der Austausch zwischen den beiden ÖRR-Sendern vielleicht noch
            verbessert werden. Es lässt sich auch gut erkennen, welche
            Medienhäuser am ehesten in den Formaten vertreten sind. Diese
            Zeitungen sind in der Regel auch in allen Talksshows vertreten.
            <br />Diese Darstellung wollen wir aber noch um die konkreten
            Personen erweitern. Also fügen wir eine zusätzliche Ebene in die
            Hirarchie ein.
        </p>
    </div>

    <h3
        id="media-cycle-2"
        class="max-w-2xl m-auto pt-8 pb-4 text-2xl font-bold"
    >
        Medienrepräsentanz mit Vertreter:innen (2)
    </h3>
    <V11_MediaRepresentatives {data} id={"media-cycle-2"} {formatOrder} />
    <div class="max-w-2xl m-auto py-8">
        <p>
            Im Vergleich zur vorherigen Grafik, ist diese etwas kleinteiliger.
            Zwischen den Talkshow-Episoden und den Medienhäusern haben wir eine
            neue Ebene eingefügt, die uns zeigt wer in welchen Talkshows welches
            Medienhaus vertritt. Da diese zusätzliche Ebene die Grafik etwas
            schwerer lesbar macht, wenn wir alle Personen einblenden, sind
            weniger präsente Journalist:innen ausgeblendet.
        </p>
    </div>

    <h3
        id="match-making-pol"
        class="max-w-2xl m-auto pt-8 pb-4 text-2xl font-bold"
    >
        Matchmaking - unter Parteien
    </h3>
    <V12_MatchMaking {data} id={"match-making-pol"} />
    <div class="max-w-2xl m-auto py-8">
        <p>
            Die kommenden drei Visualisierungen beziehen sich auf die Parteien
            und beschreiben, z.B. im Fall der obrigen Darstellung, welche
            Parteien in Talkshows aufeinandertreffen. Es werden absolute Zahlen
            verwendet, in dem die Episoden gezählt werden in denen
            beispielsweise eine Politiker:in der Grünen auf einen oder mehrere
            Kollegen der CDU traf. Die Matrix gibt diese Zählungen über alle
            Parteien wieder.
        </p>
    </div>

    <h3
        id="match-making-groups"
        class="max-w-2xl m-auto pt-8 pb-4 text-2xl font-bold"
    >
        Matchmaking - Parteien & Gruppen
    </h3>
    <V13_MatchMakingGroups {data} id={"match-making-groups"} {groupOrder} />
    <div class="max-w-2xl m-auto py-8">
        <p>
            Wir können uns auch ansehen, welche Parteien wie häufig auf Personen
            mit Gruppenzugehörigkeit treffen. So kann man sehen welche Partei
            mit welcher Gruppenexpertise gematchet wird. Zum Beispiel: "Welche
            Gruppen trifft die FDP, oder CDU und wieviel Prozent aller die ein
            Partei in Talkshows traf ist das"? Hier werden allerdings wieder
            Politik und Journalismus exkludiert, da diese die größten Anteile
            einnehmen.
        </p>
    </div>

    <h3
        id="match-making-media"
        class="max-w-2xl m-auto pt-8 pb-4 text-2xl font-bold"
    >
        Matchmaking - Parteien & Medien
    </h3>
    <V14_MatchMakingMedia {data} id={"match-making-media"} />
    <div class="max-w-2xl m-auto py-8">
        <p>
            Die letzte Matchmaking Auswertung, zeigt uns welche Medienhäuser die
            Parteien in Talkshows gegenübersitzen. Hier ist bisher nur
            auffällig, das die TAZ hauptsächlich geladen wird um die CDU
            einzuordnen. Während die TAZ kaum zur Betreuung anderer Parteien
            eingeladen wird. Das könnte ein kleines Indiz sein, das es
            gelegentlich eben doch einen gewisses Konfrontatives Matchmaking
            gibt. Andererseits kann das auch immer eine Gegenüberstellung von
            Argumenten gewertet werden und ist Teil der jouranlistischen Arbeit.
        </p>
    </div>

    <h3
        id="party-invite-dist-overview"
        class="max-w-2xl m-auto pt-8 pb-4 text-2xl font-bold"
    >
        Parteibücher in Talkshows
    </h3>
    <V15_PartyDistOverview {data} id={"party-invite-dist-overview"} />
    <div class="max-w-2xl m-auto py-8">
        <p>
            In den Datenzeitraum fällt glücklicherweise auch die Bundestagswahl.
            Also können wir die Parteiverteilungen insgesamt und während der
            Bundestagswahl vergleichen. Zwischen dem gesamten Datenzeitraum und
            dem der Bundestagswahl, gibt es kaum Unterschiede. Eine Ausnahme ist
            der Anteile der AfD. Diese Partei wurde währende der Bundestagswahl
            öfter eingeladen als es zuvor der Fall war. Im folgenden die
            Verteilung der Parteipräsenz pro Formate während des Wahlkampfes.
        </p>
    </div>

    <h3
        id="party-invite-dist-format"
        class="max-w-2xl m-auto pt-8 pb-4 text-2xl font-bold"
    >
        Parteibücher während der BTW nach Format
    </h3>
    <V16_PartyDistFormat {data} id={"party-invite-dist-format"} {formatOrder} />
    <div class="max-w-2xl m-auto py-8">
        <p>
            Der größte Anteil an konservativen Politiker:innen fällt auf <i
                >Maybrit Illner</i
            >. Über alle Formate fällt auf, das CDU und SPD mit Ausnahme von
            Frau Illners Show immer an den ersten beiden Stellen landen. Das
            diese beiden Parteien am häufigsten in Talkshows sitzen, wissen wir
            bereits aus den Grafiken zum Matchmaking. Die Ergebnisse zu Caren
            Miosga sehen zuerst einmal sehr einseitig aus, allerdings hat die
            Sendung wenige Talkende pro Episode und hat während des Wahlkampfes
            wenige Folgen veröffentlicht. Die AfD war am häufigsten bei
            <i>Maischberger</i> eingeladen. Die Linke hingegen kommt am häufigsten
            bei Hart aber fair zu Wort. Die Tendenz das in der Mehrheit CDU/CSU und
            SPD in ÖRR-Talksendungen sitzen, wird sich über die Regierungsperiode
            vermutlich noch verstärken.
        </p>
    </div>
    <h3
        id="party-invite-dist-per-month"
        class="max-w-2xl m-auto pt-8 pb-4 text-2xl font-bold"
    >
        Parteibücher über die Zeit
    </h3>
    <V17_PartyDistOverTime {data} id={"party-invite-dist-per-month"} />
    <div class="max-w-2xl m-auto py-16">
        <p>
            Wir können zusätzlich alle Talkshowplätze von Politiker:innen über
            die Zeit betrachten. Die obrige Darstellung zeigt wie häufig eine
            Partei in einem Monat in den fünf Talkshows aufgetreten ist.
            Spannend ist hier der Bereich kurz vor Koalitionsbruch am
            6.November. Im Oktober 2024 tut sich in der Verteilung der
            Parteibücher ein Loch auf. Zu dieser Zeit werden fast ausschließlich
            CDU, SPD, Grüne und FPD eingeladen. Das Phänomen setzt sich im
            November 2024 fort, nachdem der damalige Bundeskanzler Olaf Scholz
            seinen Finanzminister aus dem Amt entlässt. Der Trend löst sich erst
            im Dezember 2024 auf. Vermutlich weil der <i>Ampelbruch</i> medial
            größtenteils verarbeitet war. <br />
            Aus der Grafik kann auch auffallen, das die AfD seit März, nicht mehr
            eingeladen wurde. Die Einstufung als gesichert rechtsextremistisch erfolgte
            am
            <a
                href="https://www.tagesschau.de/inland/innenpolitik/verfassungsschutz-afd-102.html"
                target="_blank"
                class="underline"
            >
                2.5.2025
            </a>. Seit der Bundestagswahl wird die AfD nicht mehr in Talkshows
            eingeladen. Das die Afd seit der Bundestagswahl nicht mehr in Talkshows 
            eingeladen wird, hat sicher auch mit vergangenen Auftritten zutun.
            Es konnte der Eindruck entstehen, das die Talkshows als Bühne für 
            Verschwörungstheorien und Desinformation genutzt wurden. <br />
            Die Auftrittsfrequenz der Linken steigt hingegen im Trend eher an. Mit
            dem Erfolg der Partei scheint eine gewisse Auseinandersetzung mit der
            Partei stattzufinden.
        </p>
    </div>
</div>

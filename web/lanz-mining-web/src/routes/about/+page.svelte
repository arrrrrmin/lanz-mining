<script>
    import HeaderNav from "../../components/HeaderNav.svelte";
    import Quote from "../../components/Quote.svelte";
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
        title: "Lanz Mining, Über",
        description:
            "Daten der ÖR-Talkshows, Markus Lanz, Maischberger, Maybrit Illner, Caren Miosga und Hart aber fair. Die Datenauskünfte zeigen dir welche Daten vorhanden und wo die so her kommen.",
        url: "https://arrrrrmin.github.io/lanz-mining/about",
    };
</script>


<Meta
    title="Lanz Mining, Über"
    description="Daten der ÖR-Talkshows, Markus Lanz, Maischberger, Maybrit Illner, Caren Miosga und Hart aber fair. Über das Projekt."
    image={meta.image}
    url="https://arrrrrmin.github.io/lanz-mining/about"
    siteUrl="https://arrrrrmin.github.io/lanz-mining/"
    {openGraph}
    twitter="true"
/>
<HeaderNav />
<main>
    <h2 class="max-w-2xl mx-auto py-4 text-l font-bold">Über Lanz Mining</h2>
    <p>
        Mein Name ist <code>arrrrrmin</code> und ich bin
        <a href="https://www.ccc.de" target="_blank">CCC</a>-affiner Data
        Scientist aus Tübingen. Ich arbeite jede Tag mit verschiedenen Daten und
        will einen Beitrag gegen den Rechtsruck leisten. Seit den Enthüllungen
        von Correctiv, müssen wir alle versuchen einen Beitrag im Rahmen unserer
        Möglichkeiten zu leisten. Dieses Projekt ist in meiner Freizeit
        entstanden. Ein Freund fragte:
        <Quote>
            Dieser Robin Alexander ist aber ständig bei Lanz?! Ist das so? Gibt
            es da eigentlich keine Auskunft?
        </Quote>
        Also hab ich für meinen Kumpel diese Informationen maschinell erfragt und
        diese Projekt gebaut. Während dem Projekt fand sich schnell eine Forderung:
        <strong> Öffentliches Geld, öffentliche Daten</strong>.
    </p>
    <p>
        Wenn ihr die Daten selbst gut brauchen könnt, meld dich gerne bei mir
        auf
        <a href="https://chaos.social/@arrrrrmin"><span>Mastodon</span></a>,
        <a href="https://bsky.app/profile/arrrrrmin.bsky.social"
            ><span>Bluesky</span></a
        >
        oder per Mail: <span>hello [AT] arrrrrmin [DOT] dev</span>
    </p>
</main>

<style lang="postcss">
    @reference "tailwindcss/theme";
</style>

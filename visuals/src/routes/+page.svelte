<script>
    import V0_Overview from "$lib/visualisations/V0_Overview.svelte";
    import V1_EpisodesTotal from "$lib/visualisations/V1_EpisodesTotal.svelte";
    import V2_ContentPerMonth from "$lib/visualisations/V2_ContentPerMonth.svelte";
    import V3_TalkshowsVsSquidGame from "$lib/visualisations/V3_TalkshowsVsSquidGame.svelte";
    import V4_TopTalkers from "$lib/visualisations/V4_TopTalkers.svelte";
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

    let { data } = $props();
    let formatOrder = $state({});
    let groupOrder = $state({});
</script>

<div>
    <div class="max-w-2xl m-auto py-8">
        <h1 class="font-black text-5xl">GPN23 - LanzMining</h1>
        <h2 class="font-semibold text-3xl">Wer spricht denn da?</h2>
        <dl class="pt-10 text-lg">
            <div class="flex gap-2">
                <dt>at:</dt>
                <dd>
                    <a
                        class="underline hover:text-stone-400"
                        target="_blank"
                        href="https://entropia.de/GPN23">GPN23 in Karlsruhe</a
                    >
                </dd>
            </div>
            <div class="flex gap-2">
                <dt>by:</dt>
                <dd>
                    <a
                        class="underline hover:text-stone-400"
                        target="_blank"
                        href="https://chaos.social/@arrrrrmin">arrrrrmin</a
                    >
                </dd>
            </div>
            <div class="flex gap-2">
                <dt>Source:</dt>
                <dd>
                    <a
                        class="underline hover:text-stone-400"
                        target="_blank"
                        href="https://codeberg.org/arrrrrmin/GPN23-SprechschauMining"
                        >codeberg/arrrrrmin/GPN23-SprechschauMining</a
                    >
                </dd>
            </div>
        </dl>
        <div class="pt-10 pb-12">
            <p class="py-2">
                This page provides visualisations build for this keynote in the
                web, so interactions are still useable and people can explore
                the data a little more.
            </p>
            <p>
                Plots are provided in raw for without additional context. For
                more information see the talk slides or the recording on <a
                    href="https://media.ccc.de">media.ccc.de</a
                >.
            </p>
            <p><b>Hope you enjoy the keynote</b></p>
        </div>
    </div>

    <h3 id="v0-overview" class="pt-8 pb-4 text-2xl font-bold">
        View over 1+ year
    </h3>
    <V0_Overview {data} id={"v0-overview"} />
    <div class="py-8"></div>

    <h3 id="episodes-total" class="pt-8 pb-4 text-2xl font-bold">
        Episodes per format
    </h3>
    <V1_EpisodesTotal {data} id={"episodes-total"} bind:formatOrder />
    <div class="py-8"></div>

    <h3 id="content-per-month" class="pt-8 pb-4 text-2xl font-bold">
        Produced talk content (in minutes) per month
    </h3>
    <V2_ContentPerMonth {data} id={"content-per-month"} {formatOrder} />
    <div class="py-8"></div>

    <h3 id="talkshows-vs-squidgame" class="pt-8 pb-4 text-2xl font-bold">
        Average month compared to SquidGame
    </h3>
    <V3_TalkshowsVsSquidGame
        {data}
        id={"talkshows-vs-squidgame"}
        {formatOrder}
    />
    <div class="py-8"></div>

    <h3 id="top-talkers" class="pt-8 pb-4 text-2xl font-bold">
        Top 15 most invited talkers
    </h3>
    <V4_TopTalkers {data} id={"top-talkers"} n={15} {formatOrder} />
    <div class="py-8"></div>

    <h3 id="invite-ratio" class="pt-8 pb-4 text-2xl font-bold">Invite ratio</h3>
    <V5_InviteRatio {data} id={"invite-ratio"} />
    <div class="py-8"></div>

    <h3 id="lots-of-roles" class="pt-8 pb-4 text-2xl font-bold">
        Lots of roles
    </h3>
    <V6_LotsOfRoles {data} id={"lots-of-roles"} />
    <div class="py-8"></div>

    <h3 id="main-experts" class="pt-8 pb-4 text-2xl font-bold">Main experts</h3>
    <V7_Experts {data} id={"main-experts"} />
    <div class="py-8"></div>

    <h3 id="guest-divergence" class="pt-8 pb-4 text-2xl font-bold">
        Guest divergence (in proportion to broadcast station (all on ARD side
        adds up to 100%))
    </h3>
    <V8_GuestDivergence {data} id={"guest-divergence"} />
    <div class="py-8"></div>

    <h3 id="group-representatives" class="pt-8 pb-4 text-2xl font-bold">
        Group representatives
    </h3>
    <V9_TopPerGroup {data} id={"group-representatives"} bind:groupOrder />
    <div class="py-8"></div>

    <h3 id="media-cycle" class="pt-8 pb-4 text-2xl font-bold">
        Media representation in talkshow formats
    </h3>
    <V10_MediaCycle {data} id={"media-cycle"} {formatOrder} />
    <div class="py-8"></div>

    <h3 id="media-cycle-2" class="pt-8 pb-4 text-2xl font-bold">
        Media representatives in talkshow formats (2)
    </h3>
    <V11_MediaRepresentatives {data} id={"media-cycle-2"} {formatOrder} />
    <div class="py-8"></div>

    <h3 id="match-making-pol" class="pt-8 pb-4 text-2xl font-bold">
        Political match making
    </h3>
    <V12_MatchMaking {data} id={"match-making-pol"} />
    <div class="py-8"></div>

    <h3 id="match-making-groups" class="pt-8 pb-4 text-2xl font-bold">
        Which groups are meet by politicians?
    </h3>
    <V13_MatchMakingGroups {data} id={"match-making-groups"} {groupOrder} />
    <div class="py-8"></div>

    <h3 id="match-making-media" class="pt-8 pb-4 text-2xl font-bold">
        Which party meets which media institutions?
    </h3>
    <V14_MatchMakingMedia {data} id={"match-making-media"} />
    <div class="py-8"></div>

    <h3 id="party-invite-dist-overview" class="pt-8 pb-4 text-2xl font-bold">
        Party invitation overview
    </h3>
    <V15_PartyDistOverview {data} id={"party-invite-dist-overview"} />
    <div class="py-8"></div>

    <h3 id="party-invite-dist-format" class="pt-8 pb-4 text-2xl font-bold">
        Party invitation overview
    </h3>
    <V16_PartyDistFormat {data} id={"party-invite-dist-format"} />

    <div class="max-w-2xl m-auto py-16">
        <div>
            <p class="py-2">
                For more details regarding the last example on factchecking vs
                attention, see
                <a
                    href="https://data-dialogue.arrrrrmin.dev/facts-and-attention"
                    target="_blank"
                    class="underline hover:text-stone-400"
                    >data-dialogue.arrrrrmin.dev</a
                >. It's an interactive version of this plot.
            </p>
            <p>
                So nice that you'r interested enough to get here. If you have
                ideas or comments, please reach out to me on
                <a
                    href="https://chaos.social/@arrrrrmin"
                    target="_blank"
                    class="underline hover:text-stone-400">Mastodon</a
                >. Thanks 🙏
            </p>
        </div>
    </div>
</div>

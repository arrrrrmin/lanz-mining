import { error } from '@sveltejs/kit';
import * as d3 from "d3";

export const prerender = true;

/** @type {import('./$types').PageServerLoad} */
export async function load({ params }) {
    const dateParser = d3.timeParse("%Y-%m-%d")
    const posts = await d3.json(
        "https://codeberg.org/arrrrrmin/factchecking-vs-attention/raw/branch/main/export-2025-03-05.13:43.json"
    ).then((d) => (
        {
            bluesky_posts: d["bluesky-posts"].map(D => ({ ...D, created_at: d3.isoParse(D.created_at) })),
            mastodon_posts: d["mastodon-posts"].map(D => ({ ...D, created_at: d3.isoParse(D.created_at) })),
        }
    ));

    if (posts) {
        return { data: posts };
    }

    error(404, 'Not found');
}
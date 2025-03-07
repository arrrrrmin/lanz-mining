import { error } from '@sveltejs/kit';
import * as d3 from "d3";

export const prerender = true;

/** @type {import('./$types').PageServerLoad} */
export async function load({ params }) {
	const dateParser = d3.timeParse("%Y-%m-%d")
	const data = await d3.csv(
		"https://raw.githubusercontent.com/arrrrrmin/lanz-mining/refs/heads/svelte-web/web/lanz-mining-web/static/data-processed-update.csv"
	).then((d) => d.map((D) => {
		return {
			index: parseInt(D.index),
			episode_name: D.episode_name,
			date: dateParser(D.date),
			// description: D.description,
			factcheck: D.factcheck,
			len: parseInt(D["length"]),
			name: D.name,
			role: D.role,
			// message: D.message,
			talkshow: D.talkshow,
			party: D.party,
			group: D.group,
			media: D.media,
		}
	}));

	if (data) {
		return { data: data };
	}

	error(404, 'Not found');
}
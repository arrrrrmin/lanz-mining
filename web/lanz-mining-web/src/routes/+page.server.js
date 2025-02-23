import { error } from '@sveltejs/kit';
import * as d3 from "d3";


/** @type {import('./$types').PageServerLoad} */
export async function load({ params }) {
	const dateParser = d3.timeParse("%Y-%m-%d")
	const data = await d3.csv("http://localhost:5173/data-processed-update.csv").then((d) => d.map((D) => {
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
			// register_index: D.register_index,
			// Rechtliches: parseInt(D.Rechtliches),
			// Innenpolitik: parseInt(D.Innenpolitik),
			// Soziales: parseInt(D.Soziales),
			// Außenpolitik: parseInt(D.Außenpolitik),
			// Migration: parseInt(D.Migration),
			// Energie: parseInt(D.Energie),
			// Klima: parseInt(D.Klima),
			// Sicherheit: parseInt(D.Sicherheit),
			// Digitales: parseInt(D.Digitales),
			// Bildung: parseInt(D.Bildung),
			// Wirtschaft: parseInt(D.Wirtschaft),
			// Russland: parseInt(D.Russland),
			// Nahost: parseInt(D.Nahost),
			// Ukraine: parseInt(D.Ukraine),
			// Gesundheit: parseInt(D.Gesundheit),
		}
	}));

	if (data) {
		return { data: data };
	}

	error(404, 'Not found');
}
import { error } from '@sveltejs/kit';
import * as d3 from "d3";
import * as utils from "$lib/visualisations/utils";


export async function fetchLanzMining() {
    const dateParser = d3.timeParse("%Y-%m-%d");

    const data = await d3.csv("http://localhost:5173/data/lanz-mining-2025-5-16.csv").then((d) => d.map((D) => {
        // Exclude some fields we currently don't use!
        return {
            // description: D.description,
            // message: D.message,
            index: parseInt(D.index),
            episode_name: D.episode_name,
            date: dateParser(D.date),
            factcheck: D.factcheck,
            len: parseInt(D["length"]),
            name: D.name,
            role: D.role,
            talkshow: D.talkshow,
            party: D.party,
            group: D.group,
            media: D.media,
        }
    }));

    if (data) {
        // Filter data to the first of Feb., so all shows have a fair start 
        return { data: utils.uniformStart(data) };
    }

    error(404, 'Not found');
}
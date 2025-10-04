import * as d3 from "npm:d3";
import * as utils from "../components/utils.js";


export async function fetchLanzMining(host, file) {
    const dateParser = d3.timeParse("%Y-%m-%d");

    const data = await d3.csv(`${host}/${file}`).then((d) => d.map((D) => {
        return {
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
            /** Currently not used:
            * description: D.description,
            * message: D.message,
            */
        }
    }));

    if (data) {
        // Filter data to the first of Feb., so all shows have a fair start 
        let _data = data.filter(d => d.group);
        return utils.uniformStart(_data);
    }
}
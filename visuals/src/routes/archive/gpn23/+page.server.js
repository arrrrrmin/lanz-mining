import { fetchLanzMining } from '$lib/fetch';
import { error } from '@sveltejs/kit';
import config from '$lib/config.js';

export const prerender = true;

export async function load({ params }) {
    const { data } = await fetchLanzMining(config.dataHost, "data/lanz-mining-2025-5-30.csv");

    if (data) {
        return { data: data };
    }

    error(404, 'Not found');
}
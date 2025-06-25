import { fetchLanzMining } from '$lib/fetch';
import { error } from '@sveltejs/kit';

export const prerender = true;

export async function load({ params }) {
    const { data } = await fetchLanzMining();

    if (data) {
        return { data: data };
    }

    error(404, 'Not found');
}
import { fetchLanzMining } from '$lib/fetch';
import { error } from '@sveltejs/kit';
import config from '$lib/config.js';

export const prerender = true;

export async function load({ params }) {
    return { data: undefined };
}
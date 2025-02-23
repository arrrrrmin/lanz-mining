<header>
    <nav
        class="mx-auto grid xs:grid-cols-1 sm:flex justify-between items-baseline max-w-7xl py-4"
        aria-label="Global"
    >
        <div class="py-2">
            <h1><a href="/">Open Sprechschau</a></h1>
        </div>
        <div class="flex gap-x-4">
            <a aria-current="false" href="/datenauskunfte/">Datenauskünfte</a>
            <a aria-current="false" href="/about/">Über</a>
            <div class="flex gap-x-2 items-center">
                <a
                    href="https://github.com/arrrrrmin/lanz-mining"
                    class="text-stone-500 hover:text-stone-800"
                    target="_blank"
                    rel="noopener noreferrer me"
                    aria-label="button"
                    title="View Source on Github"
                    ><svg
                        class="size-4"
                        fill="currentcolor"
                        viewBox="0 0 24 24"
                        stroke="currentcolor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        ><path
                            d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37.0 00-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44.0 0020 4.77 5.07 5.07.0 0019.91 1S18.73.65 16 2.48a13.38 13.38.0 00-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07.0 005 4.77 5.44 5.44.0 003.5 8.55c0 5.42 3.3 6.61 6.44 7A3.37 3.37.0 009 18.13V22"
                        ></path></svg
                    >
                </a><a
                    href="https://chaos.social/@arrrrrmin"
                    class="text-stone-500 hover:text-stone-800"
                    target="_blank"
                    rel="noopener noreferrer me"
                    aria-label="button"
                    title="See You on Mastodon"
                    ><svg
                        class="size-4"
                        fill="currentcolor"
                        viewBox="0 0 24 24"
                        stroke="currentcolor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        ><path
                            d="M21.58 13.913c-.29 1.469-2.592 3.121-5.238 3.396-1.379.184-2.737.368-4.185.276-2.368-.092-4.237-.551-4.237-.551.0.184.014.459.043.643.308 2.294 2.317 2.478 4.22 2.57 1.922.0 3.633-.46 3.633-.46l.079 1.653s-1.344.734-3.738.918c-1.32.091-2.96-.092-4.869-.551-4.14-1.102-4.853-5.507-4.961-10.005-.034-1.285-.013-2.57-.013-3.58.0-4.589 3-5.966 3-5.966 1.513-.734 4.11-1.01 6.808-1.01h.067c2.699.0 5.296.276 6.81 1.01.0.0 3 1.377 3 5.967.0.0.037 3.304-.419 5.69"
                            stroke="currentcolor"
                        ></path><path
                            d="M17.832 8.633v5h-1.978V8.78c0-1.023-.43-1.542-1.29-1.542-.95.0-1.427.616-1.427 1.834v2.655H11.17V9.072c0-1.218-.476-1.834-1.427-1.834-.86.0-1.29.52-1.29 1.542v4.852H6.475V8.633c0-1.022.26-1.834.782-2.434.538-.6 1.243-.909 2.118-.909 1.012.0 1.779.39 2.286 1.169l.492.827.493-.827c.507-.78 1.274-1.169 2.286-1.169.875.0 1.58.308 2.118.909.522.6.782 1.412.782 2.434"
                            fill="currentcolor"
                            stroke="none"
                        ></path></svg
                    >
                </a><a
                    href="https://bsky.app/profile/arrrrrmin.bsky.social"
                    class="text-stone-500 hover:text-stone-800"
                    target="_blank"
                    rel="noopener noreferrer me"
                    aria-label="button"
                    title="See You on Bluesky"
                    ><svg
                        class="size-4"
                        fill="currentcolor"
                        viewBox="0 0 360 320"
                        ><path
                            d="M180 141.964c-16.301-31.702-60.692-90.7823-101.9653-119.92C38.4971-5.86834 23.414-1.03207 13.526 3.43594 2.08093 8.60755.0 26.1785.0 36.5164.0 46.8542 5.66748 121.272 9.36416 133.694 21.5786 174.738 65.0603 188.607 105.104 184.156 107.151 183.852 109.227 183.572 111.329 183.312 109.267 183.642 107.19 183.924 105.104 184.156 46.4204 192.847-5.69621 214.233 62.6582 290.33 137.848 368.18 165.705 273.637 180 225.702c14.295 47.935 30.76 139.069 115.995 64.628C360 225.702 313.58 192.85 254.896 184.158 252.81 183.926 250.733 183.645 248.671 183.315 250.773 183.574 252.849 183.855 254.896 184.158 294.94 188.61 338.421 174.74 350.636 133.697 354.333 121.275 360 46.8568 360 36.519 360 26.1811 357.919 8.61012 346.474 3.43851 336.586-1.02949 321.503-5.86576 281.965 22.0466 240.692 51.1843 196.301 110.262 180 141.964z"
                        ></path></svg
                    ></a
                >
            </div>
        </div>
    </nav>
</header>

<style lang="postcss">
    @reference "tailwindcss/theme";
    h1 a {
        @apply text-xl font-bold;
    }
    a {
        @apply text-sm/6 font-semibold text-gray-500 hover:text-gray-800 no-underline;
        /**px-2.5 border-gray-800 border-1 */
    }
</style>

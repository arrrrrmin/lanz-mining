<script>
    import { MetaTags, JsonLd } from "svelte-meta-tags";
    import config from "$lib/config";

    /** Open Graph information */
    const openGraph = {
        type: "article",
        url: config.siteUrl,
        title: config.title,
        description: config.description,
        article: {
            publishedTime: config.published.toISOString(),
            modifiedTime: config.updated.toISOString(),
            section: "Data Visualizations",
            authors: [config.author],
            tags: config.tags,
        },
        images: [`${config.siteUrl}/${config.image}`],
    };

    /** Twitter information */
    const twitter = {
        cardType: "summary_large_image",
        title: config.title,
        description: config.description,
        image: `${config.siteUrl}/${config.image}`,
        imageAlt: config.imageAlt,
    };

    /** Collection of all tags */
    const main = {
        title: config.title,
        robots: "index,follow", // default
        // additionalRobotsProps: "",
        description: config.description,
        // This is not the same as tags (topics) for blog related things
        canonical: config.siteUrl,
        // additionalMetaTags: "",
        // additionalLinkTags: "",
        twitter: twitter,
        openGraph: openGraph,
        keywords: config.tags,
    };

    /** Json-Ld properties */
    const schema = {
        "@type": "Article",
        mainEntityOfPage: { "@type": "WebPage", "@id": config.siteUrl },
        headline: config.title,
        image: `${config.siteUrl}/${config.image}`,
        datePublished: config.published.toISOString(),
        dateModified: config.updated.toISOString(),
        author: {
            "@type": "Person",
            name: config.author,
            sameAs: [
                "https://arrrrrmin.dev",
                "https://data-dialogue.arrrrrmin.dev",
            ],
            url: "https://arrrrrmin.dev",
        },
        publisher: {
            "@type": "Organization",
            name: "LanzMining",
            logo: {
                "@type": "ImageObject",
                url: `${config.siteUrl}/${config.image}`,
            },
        },
    };
</script>

<MetaTags {...main} />
<JsonLd {schema} />

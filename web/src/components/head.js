import { configuration } from "../assets/config.js";


export function renderMeta({ title, path, data }) {
    console.log(title, path, data);
    const { metaTitle, tags, jsonLd } = generateMetadata({ title, path, data });

    const metaTags = tags
        .map(tag => {
            if (tag.name) return `<meta name="${tag.name}" content="${tag.content}">`;
            if (tag.property) return `<meta property="${tag.property}" content="${tag.content}">`;
            if (tag.rel) return `<link rel="${tag.rel}" href="${tag.href}">`;
            return "";
        })
        .join("\n  ");

    const jsonLdTag = `<script type="application/ld+json">${JSON.stringify(jsonLd, null, 2)}</script>`;

    return `
    <title>${metaTitle}</title>
    <link rel="icon" href=${configuration.favicon} type="image/png" sizes="96x96">
    <link rel="me" href="https://chaos.social/@arrrrrmin">
    <meta name="fediverse:creator" content="@arrrrrmin@chaos.social">
    ${metaTags}
    ${jsonLdTag}
  `;
}

export function generateMetadata({ title, path, data = {} }) {
    const site = {
        name: undefined,
        url: configuration.url,
        description: configuration.description,
        author: configuration.author,
        language: configuration.language,
        image: `${configuration.url}/_file/${configuration.image}`,
    };

    const metaTitle = `${title} | ${configuration.subtitle}`;
    const metaDescription = site.description;
    const canonicalUrl = site.url;
    const image = site.image;
    const published = data.date || new Date().toISOString();

    return {
        metaTitle: title,
        tags: [
            // Basic
            { name: "description", content: metaDescription },
            { name: "author", content: site.author },
            { name: "language", content: site.language },
            { name: "robots", content: "index, follow" },
            { rel: "canonical", href: canonicalUrl },

            // OpenGraph
            { property: "og:type", content: data.type || "website" },
            { property: "og:title", content: metaTitle },
            { property: "og:description", content: metaDescription },
            { property: "og:url", content: canonicalUrl },
            { property: "og:image", content: image },

            // Twitter Card
            { name: "twitter:card", content: "summary_large_image" },
            { name: "twitter:title", content: metaTitle },
            { name: "twitter:description", content: metaDescription },
            { name: "twitter:image", content: image },

            // Extras
            { name: "date", content: published },
            { name: "theme-color", content: "#FBBF24" },
        ],
        jsonLd: {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "WebSite",
                    "@id": "https://lanz-mining.arrrrrmin.dev/#website",
                    "url": "https://lanz-mining.arrrrrmin.dev",
                    "name": "Lanz Mining",
                    "alternateName": metaTitle,
                    "description": metaDescription,
                    "inLanguage": "de",
                    "publisher": {
                        "@id": "https://lanz-mining.arrrrrmin.dev/#organization"
                    }
                },
                {
                    "@type": "Organization",
                    "@id": "https://lanz-mining.arrrrrmin.dev/#organization",
                    "name": "Lanz Mining Project",
                    "url": "https://lanz-mining.arrrrrmin.dev",
                    "logo": {
                        "@type": "ImageObject",
                        "url": image
                    },
                    "sameAs": [
                        "https://github.com/arrrrrmin/lanz-mining"
                    ]
                },
                // TODO this would be nice to support
                // {
                //     "@type": "Dataset",
                //     "@id": "https://lanz-mining.arrrrrmin.dev/#dataset",
                //     "name": "Lanz Mining Talkshow Dataset",
                //     "description": "Structured data about guests and episodes of German public talk shows, collected for analysis of media participation and diversity representation.",
                //     "url": "https://lanz-mining.arrrrrmin.dev/data",
                //     "license": "https://creativecommons.org/licenses/by/4.0/",
                //     "creator": {
                //         "@id": "https://lanz-mining.arrrrrmin.dev/#organization"
                //     },
                //     "distribution": {
                //         "@type": "DataDownload",
                //         "encodingFormat": "application/json",
                //         "contentUrl": "https://lanz-mining.arrrrrmin.dev/api/data"
                //     },
                //     "keywords": [
                //         "media analysis",
                //         "talk shows",
                //         "public broadcasting",
                //         "ARD",
                //         "ZDF",
                //         "ZDF Markus Lanz",
                //         "ZDF Maybrit Illner",
                //         "ARD Sandra Maischberger",
                //         "ARD Hart aber fair",
                //         "ARD Caren Miosga",
                //         "participation",
                //         "representation",
                //         "Germany"
                //     ],
                //     "temporalCoverage": `${configuration.temporalCoverage.start}/${configuration.temporalCoverage.end}`,
                //     "spatialCoverage": {
                //         "@type": "Country",
                //         "name": "Germany"
                //     }
                // }
            ]
        }

    };
}

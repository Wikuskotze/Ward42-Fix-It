const CACHE_NAME = "ward42-fixit-v2";

const FILES_TO_CACHE = [
    "/",
    "/offline",
    "/report",
    "/status",
    "/login",
    "/static/css/styles.css",
    "/static/manifest.json"
];

self.addEventListener(
    "install",
    (event) => {

        self.skipWaiting();

        event.waitUntil(

            caches.open(CACHE_NAME)
                .then((cache) => {

                    return cache.addAll(
                        FILES_TO_CACHE
                    );

                })

        );

    }
);

self.addEventListener(
    "activate",
    (event) => {

        event.waitUntil(
            clients.claim()
        );

    }
);

self.addEventListener(
    "fetch",
    (event) => {

        event.respondWith(

            fetch(event.request)

            .catch(async () => {

                if (
                    event.request.mode ===
                    "navigate"
                ) {

                    return await caches.match(
                        "/offline"
                    );
                }

                const cachedResponse =
                    await caches.match(
                        event.request
                    );

                return (
                    cachedResponse
                    ||
                    Response.error()
                );

            })

        );

    }
);

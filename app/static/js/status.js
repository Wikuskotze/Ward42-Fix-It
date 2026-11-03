document.addEventListener("DOMContentLoaded", () => {

    const reference =
        document.getElementById("reference");

    if (!reference) return;

    reference.addEventListener("input", () => {

        reference.value =
            reference.value
                .trim()
                .toUpperCase()
                .replace(/\s/g, "");

    });

});

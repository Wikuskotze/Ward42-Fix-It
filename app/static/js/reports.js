document.addEventListener("DOMContentLoaded", () => {

    const categoryFilter =
        document.getElementById("category");

    const statusFilter =
        document.getElementById("status");

    const searchField =
        document.getElementById("search");

    const reportRows =
        document.querySelectorAll(
            "tbody tr[data-category]"
        );

    function filterReports() {

        const selectedCategory =
            categoryFilter
                ? categoryFilter.value.toLowerCase()
                : "";

        const selectedStatus =
            statusFilter
                ? statusFilter.value.toLowerCase()
                : "";

        const searchText =
            searchField
                ? searchField.value
                    .trim()
                    .toLowerCase()
                : "";

        reportRows.forEach(row => {

            const category =
                row.dataset.category
                    ?.toLowerCase() || "";

            const status =
                row.dataset.status
                    ?.toLowerCase() || "";

            const rowText =
                row.textContent
                    .toLowerCase();

            const categoryMatch =
                !selectedCategory ||
                category === selectedCategory;

            const statusMatch =
                !selectedStatus ||
                status === selectedStatus;

            const searchMatch =
                !searchText ||
                rowText.includes(searchText);

            row.style.display =
                categoryMatch &&
                statusMatch &&
                searchMatch
                    ? ""
                    : "none";

        });

    }

    if (categoryFilter) {

        categoryFilter.addEventListener(
            "change",
            filterReports
        );

    }

    if (statusFilter) {

        statusFilter.addEventListener(
            "change",
            filterReports
        );

    }

    if (searchField) {

        searchField.addEventListener(
            "input",
            filterReports
        );

    }

    filterReports();

});

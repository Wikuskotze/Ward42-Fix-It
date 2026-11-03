const chartCanvas =
    document.getElementById("reportChart");

if (chartCanvas) {

    new Chart(chartCanvas, {

        type: "bar",

        data: {

            labels: [
                "Potholes",
                "Water Leaks",
                "Streetlights",
                "Illegal Dumping",
                "Other"
            ],

            datasets: [{

                label: "Reports",

                data: [
                    potholeCount,
                    waterLeakCount,
                    streetlightCount,
                    dumpingCount,
                    otherCount
                ],

                backgroundColor: [
                    "#198754",
                    "#0dcaf0",
                    "#ffc107",
                    "#dc3545",
                    "#6c757d"
                ],

                borderWidth: 1

            }]
        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    display: true
                },

                title: {

                    display: true,

                    text: "Reports by Category"
                }
            },

            scales: {

                y: {

                    beginAtZero: true,

                    ticks: {

                        precision: 0
                    }
                }
            }
        }

    });

}

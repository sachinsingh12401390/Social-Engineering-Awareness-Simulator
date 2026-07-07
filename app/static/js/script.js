document.addEventListener("DOMContentLoaded", function () {

    const canvas = document.getElementById("scoreChart");

    if (!canvas) {
        return;
    }

    if (!window.chartData) {
        console.error("Chart data not found.");
        return;
    }

    const ctx = canvas.getContext("2d");

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: window.chartData.labels,
            datasets: [{
                label: "Score (%)",
                data: window.chartData.scores,
                backgroundColor: [
                    "#0d6efd",
                    "#198754",
                    "#ffc107",
                    "#dc3545",
                    "#6f42c1",
                    "#20c997",
                    "#fd7e14",
                    "#0dcaf0"
                ],
                borderColor: "#212529",
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });

});
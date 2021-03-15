const setup = () => {
    const getTheme = () => {
        if (window.localStorage.getItem("dark")) {
            return JSON.parse(window.localStorage.getItem("dark"));
        }
        return (
            !!window.matchMedia &&
            window.matchMedia("(prefers-color-scheme: dark)").matches
        );
    };

    const setTheme = (value) => {
        window.localStorage.setItem("dark", value);
    };

    return {
        loading: true,
        isDark: getTheme(),
        toggleTheme() {
            this.isDark = !this.isDark;
            setTheme(this.isDark);
        },
        setLightTheme() {
            this.isDark = false;
            setTheme(this.isDark);
        },
        setDarkTheme() {
            this.isDark = true;
            setTheme(this.isDark);
        },
        isSettingsPanelOpen: false,
        openSettingsPanel() {
            this.isSettingsPanelOpen = true;
            this.$nextTick(() => {
                this.$refs.settingsPanel.focus();
            });
        },
        isNotificationsPanelOpen: false,
        openNotificationsPanel() {
            this.isNotificationsPanelOpen = true;
            this.$nextTick(() => {
                this.$refs.notificationsPanel.focus();
            });
        },
        isSearchPanelOpen: false,
        openSearchPanel() {
            this.isSearchPanelOpen = true;
            this.$nextTick(() => {
                this.$refs.searchInput.focus();
            });
        },
        isMobileSubMenuOpen: false,
        openMobileSubMenu() {
            this.isMobileSubMenuOpen = true;
            this.$nextTick(() => {
                this.$refs.mobileSubMenu.focus();
            });
        },
        isMobileMainMenuOpen: false,
        openMobileMainMenu() {
            this.isMobileMainMenuOpen = true;
            this.$nextTick(() => {
                this.$refs.mobileMainMenu.focus();
            });
        },
    };
};
document.addEventListener("DOMContentLoaded", function () {
    window.onload = () => {
        // Chart
        let ctx = document.getElementById("myChart");
        let myChart = new Chart(ctx, {
            type: "bar",
            data: {
                labels: ["Positif", "Netral", "Negatif"],
                datasets: [
                    {
                        label: "Sentiment",
                        data: JSON.parse(ctx.dataset.barchart),
                        backgroundColor: [
                            "rgba(54, 162, 235, 0.2)",
                            "rgba(255, 206, 86, 0.2)",
                            "rgba(255, 99, 132, 0.2)",
                        ],
                        borderColor: [
                            "rgba(54, 162, 235, 1)",
                            "rgba(255, 206, 86, 1)",
                            "rgba(255, 99, 132, 1)",
                        ],
                        borderWidth: 1,
                    },
                ],
            },
            options: {
                title: {
                    display: true,
                    text: "Chart.js Bar Chart",
                },
                legend: {
                    display: false,
                },
                scales: {
                    yAxes: [
                        {
                            ticks: {
                                beginAtZero: true,
                            },
                        },
                    ],
                },
                tooltips: {
                    position: "average",
                    mode: "index",
                    intersect: false,
                },
            },
        });

        let ctx2 = document.getElementById("myDoughnutChart");
        let myDoughnutChart = new Chart(ctx2, {
            type: "doughnut",
            data: {
                datasets: [
                    {
                        data: JSON.parse(ctx2.dataset.doughnutchart),
                        backgroundColor: [
                            "rgba(113, 94, 255, 1)",
                            "rgba(250, 255, 117, 1)",
                            "rgba(255, 82, 59, 1)",
                        ],
                        label: "Dataset 1",
                    },
                ],
                labels: ["Positif", "Netral", "Negatif"],
            },
            options: {
                responsive: true,
                legend: {
                    position: "top",
                },
                title: {
                    display: true,
                    text: "Chart.js Doughnut Chart",
                },
                animation: {
                    animateScale: true,
                    animateRotate: true,
                },
                tooltips: {
                    callbacks: {
                        label: function (tooltipItem, data) {
                            let dataset =
                                data.datasets[tooltipItem.datasetIndex];
                            let total = dataset.data.reduce(function (
                                previousValue,
                                currentValue,
                                currentIndex,
                                array
                            ) {
                                return previousValue + currentValue;
                            });
                            let currentValue = dataset.data[tooltipItem.index];
                            let percentage = Math.floor(
                                (currentValue / total) * 100 + 0.5
                            );
                            return ` ${percentage}%`;
                        },
                        title: function (tooltipItem, data) {
                            return data.labels[tooltipItem[0].index];
                        },
                    },
                },
            },
        });

        let ctx3 = document.getElementById("myLineChart");
        const { tanggal, positif, netral, negatif } = JSON.parse(
            ctx3.dataset.linechart
        );
        let myLineChart = new Chart(ctx3, {
            type: "line",
            data: {
                labels: tanggal,
                datasets: [
                    {
                        label: "Positif",
                        borderColor: "rgba(54, 162, 235, 1)",
                        backgroundColor: "rgba(54, 162, 235, 0.2)",
                        data: positif,
                        fill: false,
                    },
                    {
                        label: "Netral",
                        borderColor: "rgba(255, 205, 86, 1)",
                        backgroundColor: "rgba(255, 205, 86, 0.2)",
                        data: netral,
                        fill: false,
                    },
                    {
                        label: "Negatif",
                        borderColor: "rgba(255, 99, 132, 1)",
                        backgroundColor: "rgba(255, 99, 132, 0.2)",
                        data: negatif,
                        fill: false,
                    },
                ],
            },
            options: {
                responsive: true,
                title: {
                    display: true,
                    text: "Tooltip Position: average",
                },
                tooltips: {
                    position: "average",
                    mode: "index",
                    intersect: false,
                },
            },
        });

        // Sweet Alert
        const msg = document.getElementById("message");
        const alert = (response, message, type) => {
            Swal.fire({
                title: `${response}!`,
                html: message,
                icon: type,
                confirmButtonText: "Next",
            });
        };
        if (msg) {
            if (msg.dataset.success)
                alert("Success", msg.dataset.success, msg.dataset.type);
            else if (msg.dataset.error)
                alert("Error", msg.dataset.error, msg.dataset.type);
        }
    };
});

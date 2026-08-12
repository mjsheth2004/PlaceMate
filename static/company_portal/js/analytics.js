/**
 * Company Portal Recruiter Analytics JavaScript
 * Renders interactive Chart.js visualizations with dynamic light/dark mode theme support.
 */

document.addEventListener('DOMContentLoaded', () => {
    // Helper to safely parse embedded JSON
    function getJsonData(id) {
        const elem = document.getElementById(id);
        if (!elem) return { labels: [], data: [] };
        try {
            const parsed = JSON.parse(elem.textContent || '{}');
            return {
                labels: parsed.labels || [],
                data: parsed.data || parsed.values || [],
                applicants: parsed.applicants || [],
                hires: parsed.hires || parsed.selections || []
            };
        } catch (e) {
            console.error(`Failed to parse JSON for ${id}:`, e);
            return { labels: [], data: [] };
        }
    }

    const funnelData = getJsonData('funnel-data');
    const driveCompData = getJsonData('drive-comp-data');
    const deptData = getJsonData('dept-data');
    const cgpaData = getJsonData('cgpa-data');


    // Dynamic Theme Helper
    function getThemeColors() {
        const isDark = document.body.getAttribute('data-theme') === 'dark';
        return {
            textColor: isDark ? '#F4E9CD' : '#264653',
            secondaryTextColor: isDark ? '#E9C46A' : '#8A6D3B',
            gridColor: isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.06)',
            tooltipBg: isDark ? '#264653' : '#FDFBF7',
            tooltipText: isDark ? '#F4E9CD' : '#264653',
        };
    }

    let colors = getThemeColors();

    // Chart References
    let funnelChart, driveCompChart, deptChart, cgpaChart;

    // Set Default Chart Font
    Chart.defaults.font.family = "'Inter', sans-serif";

    // 1. Recruitment Pipeline Funnel Chart (Doughnut)
    const funnelCtx = document.getElementById('funnelChart');
    if (funnelCtx) {
        funnelChart = new Chart(funnelCtx, {
            type: 'doughnut',
            data: {
                labels: funnelData.labels,
                datasets: [{
                    data: funnelData.data,
                    backgroundColor: [
                        '#2A9D8F', // Applied
                        '#E9C46A', // Shortlisted
                        '#E76F51', // Interview
                        '#21867A', // Selected
                        '#D62828'  // Rejected
                    ],
                    borderWidth: 2,
                    borderColor: colors.tooltipBg,
                    hoverOffset: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: colors.textColor,
                            boxWidth: 12,
                            padding: 15,
                            font: { size: 11, weight: '500' }
                        }
                    },
                    tooltip: { cornerRadius: 6 }
                },
                cutout: '65%'
            }
        });
    }

    // 2. Drive Comparison Grouped Bar Chart
    const driveCompCtx = document.getElementById('driveCompChart');
    if (driveCompCtx) {
        driveCompChart = new Chart(driveCompCtx, {
            type: 'bar',
            data: {
                labels: driveCompData.labels,
                datasets: [
                    {
                        label: 'Applicants',
                        data: driveCompData.applicants,
                        backgroundColor: 'rgba(42, 157, 143, 0.8)',
                        borderRadius: 4
                    },
                    {
                        label: 'Hires',
                        data: driveCompData.hires,
                        backgroundColor: 'rgba(33, 134, 122, 0.9)',
                        borderRadius: 4
                    }

                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { color: colors.textColor, font: { size: 11, weight: '500' } }
                    },
                    y: {
                        beginAtZero: true,
                        grid: { color: colors.gridColor },
                        ticks: { color: colors.secondaryTextColor, stepSize: 1, font: { size: 11 } }
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                        labels: { color: colors.textColor, boxWidth: 12, font: { size: 11 } }
                    },
                    tooltip: { cornerRadius: 6 }
                }
            }
        });
    }

    // 3. Department Distribution Pie Chart
    const deptCtx = document.getElementById('deptChart');
    if (deptCtx) {
        deptChart = new Chart(deptCtx, {
            type: 'pie',
            data: {
                labels: deptData.labels,
                datasets: [{
                    data: deptData.data,
                    backgroundColor: [
                        '#2A9D8F',
                        '#E9C46A',
                        '#E76F51',
                        '#21867A',
                        '#F4A261',
                        '#264653'
                    ],
                    borderWidth: 2,
                    borderColor: colors.tooltipBg
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: colors.textColor,
                            boxWidth: 12,
                            padding: 12,
                            font: { size: 11 }
                        }
                    },
                    tooltip: { cornerRadius: 6 }
                }
            }
        });
    }

    // 4. Candidate CGPA Distribution Bar Chart
    const cgpaCtx = document.getElementById('cgpaChart');
    if (cgpaCtx) {
        cgpaChart = new Chart(cgpaCtx, {
            type: 'bar',
            data: {
                labels: cgpaData.labels,
                datasets: [{
                    label: 'Candidates',
                    data: cgpaData.data,
                    backgroundColor: 'rgba(233, 196, 106, 0.85)',
                    borderColor: '#E9C46A',
                    borderWidth: 1,
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { color: colors.textColor, font: { size: 11, weight: '500' } }
                    },
                    y: {
                        beginAtZero: true,
                        grid: { color: colors.gridColor },
                        ticks: { color: colors.secondaryTextColor, stepSize: 1, font: { size: 11 } }
                    }
                },
                plugins: {
                    legend: { display: false },
                    tooltip: { cornerRadius: 6 }
                }
            }
        });
    }

    // Function to update all charts on theme toggle
    function updateChartsTheme() {
        const updatedColors = getThemeColors();
        
        [funnelChart, driveCompChart, deptChart, cgpaChart].forEach(chart => {
            if (!chart) return;
            
            if (chart.options.plugins?.legend?.labels) {
                chart.options.plugins.legend.labels.color = updatedColors.textColor;
            }
            if (chart.options.scales?.x?.ticks) {
                chart.options.scales.x.ticks.color = updatedColors.secondaryTextColor;
            }
            if (chart.options.scales?.x?.grid) {
                chart.options.scales.x.grid.color = updatedColors.gridColor;
            }
            if (chart.options.scales?.y?.ticks) {
                chart.options.scales.y.ticks.color = updatedColors.secondaryTextColor;
            }
            if (chart.options.scales?.y?.grid) {
                chart.options.scales.y.grid.color = updatedColors.gridColor;
            }
            chart.update();
        });
    }

    // Observer for Theme Changes (Light / Dark Mode Sync)
    const observer = new MutationObserver(updateChartsTheme);
    observer.observe(document.body, { attributes: true, attributeFilter: ['data-theme'] });
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

    window.addEventListener('themeChanged', updateChartsTheme);
});


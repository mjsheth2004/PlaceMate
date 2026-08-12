/**
 * Student Analytics Chart.js Integration Script
 * Manages responsive rendering and dynamic theme transitions for analytics charts.
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
                data: parsed.data || parsed.values || []
            };
        } catch (e) {
            console.error(`Failed to parse JSON for ${id}:`, e);
            return { labels: [], data: [] };
        }
    }

    const statusData = getJsonData('status-data');
    const salaryData = getJsonData('salary-data');
    const timelineData = getJsonData('timeline-data');
    const skillData = getJsonData('skill-data');


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
    let statusChart, timelineChart, salaryChart, skillChart;

    // Chart Default Fonts
    Chart.defaults.font.family = "'Inter', sans-serif";

    // 1. Status Doughnut Chart
    const statusCtx = document.getElementById('statusChart');
    if (statusCtx) {
        statusChart = new Chart(statusCtx, {
            type: 'doughnut',
            data: {
                labels: statusData.labels,
                datasets: [{
                    data: statusData.data,
                    backgroundColor: [
                        '#2A9D8F', // Applied
                        '#E9C46A', // Shortlisted
                        '#E76F51', // Interview Scheduled
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
                            font: { size: 12, weight: '500' }
                        }
                    },
                    tooltip: {
                        padding: 10,
                        cornerRadius: 6
                    }
                },
                cutout: '68%'
            }
        });
    }

    // 2. Timeline Line Chart
    const timelineCtx = document.getElementById('timelineChart');
    if (timelineCtx) {
        timelineChart = new Chart(timelineCtx, {
            type: 'line',
            data: {
                labels: timelineData.labels,
                datasets: [{
                    label: 'Applications',
                    data: timelineData.data,
                    borderColor: '#2A9D8F',
                    backgroundColor: 'rgba(42, 157, 143, 0.12)',
                    fill: true,
                    tension: 0.35,
                    borderWidth: 3,
                    pointBackgroundColor: '#2A9D8F',
                    pointRadius: 4,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        grid: { color: colors.gridColor },
                        ticks: { color: colors.secondaryTextColor, font: { size: 11 } }
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

    // 3. Salary Tier Bar Chart
    const salaryCtx = document.getElementById('salaryChart');
    if (salaryCtx) {
        salaryChart = new Chart(salaryCtx, {
            type: 'bar',
            data: {
                labels: salaryData.labels,
                datasets: [{
                    label: 'Drives',
                    data: salaryData.data,
                    backgroundColor: [
                        'rgba(42, 157, 143, 0.75)',
                        'rgba(233, 196, 106, 0.85)',
                        'rgba(231, 111, 81, 0.75)',
                        'rgba(33, 134, 122, 0.9)'
                    ],
                    borderRadius: 6,
                    borderSkipped: false
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

    // 4. Skill Alignment Horizontal Bar Chart
    const skillCtx = document.getElementById('skillChart');
    if (skillCtx) {
        skillChart = new Chart(skillCtx, {
            type: 'bar',
            data: {
                labels: skillData.labels,
                datasets: [{
                    label: 'Active Drives Requiring Skill',
                    data: skillData.data,
                    backgroundColor: '#2A9D8F',
                    borderRadius: 4
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        beginAtZero: true,
                        grid: { color: colors.gridColor },
                        ticks: { color: colors.secondaryTextColor, stepSize: 1, font: { size: 11 } }
                    },
                    y: {
                        grid: { display: false },
                        ticks: { color: colors.textColor, font: { size: 11, weight: '500' } }
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
        
        [statusChart, timelineChart, salaryChart, skillChart].forEach(chart => {
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


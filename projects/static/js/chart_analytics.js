// Initialize data structure for sales analytics
let salesData = {
    years: [],
    months: [],
    projects: []
};

let currentYear = '2024';
let selectedProject = 'all';
let showingAllData = false;
let filterValue = '';

// Ma'lumotlarni olish
async function fetchData() {
    try {
        const response = await fetch('/project-analysis/');
        
        if (!response.ok) {
            throw new Error('Ma\'lumotlarni olishda xatolik yuz berdi');
        }
        
        const data = await response.json();
        
        salesData = {
            years: data.years || [],
            months: data.months || [],
            projects: data.projects || []
        };

        // Initialize year selector options after data load
        yearSelector.innerHTML = '';
        salesData.years.forEach(year => {
            const option = document.createElement('option');
            option.value = year;
            option.text = year;
            option.selected = year === currentYear;
            yearSelector.appendChild(option);
        });

        // Initialize project buttons after data load
        projectSelector.innerHTML = '';
        projectSelector.appendChild(allProjectsBtn);
        salesData.projects.forEach(project => {
            const btn = document.createElement('button');
            btn.className = 'w-full px-3 py-2 text-sm font-medium text-gray-700 transition-all bg-gray-200 sm:w-auto sm:px-4 rounded-xl dark:bg-gray-700 dark:text-gray-300 hover:bg-purple-100 dark:hover:bg-purple-900 sm:text-base';
            btn.textContent = project.name;
            btn.onclick = () => {
                selectedProject = project.name;
                updateChart();
                updateTable();
                updateButtonStates();
            };
            projectSelector.appendChild(btn);
        });

        // Set current year to latest year
        currentYear = salesData.years[salesData.years.length - 1];
        
        // Update visualizations
        updateChart();
        updateTable();
        updateButtonStates();

        return salesData;
    } catch (error) {
        console.error('Xatolik:', error);
        const chartElement = document.querySelector('#salesChart');
        chartElement.innerHTML = `
            <div class="text-center p-4">
                <p class="text-red-500">Ma'lumotlarni yuklashda xatolik yuz berdi. Iltimos qaytadan urinib ko'ring.</p>
            </div>
        `;
    }
}

// Create filter and controls section first
const filterControls = document.createElement('div');
filterControls.className = 'flex flex-col flex-wrap items-center gap-4 p-4 mb-4 bg-white border border-gray-100 shadow-lg sm:flex-row sm:p-6 dark:bg-gray-800 rounded-xl dark:border-gray-700 sm:mb-6';

// Year selector
const yearSelector = document.createElement('select');
yearSelector.className = 'w-full sm:w-auto px-3 sm:px-4 py-2 sm:py-2.5 bg-gray-50 dark:bg-gray-700 border-2 border-purple-200 dark:border-purple-800 rounded-xl text-gray-700 dark:text-gray-300 focus:ring-4 focus:ring-purple-500/30 focus:border-purple-500 transition-all text-sm sm:text-base';

// Filter input
const filterInput = document.createElement('div');
filterInput.className = 'relative w-full sm:flex-1';
filterInput.innerHTML = `
    <input type="text" placeholder="Filter projects..." 
    class="w-full px-3 sm:px-4 py-2 sm:py-2.5 pl-10 sm:pl-12 bg-gray-50 dark:bg-gray-700 border-2 border-purple-200 dark:border-purple-800 rounded-xl text-gray-700 dark:text-gray-300 focus:ring-4 focus:ring-purple-500/30 focus:border-purple-500 transition-all text-sm sm:text-base">
    <i class="fas fa-search absolute left-3 sm:left-4 top-1/2 transform -translate-y-1/2 text-purple-500"></i>
`;

// Show all toggle
const toggleButton = document.createElement('button');
toggleButton.className = 'w-full sm:w-auto px-4 sm:px-6 py-2 sm:py-2.5 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white rounded-xl shadow-lg transition-all flex items-center justify-center sm:justify-start gap-2 text-sm sm:text-base';
toggleButton.innerHTML = '<i class="fas fa-eye"></i><span>Show All</span>';

filterControls.appendChild(yearSelector);
filterControls.appendChild(filterInput);
filterControls.appendChild(toggleButton);

// Project selector section
const projectSelector = document.createElement('div');
projectSelector.className = 'flex flex-wrap gap-2 p-4 mb-4 bg-white border border-gray-100 shadow-lg sm:gap-4 sm:p-6 dark:bg-gray-800 rounded-xl dark:border-gray-700 sm:mb-6';

const allProjectsBtn = document.createElement('button');
allProjectsBtn.className = 'w-full px-3 py-2 text-sm font-medium text-white transition-all bg-purple-600 sm:w-auto sm:px-4 rounded-xl hover:bg-purple-700 sm:text-base';
allProjectsBtn.textContent = 'All Projects';
allProjectsBtn.onclick = () => {
    selectedProject = 'all';
    updateChart();
    updateTable();
    updateButtonStates();
};

// Insert controls in correct order
const chartElement = document.querySelector('#salesChart');
chartElement.before(projectSelector);
chartElement.before(filterControls);

function updateButtonStates() {
    projectSelector.querySelectorAll('button').forEach(btn => {
        if ((btn.textContent === 'All Projects' && selectedProject === 'all') ||
            btn.textContent === selectedProject) {
            btn.className = 'w-full px-3 py-2 text-sm font-medium text-white transition-all bg-purple-600 sm:w-auto sm:px-4 rounded-xl hover:bg-purple-700 sm:text-base';
        } else {
            btn.className = 'w-full px-3 py-2 text-sm font-medium text-gray-700 transition-all bg-gray-200 sm:w-auto sm:px-4 rounded-xl dark:bg-gray-700 dark:text-gray-300 hover:bg-purple-100 dark:hover:bg-purple-900 sm:text-base';
        }
    });
}

function calculateTotalSales(year, projectName = 'all') {
    if (!salesData.projects.length) return 0;
    
    if (projectName === 'all') {
        return salesData.projects.reduce((total, project) => {
            return total + (project.sales[year] ? project.sales[year].reduce((sum, sale) => sum + sale, 0) : 0);
        }, 0);
    } else {
        const project = salesData.projects.find(p => p.name === projectName);
        return project && project.sales[year] ? 
            project.sales[year].reduce((sum, sale) => sum + sale, 0) : 0;
    }
}

const chartOptions = {
    series: [],
    chart: {
        height: 400,
        type: 'line',
        fontFamily: 'Montserrat, sans-serif',
        toolbar: {
            show: false
        },
        zoom: {
            enabled: false
        },
        background: 'transparent',
        foreColor: '#9CA3AF'
    },
    stroke: {
        curve: 'smooth',
        width: 3
    },
    colors: ['#8B5CF6', '#3B82F6', '#10B981'],
    grid: {
        borderColor: '#374151',
        strokeDashArray: 5,
        xaxis: {
            lines: {
                show: true
            }
        },
        yaxis: {
            lines: {
                show: true
            }
        }
    },
    xaxis: {
        categories: [],
        labels: {
            style: {
                colors: '#9CA3AF',
                fontSize: '12px',
                fontWeight: 500
            },
            rotate: -45,
            rotateAlways: false,
            hideOverlappingLabels: true
        },
        axisBorder: {
            color: '#374151'
        },
        axisTicks: {
            color: '#374151'
        }
    },
    yaxis: {
        labels: {
            formatter: value => `$${value.toLocaleString()}`,
            style: {
                colors: '#9CA3AF',
                fontSize: '12px',
                fontWeight: 500
            }
        }
    },
    legend: {
        show: true,
        position: 'top',
        horizontalAlign: 'right',
        labels: {
            colors: '#9CA3AF'
        },
        fontSize: '12px',
        markers: {
            width: 12,
            height: 12,
            radius: 12
        }
    },
    tooltip: {
        theme: 'dark',
        y: {
            formatter: value => `$${value.toLocaleString()}`
        },
        style: {
            fontSize: '12px',
            fontFamily: 'Montserrat, sans-serif'
        }
    },
    responsive: [{
        breakpoint: 480,
        options: {
            legend: {
                position: 'bottom',
                horizontalAlign: 'center'
            }
        }
    }]
};

const chart = new ApexCharts(document.querySelector("#salesChart"), chartOptions);
chart.render();

function updateChart() {
    if (!salesData.projects.length) return;

    let series = [];
    if (selectedProject === 'all') {
        series = salesData.projects.map(project => ({
            name: project.name,
            data: project.sales[currentYear] || []
        }));
    } else {
        const project = salesData.projects.find(p => p.name === selectedProject);
        if (project) {
            series = [{
                name: project.name,
                data: project.sales[currentYear] || []
            }];
        }
    }

    const totalSales = calculateTotalSales(currentYear, selectedProject);
    
    chart.updateOptions({
        series: series,
        xaxis: {
            categories: salesData.months
        },
        title: {
            text: `Total Sales: $${totalSales.toLocaleString()}`,
            align: 'center',
            style: {
                fontSize: '16px',
                fontWeight: 600,
                color: '#9CA3AF'
            },
            margin: 10
        }
    });
}

function createTableRow(project, monthIndex, year) {
    if (!project || !project.sales || !project.sales[year]) return null;
    
    const row = document.createElement('tr');
    row.className = 'transition-all duration-300 transform translate-y-4 opacity-0 hover:bg-gray-50 dark:hover:bg-gray-700';
    row.innerHTML = `
        <td class="px-3 sm:px-6 py-3 sm:py-4 whitespace-nowrap">
            <div class="flex items-center">
                <div class="text-xs sm:text-sm font-medium text-gray-900 dark:text-gray-100">${project.name}</div>
            </div>
        </td>
        <td class="px-3 sm:px-6 py-3 sm:py-4 whitespace-nowrap">
            <div class="text-xs sm:text-sm text-gray-500 dark:text-gray-400">${salesData.months[monthIndex]}</div>
        </td>
        <td class="px-3 sm:px-6 py-3 sm:py-4 whitespace-nowrap">
            <div class="text-xs sm:text-sm font-semibold text-emerald-600 dark:text-emerald-400">$${(project.sales[year][monthIndex] || 0).toLocaleString()}</div>
        </td>
    `;
    return row;
}

function updateTable() {
    const tableBody = document.getElementById('salesTable');
    if (!tableBody) return;
    
    tableBody.innerHTML = '';
    
    if (!salesData.projects.length) return;

    const monthsToShow = currentYear === '2024' ? 11 : 12;
    let projectsToShow = selectedProject === 'all' ? 
        salesData.projects : 
        [salesData.projects.find(p => p.name === selectedProject)].filter(Boolean);

    projectsToShow = projectsToShow.filter(project => 
        project.name.toLowerCase().includes(filterValue.toLowerCase())
    );

    const rows = [];
    if (showingAllData) {
        projectsToShow.forEach(project => {
            for(let i = 0; i < monthsToShow; i++) {
                const row = createTableRow(project, i, currentYear);
                if (row) rows.push(row);
            }
        });
    } else {
        projectsToShow.forEach(project => {
            const row = createTableRow(project, 0, currentYear);
            if (row) rows.push(row);
        });
    }

    rows.forEach((row, index) => {
        tableBody.appendChild(row);
        gsap.to(row, {
            opacity: 1,
            y: 0,
            duration: 0.3,
            delay: index * 0.05
        });
    });
}

// Event listeners
yearSelector.addEventListener('change', (e) => {
    currentYear = e.target.value;
    updateChart();
    updateTable();
});

filterInput.querySelector('input').addEventListener('input', (e) => {
    filterValue = e.target.value;
    updateTable();
});

toggleButton.addEventListener('click', () => {
    showingAllData = !showingAllData;
    toggleButton.innerHTML = showingAllData ? 
        '<i class="fas fa-eye-slash"></i><span>Show Less</span>' : 
        '<i class="fas fa-eye"></i><span>Show All</span>';
    updateTable();
});

// Initialize
fetchData();

// Dark mode handling
const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        if (mutation.attributeName === 'class') {
            const isDark = document.documentElement.classList.contains('dark');
            chart.updateOptions({
                theme: {
                    mode: isDark ? 'dark' : 'light'
                },
                grid: {
                    borderColor: isDark ? '#374151' : '#E5E7EB'
                }
            });
        }
    });
});

observer.observe(document.documentElement, {
    attributes: true
});
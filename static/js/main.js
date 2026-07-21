const themeToggle = document.getElementById('toggleTheme');
if (themeToggle) {
  themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('alt-theme');
    const newTheme = document.body.classList.contains('alt-theme') ? 'dark' : 'light';
    localStorage.setItem('pharmacyTheme', newTheme);
  });
}
const savedTheme = localStorage.getItem('pharmacyTheme');
if (savedTheme === 'dark') {
  document.body.classList.add('alt-theme');
}

const chartColors = {
  primary: '#6c8cff',
  secondary: '#22d3ee',
  success: '#4ade80',
  danger: '#ff5c7a',
  warning: '#fbbf24',
  palette: ['#6c8cff', '#22d3ee', '#4ade80', '#f97316', '#ec4899', '#34d399', '#60a5fa', '#a78bfa']
};

function createDoughnutChart(canvasId, labels, values, title) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;
  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: values,
        backgroundColor: chartColors.palette,
        borderColor: '#0f172d',
        borderWidth: 3,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {color: '#e8f0ff', font: {size: 12, weight: 500}, padding: 15}
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          titleColor: '#22d3ee',
          bodyColor: '#e8f0ff',
          borderColor: '#6c8cff',
          borderWidth: 1,
          padding: 12,
          titleFont: {size: 14, weight: 'bold'},
          callbacks: {
            label: function(context) {
              return context.label + ': ' + context.parsed + ' units';
            }
          }
        }
      },
      animation: {duration: 1500, easing: 'easeInOutQuart'}
    },
  });
}

function createBarChart(canvasId, labels, values, title) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: title,
        data: values,
        backgroundColor: chartColors.palette,
        borderColor: '#6c8cff',
        borderWidth: 2,
        borderRadius: 8,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      indexAxis: 'y',
      plugins: {
        legend: {
          display: true,
          labels: {color: '#e8f0ff', font: {size: 12}, padding: 15}
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          titleColor: '#22d3ee',
          bodyColor: '#e8f0ff',
          borderColor: '#6c8cff',
          borderWidth: 1,
          padding: 12,
        }
      },
      scales: {
        y: {ticks: {color: '#9bb3d0'}, grid: {color: 'rgba(255, 255, 255, 0.05)'}},
        x: {ticks: {color: '#9bb3d0'}, grid: {color: 'rgba(255, 255, 255, 0.05)'}}
      },
      animation: {duration: 1500, easing: 'easeInOutQuart'}
    },
  });
}

function createLineChart(canvasId, labels, values, title) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5'],
      datasets: [{
        label: 'Sales Trend',
        data: values && values.length ? values : [10, 20, 25, 30, 35],
        borderColor: '#22d3ee',
        backgroundColor: 'rgba(34, 211, 238, 0.1)',
        borderWidth: 3,
        fill: true,
        tension: 0.4,
        pointBackgroundColor: '#6c8cff',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 6,
        pointHoverRadius: 8,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          display: true,
          labels: {color: '#e8f0ff', font: {size: 12}, padding: 15}
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          titleColor: '#22d3ee',
          bodyColor: '#e8f0ff',
          borderColor: '#6c8cff',
          borderWidth: 1,
          padding: 12,
        }
      },
      scales: {
        y: {ticks: {color: '#9bb3d0'}, grid: {color: 'rgba(255, 255, 255, 0.05)'}},
        x: {ticks: {color: '#9bb3d0'}, grid: {color: 'rgba(255, 255, 255, 0.05)'}}
      },
      animation: {duration: 1500, easing: 'easeInOutQuart'}
    },
  });
}

document.addEventListener('DOMContentLoaded', () => {
  if (typeof categoryLabels !== 'undefined' && typeof categorySales !== 'undefined') {
    createDoughnutChart('categorySalesChart', categoryLabels, categorySales, 'Category Sales');
  }
  if (typeof stockLabels !== 'undefined' && typeof stockValues !== 'undefined') {
    createBarChart('stockChart', stockLabels, stockValues, 'Stock by Category');
  }
  const salesTrendCtx = document.getElementById('salesTrendChart');
  if (salesTrendCtx) {
    createLineChart('salesTrendChart', ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5'], [12, 28, 35, 42, 50], 'Sales Trend');
  }
  const healthCtx = document.getElementById('healthChart');
  if (healthCtx) {
    createBarChart('healthChart', ['In Stock', 'Low Stock', 'Critical'], [65, 25, 10], 'Inventory Health');
  }
});

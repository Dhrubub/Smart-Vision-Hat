// Mode Usage Stats
const modeUsageCtx = document.getElementById('modeUsageChart').getContext('2d');
const modeUsageData = {
  labels: ['Insight Snap Mode', 'Eyes-On Mode', 'Vision Assist Mode'],
  datasets: [{
    data: [120, 80, 45],
    backgroundColor: ['red', 'green', 'blue']
  }]
};
const modeUsageChart = new Chart(modeUsageCtx, {
  type: 'pie',
  data: modeUsageData
});

// Usage Time Stats
const usageTimeCtx = document.getElementById('usageTimeChart').getContext('2d');
const usageTimeData = {
  labels: ['2023-10-01', '2023-09-30', '2023-09-25'],
  datasets: [{
    data: [5, 3, 4],
    backgroundColor: 'blue'
  }]
};
const usageTimeChart = new Chart(usageTimeCtx, {
  type: 'bar',
  data: usageTimeData
});

// Top 10 Objects Detected
const topObjectsCtx = document.getElementById('topObjectsChart').getContext('2d');
const topObjectsData = {
  labels: ['Car', 'Dog', 'Tree', 'Person', 'Bicycle'],
  datasets: [{
    data: [35, 25, 20, 18, 15],
    backgroundColor: ['red', 'green', 'blue', 'yellow', 'purple']
  }]
};
const topObjectsChart = new Chart(topObjectsCtx, {
  type: 'doughnut',
  data: topObjectsData
});

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

const labels = ["Test1", "Test2"];
const scores = [10, 20];
const correct = 10;
const wrong = 5;

const barCtx = document.getElementById('barChart');

new Chart(barCtx, {
  type: 'bar',
  data: {
    labels: ['Quiz 1', 'Quiz 2', 'Quiz 3', 'Quiz 4'],
    datasets: [{
      label: 'Scores',
      data: [60, 75, 80, 90],
      backgroundColor: '#4f46e5'
    }]
  }
});



const pieCtx = document.getElementById('pieChart');

new Chart(pieCtx, {
  type: 'pie',
  data: {
    labels: ['Correct', 'Wrong', 'Skipped'],
    datasets: [{
      data: [70, 20, 10],
      backgroundColor: ['#4f46e5', '#ef4444', '#f59e0b']
    }]
  }
});
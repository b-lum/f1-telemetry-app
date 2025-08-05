import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
} from 'chart.js';

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement);

export default function TelemetryChart({ label, datasets }) {
  const chartData = {
    labels: Array(datasets[0].data.length).fill(''),
    datasets: datasets.map(ds => ({
      label: ds.label,
      data: ds.data,
      borderColor: ds.color,
      tension: 0.3,
    }))
  };

  const options = {
    animation: false,
    scales: {
      y: {
        min: 0,
        max: label === 'Speed' ? 400 : 1
      }
    }
  };

  return <Line data={chartData} options={options} />;
}

import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
} from 'chart.js';

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement);

export default function TelemetryChart({ label, data, color }) {
   const chartData = {
      labels: Array(data.length).fill(''),
      datasets: [{
         label,
         data,
         borderColor: color,
         tension: 0.3,
      }]
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

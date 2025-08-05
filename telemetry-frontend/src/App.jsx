import { useEffect, useState, useRef } from 'react';  // <-- add useRef here
import axios from 'axios';
import TelemetryChart from './components/TelemetryChart';

function App() {
  const [speedData, setSpeedData] = useState(Array(50).fill(0));
  const [throttleData, setThrottleData] = useState(Array(50).fill(0));
  const [brakeData, setBrakeData] = useState(Array(50).fill(0));

  const [isPolling, setIsPolling] = useState(false);
  const intervalRef = useRef(null);  // <-- interval ID stored here

  // Start polling function
  const startPolling = () => {
    if (!intervalRef.current) {
      console.log("Starting polling");

      intervalRef.current = setInterval(async () => {
        console.log("Polling...");

        try {
          const res = await axios.get("http://localhost:8000/telemetry");
          const { speed, throttle, brake } = res.data;

          setSpeedData(prev => [...prev.slice(1), speed]);
          setThrottleData(prev => [...prev.slice(1), throttle]);
          setBrakeData(prev => [...prev.slice(1), brake]);
        } catch (err) {
          console.error("Backend not responding:", err.message);
        }
      }, 100);
      setIsPolling(true);
    }
  };

  // Stop polling function
  const stopPolling = () => {
    if (intervalRef.current) {
      console.log("Stopping polling", intervalRef.current);
      clearInterval(intervalRef.current);
      intervalRef.current = null;
      setIsPolling(false);
    }
  };

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>F1 2020 Live Telemetry</h1>
      
      <button onClick={() => (isPolling ? stopPolling() : startPolling())}>
        {isPolling ? 'Stop' : 'Start'}
      </button>

      <TelemetryChart label="Speed" data={speedData} color="green" />
      <TelemetryChart label="Throttle" data={throttleData} color="blue" />
      <TelemetryChart label="Brake" data={brakeData} color="red" />
    </div>
  );
}

export default App;

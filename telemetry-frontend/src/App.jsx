import { useEffect, useState, useRef, memo } from 'react';
import TelemetryChart from './components/TelemetryChart';

// Memoized chart components
const SpeedChart = memo(({ data }) => (
  <TelemetryChart
    label="Speed"
    datasets={[{ label: "Speed", data, color: "green" }]}
  />
));

const ThrottleBrakeChart = memo(({ throttleData, brakeData }) => (
  <TelemetryChart
    label="Throttle & Brake"
    datasets={[
      { label: "Throttle", data: throttleData, color: "blue" },
      { label: "Brake", data: brakeData, color: "red" },
    ]}
  />
));

const WheelSlipChart = memo(({ wheelSlip }) => (
  <TelemetryChart
    label="Wheel Slip"
    datasets={[
      { label: "Rear Left", data: wheelSlip.map(ws => ws[0]), color: "cyan" },
      { label: "Rear Right", data: wheelSlip.map(ws => ws[1]), color: "pink" },
      { label: "Front Left", data: wheelSlip.map(ws => ws[2]), color: "orange" },
      { label: "Front Right", data: wheelSlip.map(ws => ws[3]), color: "purple" },
    ]}
  />
));

function App() {
  // React state (for rendering)
  const [speedData, setSpeedData] = useState(Array(50).fill(0));
  const [throttleData, setThrottleData] = useState(Array(50).fill(0));
  const [brakeData, setBrakeData] = useState(Array(50).fill(0));
  const [wheelSlip, setWheelSlip] = useState(Array.from({ length: 50 }, () => [0, 0, 0, 0]));
  const [time, setTime] = useState(0);
  const [lapData, setLapData] = useState(null);
  const [sessionData, setSessionData] = useState(null);

  // Refs for “live” data
  const speedRef = useRef([...speedData]);
  const throttleRef = useRef([...throttleData]);
  const brakeRef = useRef([...brakeData]);
  const wheelSlipRef = useRef([...wheelSlip]);
  const timeRef = useRef(time);

  const ws = useRef(null);
  const packetQueue = useRef([]);
  const renderIntervalRef = useRef(null);
  const [isRunning, setIsRunning] = useState(false);

  const startWS = () => {
    if (ws.current) return;

    ws.current = new WebSocket('ws://localhost:8000/ws/telemetry');

    ws.current.onopen = () => {
      console.log("WebSocket opened");
      setIsRunning(true);
    };

    ws.current.onmessage = (event) => {
      const packet = JSON.parse(event.data);
      packetQueue.current.push(packet);
    };

    ws.current.onerror = (err) => console.error("WebSocket error:", err);

    ws.current.onclose = () => {
      console.log("WebSocket closed");
      setIsRunning(false);
      if (renderIntervalRef.current) clearInterval(renderIntervalRef.current);
      renderIntervalRef.current = null;
    };

    // Batch update interval
    if (!renderIntervalRef.current) {
      renderIntervalRef.current = setInterval(() => {
        while (packetQueue.current.length > 0) {
          const packet = packetQueue.current.shift();

          switch (packet.packetType) {
            case "carTelemetry":
              speedRef.current.push(packet.speed);
              speedRef.current.shift();

              throttleRef.current.push(packet.throttle);
              throttleRef.current.shift();

              brakeRef.current.push(packet.brake);
              brakeRef.current.shift();

              timeRef.current = packet.time;
              break;

            case "motion":
              wheelSlipRef.current.push(packet.wheelSlip);
              wheelSlipRef.current.shift();
              break;

            case "lapData":
              setLapData(packet);
              break;

            case "session":
              setSessionData(packet);
              break;

            default:
              console.warn("Unknown packet type:", packet.packetType);
          }
        }

        // Update React state at fixed interval (20 FPS)
        setSpeedData([...speedRef.current]);
        setThrottleData([...throttleRef.current]);
        setBrakeData([...brakeRef.current]);
        setWheelSlip([...wheelSlipRef.current]);
        setTime(timeRef.current);
      }, 50);
    }
  };

  const stopWS = () => {
    if (ws.current) ws.current.close();
    ws.current = null;
    if (renderIntervalRef.current) clearInterval(renderIntervalRef.current);
    renderIntervalRef.current = null;
    setIsRunning(false);
  };

  useEffect(() => {
    return () => {
      if (ws.current) ws.current.close();
      if (renderIntervalRef.current) clearInterval(renderIntervalRef.current);
    };
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>F1 2020 Live Telemetry (WebSocket)</h1>

      <button onClick={() => (isRunning ? stopWS() : startWS())}>
        {isRunning ? 'Stop' : 'Start'}
      </button>

      <div style={{ marginTop: 10 }}>
        <strong>Current Time:</strong> {time.toFixed(2)}s
      </div>

      <SpeedChart data={speedData} />
      <ThrottleBrakeChart throttleData={throttleData} brakeData={brakeData} />
      <WheelSlipChart wheelSlip={wheelSlip} />

      {lapData && (
        <div>
          <h3>Lap Data</h3>
          <pre>{JSON.stringify(lapData, null, 2)}</pre>
        </div>
      )}

      {sessionData && (
        <div>
          <h3>Session Data</h3>
          <pre>{JSON.stringify(sessionData, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;

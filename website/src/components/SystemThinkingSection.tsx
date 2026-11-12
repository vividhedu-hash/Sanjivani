import React, { useState, useEffect, useRef } from 'react';
import { 
  Activity, 
  Cpu, 
  Sliders, 
  AlertOctagon, 
  Play, 
  Pause, 
  RotateCcw, 
  Zap, 
  Flame, 
  Snowflake,
  ShieldAlert,
  CheckCircle
} from 'lucide-react';
import { sound } from '../utils/soundEffects';

interface SystemThinkingSectionProps {
  isSlideMode?: boolean;
}

export const SystemThinkingSection: React.FC<SystemThinkingSectionProps> = ({ isSlideMode = false }) => {
  const [tUpper, setTUpper] = useState<number>(6.2);
  const [tLower, setTLower] = useState<number>(3.8);
  const [ambientScenario, setAmbientScenario] = useState<'moderate' | 'diurnal' | 'extreme'>('diurnal');
  const [simSpeed, setSimSpeed] = useState<number>(1);
  const [isPaused, setIsPaused] = useState<boolean>(false);
  const [isSensorFault, setIsSensorFault] = useState<boolean>(false);

  const [currentTemp, setCurrentTemp] = useState<number>(4.5);
  const [peltierActive, setPeltierActive] = useState<boolean>(false);
  const [ambientTemp, setAmbientTemp] = useState<number>(35.0);
  const [elapsedHours, setElapsedHours] = useState<number>(64.0);
  const [activeHoursTotal, setActiveHoursTotal] = useState<number>(5.2);
  const [history, setHistory] = useState<{ time: number; temp: number; state: boolean; amb: number }[]>([]);

  const timerRef = useRef<number | null>(null);

  useEffect(() => {
    const initHistory: { time: number; temp: number; state: boolean; amb: number }[] = [];
    for (let t = 50; t < 64; t += 0.5) {
      const amb = 35 + 7 * Math.sin(2 * Math.PI * (t - 8) / 24);
      const isAct = t >= 56 && t <= 58;
      initHistory.push({
        time: Number(t.toFixed(1)),
        temp: isAct ? 4.1 : 5.4,
        state: isAct,
        amb: Number(amb.toFixed(1))
      });
    }
    setHistory(initHistory);
  }, []);

  useEffect(() => {
    if (isPaused) return;

    const intervalMs = 250 / simSpeed;

    timerRef.current = window.setInterval(() => {
      setElapsedHours(prevH => {
        const nextH = prevH + 0.1;

        let nextAmb = 35.0;
        if (ambientScenario === 'moderate') {
          nextAmb = 32.0;
        } else if (ambientScenario === 'diurnal') {
          nextAmb = 35.0 + 7.0 * Math.sin(2 * Math.PI * (nextH - 8.0) / 24.0);
        } else if (ambientScenario === 'extreme') {
          nextAmb = 43.5 + 2.0 * Math.sin(2 * Math.PI * nextH / 24.0);
        }
        setAmbientTemp(Number(nextAmb.toFixed(1)));

        setCurrentTemp(prevT => {
          let nextState = peltierActive;

          if (isSensorFault) {
            nextState = false;
            setPeltierActive(false);
            const deltaT = 0.045 * (nextAmb - prevT) * 0.1;
            return Math.min(18.0, Number((prevT + deltaT).toFixed(2)));
          }

          if (!peltierActive && prevT >= tUpper) {
            nextState = true;
            setPeltierActive(true);
            sound.chime();
          } else if (peltierActive && prevT <= tLower) {
            nextState = false;
            setPeltierActive(false);
          }

          if (nextState) {
            setActiveHoursTotal(a => a + 0.1);
          }

          let dT = 0;
          if (nextState) {
            dT = -0.065;
          } else {
            dT = 0.018 * ((nextAmb - prevT) / 30.0);
          }

          const calculatedT = Math.max(2.2, Math.min(10.5, prevT + dT));
          return Number(calculatedT.toFixed(2));
        });

        setHistory(prevHist => {
          const updated = [...prevHist.slice(-45), {
            time: Number(nextH.toFixed(1)),
            temp: currentTemp,
            state: peltierActive,
            amb: Number(nextAmb.toFixed(1))
          }];
          return updated;
        });

        return Number(nextH.toFixed(1));
      });
    }, intervalMs);

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [isPaused, simSpeed, ambientScenario, tUpper, tLower, isSensorFault, peltierActive, currentTemp]);

  const toggleSensorFault = () => {
    const nextFault = !isSensorFault;
    setIsSensorFault(nextFault);
    if (nextFault) sound.warningBeep();
    else sound.chime();
  };

  const resetSimulation = () => {
    sound.click();
    setCurrentTemp(4.2);
    setPeltierActive(false);
    setElapsedHours(64.0);
    setActiveHoursTotal(5.2);
    setIsSensorFault(false);
  };

  return (
    <div className={`w-full bg-white rounded-2xl border border-slate-200 shadow-xl ${
      isSlideMode ? 'p-5' : 'p-6 md:p-8'
    }`}>
      
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between pb-4 border-b border-slate-200 gap-3">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded text-[11px] font-mono uppercase bg-teal-50 text-[#0F766E] border border-teal-200 font-bold">
              Closed-Loop Control Simulation
            </span>
            <span className="text-xs font-mono text-slate-500">
              Sampling Rate: 10 Hz (DS18B20 1-Wire)
            </span>
          </div>
          <h3 className={`font-serif-display font-bold text-[#0B2545] mt-1 ${
            isSlideMode ? 'text-2xl sm:text-3xl' : 'text-2xl md:text-3xl'
          }`}>
            How The System Thinks: Cooling Only When Necessary
          </h3>
          <p className="text-slate-600 text-xs sm:text-sm mt-0.5 max-w-2xl">
            Instead of continuous active refrigeration, SANJIVANI lets passive bio-PCM absorb baseline thermal ingress and activates solid-state heat pumping solely when chamber temperature hits the trigger threshold.
          </p>
        </div>

        {/* Playback Controls */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => { setIsPaused(!isPaused); sound.click(); }}
            className={`px-3 py-1.5 rounded-lg text-xs font-mono font-bold flex items-center gap-1.5 border transition-all ${
              isPaused 
                ? 'bg-emerald-600 hover:bg-emerald-700 text-white border-emerald-600' 
                : 'bg-slate-100 hover:bg-slate-200 text-slate-700 border-slate-200'
            }`}
          >
            {isPaused ? <Play className="w-3.5 h-3.5" /> : <Pause className="w-3.5 h-3.5" />}
            {isPaused ? 'Resume' : 'Pause'}
          </button>

          <button
            onClick={() => {
              const speeds = [1, 2, 5];
              const nextIdx = (speeds.indexOf(simSpeed) + 1) % speeds.length;
              setSimSpeed(speeds[nextIdx]);
              sound.click();
            }}
            className="px-2.5 py-1.5 rounded-lg bg-slate-100 text-slate-700 hover:bg-slate-200 text-xs font-mono border border-slate-200 font-semibold"
          >
            {simSpeed}× Speed
          </button>

          <button
            onClick={resetSimulation}
            className="p-1.5 rounded-lg bg-slate-100 text-slate-600 hover:text-slate-900 border border-slate-200 transition-colors"
            title="Reset Simulation"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Main Simulation Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 mt-4">
        
        {/* Left 8 Cols: Live SVG Telemetry Chart & Status Indicators */}
        <div className="lg:col-span-8 flex flex-col gap-3.5">
          
          {/* Status Metric Strip */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
            {/* Core Temp */}
            <div className={`p-3 rounded-xl border transition-all ${
              isSensorFault ? 'bg-rose-50 border-rose-300 animate-pulse' :
              currentTemp > 8.0 ? 'bg-rose-50 border-rose-300' :
              peltierActive ? 'bg-cyan-50 border-cyan-300' :
              'bg-slate-50 border-slate-200'
            }`}>
              <div className="flex items-center justify-between text-slate-500 text-[11px] font-mono">
                <span>CHAMBER TEMP</span>
                <Activity className="w-3.5 h-3.5 text-[#0F766E]" />
              </div>
              <div className="flex items-baseline gap-1 mt-0.5">
                <span className={`text-2xl font-mono font-bold ${
                  isSensorFault ? 'text-rose-600' :
                  currentTemp > 8.0 ? 'text-rose-600' :
                  peltierActive ? 'text-cyan-700' : 'text-emerald-700'
                }`}>
                  {isSensorFault ? '--.-' : currentTemp.toFixed(1)}
                </span>
                <span className="text-xs text-slate-500 font-mono">°C</span>
              </div>
              <div className="text-[10px] font-mono text-slate-500 truncate">
                Target: +2°C to +8°C
              </div>
            </div>

            {/* Peltier State */}
            <div className={`p-3 rounded-xl border transition-all ${
              isSensorFault ? 'bg-rose-50 border-rose-300' :
              peltierActive ? 'bg-cyan-50 border-cyan-300 text-cyan-800' :
              'bg-slate-50 border-slate-200 text-slate-700'
            }`}>
              <div className="flex items-center justify-between text-[11px] font-mono text-slate-500">
                <span>PELTIER STATE</span>
                <Cpu className="w-3.5 h-3.5" />
              </div>
              <div className="text-sm font-mono font-bold mt-1 uppercase flex items-center gap-1">
                {isSensorFault ? (
                  <span className="text-rose-600 flex items-center gap-1">
                    <AlertOctagon className="w-3.5 h-3.5" /> FAIL-SAFE CUT
                  </span>
                ) : peltierActive ? (
                  <span className="text-cyan-700 flex items-center gap-1">
                    <Snowflake className="w-3.5 h-3.5 animate-spin" /> ACTIVE (34W)
                  </span>
                ) : (
                  <span className="text-emerald-700 flex items-center gap-1">
                    <CheckCircle className="w-3.5 h-3.5 text-emerald-600" /> PCM STANDBY
                  </span>
                )}
              </div>
              <div className="text-[10px] font-mono text-slate-500">
                {peltierActive ? 'Extracting 18.5W' : 'Idle Drain: 0.15W'}
              </div>
            </div>

            {/* Ambient Condition */}
            <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
              <div className="flex items-center justify-between text-slate-500 text-[11px] font-mono">
                <span>AMBIENT TEMP</span>
                <Flame className="w-3.5 h-3.5 text-amber-500" />
              </div>
              <div className="flex items-baseline gap-1 mt-0.5">
                <span className="text-2xl font-mono font-bold text-amber-700">
                  {ambientTemp.toFixed(1)}
                </span>
                <span className="text-xs text-slate-500 font-mono">°C</span>
              </div>
              <div className="text-[10px] font-mono text-slate-500 uppercase">
                {ambientScenario}
              </div>
            </div>

            {/* Active Runtime */}
            <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
              <div className="flex items-center justify-between text-slate-500 text-[11px] font-mono">
                <span>ACTIVE RUNTIME</span>
                <Zap className="w-3.5 h-3.5 text-indigo-500" />
              </div>
              <div className="flex items-baseline gap-1 mt-0.5">
                <span className="text-2xl font-mono font-bold text-indigo-700">
                  {activeHoursTotal.toFixed(1)}
                </span>
                <span className="text-xs text-slate-500 font-mono">h</span>
              </div>
              <div className="text-[10px] font-mono text-slate-500">
                Duty: {((activeHoursTotal / Math.max(1, elapsedHours)) * 100).toFixed(1)}% (≤8%)
              </div>
            </div>
          </div>

          {/* Dynamic SVG Waveform & Hysteresis Chart */}
          <div className="bg-slate-50 rounded-xl p-3.5 border border-slate-200 relative">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-3">
                <span className="text-xs font-mono font-bold text-[#0B2545] uppercase">
                  Thermal Waveform (T vs Time)
                </span>
                <span className="flex items-center gap-1 text-[11px] font-mono text-[#0F766E] font-semibold">
                  <span className="w-2.5 h-0.5 bg-[#0F766E] inline-block"></span> Chamber T
                </span>
                <span className="flex items-center gap-1 text-[11px] font-mono text-amber-600 font-semibold">
                  <span className="w-2.5 h-0.5 bg-amber-500 inline-block"></span> Ambient T
                </span>
              </div>
              <div className="text-[11px] font-mono text-slate-500">
                Safe Band: +2°C to +8°C
              </div>
            </div>

            {/* Chart SVG */}
            <div className="w-full h-[180px] sm:h-[210px] relative bg-white rounded-lg border border-slate-200">
              <svg className="w-full h-full" viewBox="0 0 600 220" preserveAspectRatio="none">
                {/* Safe Corridor Zone */}
                <rect x="0" y={200 - (8.0 / 45.0) * 190} width="600" height={(6.0 / 45.0) * 190} fill="#10b981" fillOpacity="0.12" />
                
                {/* Upper Limit +8°C Line */}
                <line x1="0" y1={200 - (8.0 / 45.0) * 190} x2="600" y2={200 - (8.0 / 45.0) * 190} stroke="#dc2626" strokeDasharray="4 4" strokeWidth="1.2" />
                <text x="5" y={195 - (8.0 / 45.0) * 190} fill="#dc2626" fontSize="9" fontFamily="monospace" fontWeight="bold">+8.0°C Critical Breach</text>

                {/* Lower Limit +2°C Line */}
                <line x1="0" y1={200 - (2.0 / 45.0) * 190} x2="600" y2={200 - (2.0 / 45.0) * 190} stroke="#0284c7" strokeDasharray="4 4" strokeWidth="1.2" />
                <text x="5" y={212 - (2.0 / 45.0) * 190} fill="#0284c7" fontSize="9" fontFamily="monospace" fontWeight="bold">+2.0°C Freezing Limit</text>

                {/* Upper Hysteresis Trigger Line */}
                <line x1="0" y1={200 - (tUpper / 45.0) * 190} x2="600" y2={200 - (tUpper / 45.0) * 190} stroke="#d97706" strokeDasharray="2 3" strokeWidth="1.2" />
                <text x="490" y={195 - (tUpper / 45.0) * 190} fill="#d97706" fontSize="9" fontFamily="monospace" fontWeight="bold">ON: +{tUpper}°C</text>

                {/* Lower Hysteresis Trigger Line */}
                <line x1="0" y1={200 - (tLower / 45.0) * 190} x2="600" y2={200 - (tLower / 45.0) * 190} stroke="#0284c7" strokeDasharray="2 3" strokeWidth="1.2" />
                <text x="490" y={212 - (tLower / 45.0) * 190} fill="#0284c7" fontSize="9" fontFamily="monospace" fontWeight="bold">OFF: +{tLower}°C</text>

                {/* Ambient Waveform */}
                {history.length > 1 && (
                  <path
                    d={history.reduce((acc, pt, i) => {
                      const x = (i / (history.length - 1)) * 600;
                      const y = 200 - (pt.amb / 45.0) * 190;
                      return i === 0 ? `M ${x} ${y}` : `${acc} L ${x} ${y}`;
                    }, '')}
                    fill="none"
                    stroke="#d97706"
                    strokeWidth="1.8"
                    strokeDasharray="4 2"
                    opacity="0.75"
                  />
                )}

                {/* Chamber Temp History Path */}
                {history.length > 1 && (
                  <path
                    d={history.reduce((acc, pt, i) => {
                      const x = (i / (history.length - 1)) * 600;
                      const y = 200 - (pt.temp / 45.0) * 190;
                      return i === 0 ? `M ${x} ${y}` : `${acc} L ${x} ${y}`;
                    }, '')}
                    fill="none"
                    stroke="#0F766E"
                    strokeWidth="2.8"
                  />
                )}

                {/* Shading when Peltier Active */}
                {history.map((pt, i) => {
                  if (!pt.state || i === 0) return null;
                  const x = (i / (history.length - 1)) * 600;
                  return (
                    <rect key={i} x={x - 6} y="150" width="12" height="45" fill="#0284c7" fillOpacity="0.18" />
                  );
                })}
              </svg>
            </div>

            <div className="flex items-center justify-between text-[11px] font-mono text-slate-500 pt-2 border-t border-slate-200 mt-2">
              <span>Time Horizon: Past 45 Evaluation Steps</span>
              <span className="text-[#0F766E] font-semibold">Cyan Shaded Bands = Active Peltier Cooling</span>
            </div>
          </div>

        </div>

        {/* Right 4 Cols: Interactive Controls */}
        <div className="lg:col-span-4 flex flex-col gap-3.5">
          
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 flex flex-col gap-3.5">
            <div className="flex items-center justify-between">
              <h4 className="font-mono text-xs font-bold uppercase text-slate-800 flex items-center gap-1.5">
                <Sliders className="w-3.5 h-3.5 text-[#0F766E]" />
                Hysteresis Setpoints
              </h4>
              <span className="text-[10px] font-mono text-slate-600 bg-white px-2 py-0.5 rounded border border-slate-200 font-semibold">
                ΔT = {(tUpper - tLower).toFixed(1)}°C
              </span>
            </div>

            {/* Upper Threshold */}
            <div>
              <div className="flex justify-between text-xs font-mono mb-1">
                <span className="text-amber-800 font-semibold">Upper Trigger (Peltier ON)</span>
                <span className="font-bold text-[#0B2545]">+{tUpper.toFixed(1)}°C</span>
              </div>
              <input
                type="range"
                min="5.0"
                max="7.5"
                step="0.1"
                value={tUpper}
                onChange={e => { setTUpper(parseFloat(e.target.value)); sound.click(); }}
                className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-amber-600"
              />
              <span className="text-[10px] text-slate-500 block mt-0.5">
                Recommended: +6.2°C (Leaves 1.8°C margin before breach)
              </span>
            </div>

            {/* Lower Threshold */}
            <div>
              <div className="flex justify-between text-xs font-mono mb-1">
                <span className="text-cyan-800 font-semibold">Lower Cutoff (Peltier OFF)</span>
                <span className="font-bold text-[#0B2545]">+{tLower.toFixed(1)}°C</span>
              </div>
              <input
                type="range"
                min="2.5"
                max="4.5"
                step="0.1"
                value={tLower}
                onChange={e => { setTLower(parseFloat(e.target.value)); sound.click(); }}
                className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-[#0F766E]"
              />
              <span className="text-[10px] text-slate-500 block mt-0.5">
                Recommended: +3.8°C (Safely avoids 0°C to +2°C freeze shock)
              </span>
            </div>

            {/* Ambient Scenarios */}
            <div>
              <span className="text-xs font-mono text-slate-700 font-semibold block mb-1">
                Ambient Heat Stress Scenario:
              </span>
              <div className="grid grid-cols-3 gap-1.5">
                {(['moderate', 'diurnal', 'extreme'] as const).map(scen => (
                  <button
                    key={scen}
                    onClick={() => { setAmbientScenario(scen); sound.click(); }}
                    className={`px-2 py-1.5 rounded text-[11px] font-mono capitalize transition-colors cursor-pointer ${
                      ambientScenario === scen
                        ? 'bg-[#0F766E] text-white font-bold'
                        : 'bg-white border border-slate-200 text-slate-700 hover:bg-slate-100'
                    }`}
                  >
                    {scen === 'moderate' ? '32°C Const' : scen === 'diurnal' ? '28-42°C Diurnal' : '45°C Stress'}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Sensor Disconnection Fail-Safe Demo */}
          <div className={`p-4 rounded-xl border transition-all ${
            isSensorFault ? 'bg-rose-50 border-rose-300' : 'bg-slate-50 border-slate-200'
          }`}>
            <div className="flex items-center justify-between">
              <h4 className="font-mono text-xs font-bold uppercase text-slate-800 flex items-center gap-1.5">
                <ShieldAlert className="w-3.5 h-3.5 text-rose-600" />
                Fail-Safe Engineering
              </h4>
              <span className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded ${
                isSensorFault ? 'bg-rose-600 text-white animate-pulse' : 'bg-emerald-100 text-emerald-800 border border-emerald-300'
              }`}>
                {isSensorFault ? 'FAULT ACTIVE' : 'NOMINAL'}
              </span>
            </div>

            <p className="text-xs text-slate-600 mt-1.5 leading-snug">
              What prevents the Peltier from running continuously and freezing sensitive vaccines if a temperature sensor disconnects?
            </p>

            <button
              onClick={toggleSensorFault}
              className={`w-full mt-2.5 py-2 px-3 rounded-lg text-xs font-mono font-bold transition-all flex items-center justify-center gap-2 cursor-pointer ${
                isSensorFault
                  ? 'bg-rose-600 hover:bg-rose-700 text-white shadow-sm'
                  : 'bg-white hover:bg-slate-100 text-amber-800 border border-amber-300'
              }`}
            >
              <AlertOctagon className="w-4 h-4" />
              {isSensorFault ? 'RESTORE SENSOR CONNECTION' : 'SIMULATE SENSOR DISCONNECTION'}
            </button>

            {isSensorFault && (
              <div className="mt-2 p-2 bg-white rounded border border-rose-200 text-[10px] font-mono text-rose-800 space-y-0.5">
                <div>&gt; ERR 0x41: 1-WIRE TIMEOUT ON CORE PROBE</div>
                <div>&gt; FAIL-SAFE ACTIVE: MOSFET GATE DRIVER PULLED LOW</div>
                <div>&gt; PELTIER SHUT DOWN TO AVOID ACCIDENTAL FREEZING</div>
              </div>
            )}
          </div>

        </div>

      </div>

    </div>
  );
};

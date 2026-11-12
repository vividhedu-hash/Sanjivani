import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import type { ComponentSpec } from '../data/sanjivaniData';
import { COMPONENTS_3D } from '../data/sanjivaniData';
import { 
  Eye, 
  RotateCcw, 
  Layers, 
  Flame, 
  Snowflake, 
  Wind, 
  Compass, 
  AlertTriangle,
  Activity,
  Maximize2
} from 'lucide-react';
import { sound } from '../utils/soundEffects';

interface Model3DViewerProps {
  onSelectComponent?: (comp: ComponentSpec) => void;
  isSlideMode?: boolean;
}

export const Model3DViewer: React.FC<Model3DViewerProps> = ({ 
  onSelectComponent,
  isSlideMode = false
}) => {
  const mountRef = useRef<HTMLDivElement>(null);
  const [selectedComp, setSelectedComp] = useState<ComponentSpec>(COMPONENTS_3D[1]); // Default Bio-PCM
  const [isCutaway, setIsCutaway] = useState<boolean>(true);
  const [isLidOpen, setIsLidOpen] = useState<boolean>(true);
  const [isExploded, setIsExploded] = useState<boolean>(false);
  const [showAirflow, setShowAirflow] = useState<boolean>(true);
  const [showThermalFlow, setShowThermalFlow] = useState<boolean>(true);
  const [activeFilter, setActiveFilter] = useState<'all' | 'thermal' | 'mechanical' | 'electrical' | 'sensing'>('all');

  // Three.js instance state
  const threeState = useRef<{
    scene: THREE.Scene;
    camera: THREE.PerspectiveCamera;
    renderer: THREE.WebGLRenderer;
    parts: { [id: number]: THREE.Object3D };
    lidGroup: THREE.Group;
    cutawayGroup: THREE.Group;
    airflowIntake: THREE.LineSegments;
    airflowExhaustParticles: THREE.Points;
    airflowFinStreamlines: THREE.LineSegments;
    flowParticlesCold: THREE.Points;
    flowParticlesFluid: THREE.Points;
    fanBlades1: THREE.Group;
    fanBlades2: THREE.Group;
    orbitTarget: THREE.Vector3;
    isDragging: boolean;
    prevMouseX: number;
    prevMouseY: number;
    spherical: { radius: number; theta: number; phi: number };
  } | null>(null);

  useEffect(() => {
    if (!mountRef.current) return;

    const width = mountRef.current.clientWidth;
    const height = mountRef.current.clientHeight;

    // 1. Scene, Camera, Renderer
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xF1F5F9); // Clean Engineering Off-White / Slate 100

    const camera = new THREE.PerspectiveCamera(42, width / height, 0.1, 100);
    camera.position.set(7.8, 5.2, 9.2);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFShadowMap;

    mountRef.current.replaceChildren(renderer.domElement);

    // 2. High-End Studio Lighting for Light Mode
    const ambientLight = new THREE.AmbientLight(0xffffff, 1.1);
    scene.add(ambientLight);

    const keyLight = new THREE.DirectionalLight(0xffffff, 1.6);
    keyLight.position.set(12, 18, 12);
    keyLight.castShadow = true;
    keyLight.shadow.mapSize.width = 2048;
    keyLight.shadow.mapSize.height = 2048;
    keyLight.shadow.bias = -0.0001;
    scene.add(keyLight);

    const fillLight = new THREE.DirectionalLight(0xdbeafe, 0.9);
    fillLight.position.set(-10, 10, -8);
    scene.add(fillLight);

    // Warm ambient point light on hot-side heat sink
    const hotSinkLight = new THREE.PointLight(0xf59e0b, 2.0, 7);
    hotSinkLight.position.set(3.4, 0.2, 0.2);
    scene.add(hotSinkLight);

    // Soft cold point light inside payload cavity
    const coldCavityLight = new THREE.PointLight(0x38bdf8, 2.2, 5);
    coldCavityLight.position.set(0, 0.2, 0);
    scene.add(coldCavityLight);

    // Shadow Catcher Ground Plane
    const groundGeo = new THREE.PlaneGeometry(30, 30);
    const groundMat = new THREE.ShadowMaterial({ opacity: 0.12 });
    const groundMesh = new THREE.Mesh(groundGeo, groundMat);
    groundMesh.rotation.x = -Math.PI / 2;
    groundMesh.position.y = -2.6;
    groundMesh.receiveShadow = true;
    scene.add(groundMesh);

    // 3. Materials Library (Precision Matching Poster A-A Cutaway)
    const matOuterLLDPE = new THREE.MeshStandardMaterial({
      color: 0x1E293B, // Deep Slate
      roughness: 0.65,
      metalness: 0.2,
    });

    const matPUF = new THREE.MeshStandardMaterial({
      color: 0xFEF3C7, // Warm Cream PUF Foam
      roughness: 0.9,
      metalness: 0.05,
    });

    const matVIP = new THREE.MeshStandardMaterial({
      color: 0xE2E8F0, // Silver Metallic VIP Core
      roughness: 0.3,
      metalness: 0.75,
    });

    const matPCM = new THREE.MeshPhysicalMaterial({
      color: 0xBAE6FD, // Bio-PCM Ice Blue with crystalline transmission
      roughness: 0.15,
      metalness: 0.05,
      transmission: 0.75,
      thickness: 0.8,
      transparent: true,
      opacity: 0.88,
    });

    const matAluminium = new THREE.MeshStandardMaterial({
      color: 0xCBD5E1, // 6061-T6 Aircraft Aluminium
      roughness: 0.25,
      metalness: 0.85,
    });

    const matCopper = new THREE.MeshStandardMaterial({
      color: 0xB45309, // Pure C11000 Electrolytic Copper
      roughness: 0.28,
      metalness: 0.92,
    });

    const matPeltier = new THREE.MeshStandardMaterial({
      color: 0x0D9488, // Thermoelectric Module
      roughness: 0.35,
      metalness: 0.3,
    });

    const matFanHousing = new THREE.MeshStandardMaterial({
      color: 0x0F172A, // 80mm Fan Shroud
      roughness: 0.5,
      metalness: 0.2,
    });

    const matGlass = new THREE.MeshPhysicalMaterial({
      color: 0xE0F2FE,
      roughness: 0.1,
      metalness: 0.1,
      transmission: 0.9,
      thickness: 0.4,
      transparent: true,
      opacity: 0.92,
    });

    const matVaccine = new THREE.MeshStandardMaterial({
      color: 0x0284C7,
      roughness: 0.2,
      metalness: 0.1,
    });

    const matCap = new THREE.MeshStandardMaterial({
      color: 0xDC2626, // Red rubber stopper
      roughness: 0.5,
    });

    const partsMap: { [id: number]: THREE.Object3D } = {};
    const rootAssembly = new THREE.Group();
    scene.add(rootAssembly);

    // -----------------------------------------------------------
    // 4. ASSEMBLY GEOMETRY (Matching Section A-A of Research Poster)
    // -----------------------------------------------------------
    
    // A. Outer Shell & Insulation (Component 1)
    const enclosureGroup = new THREE.Group();
    const outerMesh = new THREE.Mesh(new THREE.BoxGeometry(4.3, 3.8, 3.5), matOuterLLDPE);
    outerMesh.castShadow = true;
    outerMesh.receiveShadow = true;
    enclosureGroup.add(outerMesh);

    // Side Carry Handles (LLDPE reinforced)
    const handleGeo = new THREE.CylinderGeometry(0.06, 0.06, 1.4, 12);
    const handleMat = new THREE.MeshStandardMaterial({ color: 0x334155, metalness: 0.6, roughness: 0.3 });
    const hLeft = new THREE.Mesh(handleGeo, handleMat);
    hLeft.rotation.z = Math.PI / 2;
    hLeft.position.set(-2.22, 0.4, 0);
    enclosureGroup.add(hLeft);

    // Middle PUF Insulation Shell
    const pufMesh = new THREE.Mesh(new THREE.BoxGeometry(3.9, 3.4, 3.1), matPUF);
    enclosureGroup.add(pufMesh);

    // Inner VIP Insulation Core
    const vipMesh = new THREE.Mesh(new THREE.BoxGeometry(3.5, 3.0, 2.7), matVIP);
    enclosureGroup.add(vipMesh);

    partsMap[1] = enclosureGroup;
    rootAssembly.add(enclosureGroup);

    // B. Bio-PCM Cassettes (Component 2: Left, Right & Bottom)
    const pcmGroup = new THREE.Group();
    // Left Cassette
    const pcmLeft = new THREE.Mesh(new THREE.BoxGeometry(0.48, 2.3, 2.1), matPCM);
    pcmLeft.position.set(-1.3, 0, 0);
    pcmGroup.add(pcmLeft);

    // Right Cassette
    const pcmRight = new THREE.Mesh(new THREE.BoxGeometry(0.48, 2.3, 2.1), matPCM);
    pcmRight.position.set(1.3, 0, 0);
    pcmGroup.add(pcmRight);

    // Bottom Cassette
    const pcmBottom = new THREE.Mesh(new THREE.BoxGeometry(2.2, 0.42, 2.1), matPCM);
    pcmBottom.position.set(0, -0.95, 0);
    pcmGroup.add(pcmBottom);

    partsMap[2] = pcmGroup;
    rootAssembly.add(pcmGroup);

    // C. Medical Payload Cavity & 24 Vaccine Vials (Component 3)
    const payloadGroup = new THREE.Group();
    
    // Aluminium 6061-T6 Heat Spreader Jacket (Component 7)
    const alJacket = new THREE.Mesh(new THREE.BoxGeometry(2.12, 1.85, 2.02), matAluminium);
    alJacket.position.set(0, 0.12, 0);
    payloadGroup.add(alJacket);
    partsMap[7] = alJacket;

    // Interior clinical white cavity
    const innerCavity = new THREE.Mesh(
      new THREE.BoxGeometry(1.95, 1.7, 1.85),
      new THREE.MeshStandardMaterial({ color: 0xF0FDF4, roughness: 0.3 })
    );
    innerCavity.position.set(0, 0.12, 0);
    payloadGroup.add(innerCavity);

    // 24 Vaccine Vials Tray Array (4 x 6 Grid)
    const vGeo = new THREE.CylinderGeometry(0.08, 0.08, 0.38, 16);
    const liqGeo = new THREE.CylinderGeometry(0.074, 0.074, 0.25, 16);
    const capGeo = new THREE.CylinderGeometry(0.085, 0.085, 0.06, 16);

    for (let x = -0.65; x <= 0.65; x += 0.42) {
      for (let z = -0.6; z <= 0.6; z += 0.25) {
        const vMesh = new THREE.Mesh(vGeo, matGlass);
        vMesh.position.set(x, -0.2, z);
        const lMesh = new THREE.Mesh(liqGeo, matVaccine);
        lMesh.position.set(x, -0.26, z);
        const cMesh = new THREE.Mesh(capGeo, matCap);
        cMesh.position.set(x, 0.01, z);
        payloadGroup.add(vMesh);
        payloadGroup.add(lMesh);
        payloadGroup.add(cMesh);
      }
    }

    partsMap[3] = payloadGroup;
    rootAssembly.add(payloadGroup);

    // D. DS18B20 1-Wire Digital Temperature Sensors (Component 4)
    const sensorGroup = new THREE.Group();
    const sensorGeo = new THREE.SphereGeometry(0.065, 16, 16);
    const matProbe = new THREE.MeshStandardMaterial({ 
      color: 0x7C3AED, 
      emissive: 0x6D28D9, 
      emissiveIntensity: 0.6 
    });

    const sCore = new THREE.Mesh(sensorGeo, matProbe);
    sCore.position.set(0, 0.05, 0);
    sensorGroup.add(sCore);

    const sPCM = new THREE.Mesh(sensorGeo, matProbe);
    sPCM.position.set(-1.1, 0.35, 0.4);
    sensorGroup.add(sPCM);

    const sCold = new THREE.Mesh(sensorGeo, matProbe);
    sCold.position.set(1.55, 0.05, 0);
    sensorGroup.add(sCold);

    // Sensor wire harness lines
    const wireMat = new THREE.LineBasicMaterial({ color: 0x7C3AED, linewidth: 2 });
    const wireGeo = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(0, 0.05, 0),
      new THREE.Vector3(0, 1.8, 0),
      new THREE.Vector3(0.8, 2.0, 0.6)
    ]);
    const wireLine = new THREE.Line(wireGeo, wireMat);
    sensorGroup.add(wireLine);

    partsMap[4] = sensorGroup;
    rootAssembly.add(sensorGroup);

    // E. Thermoelectric Heat Pump & Heat Rejection (Components 5, 6, 8, 9, 10, 11)
    const tecAssembly = new THREE.Group();
    tecAssembly.position.set(2.45, 0.05, 0);

    // Cold-side copper cold plate (Component 8)
    const coldPlateMesh = new THREE.Mesh(new THREE.BoxGeometry(0.24, 1.35, 1.35), matCopper);
    coldPlateMesh.position.set(-0.35, 0, 0);
    tecAssembly.add(coldPlateMesh);
    partsMap[8] = coldPlateMesh;

    // Arctic MX-4 TIM Layer (Component 6)
    const timColdMesh = new THREE.Mesh(new THREE.BoxGeometry(0.04, 1.25, 1.25), matAluminium);
    timColdMesh.position.set(-0.21, 0, 0);
    tecAssembly.add(timColdMesh);
    partsMap[6] = timColdMesh;

    // Dual TEC1-12706 Modules (Component 5)
    const tec1Mesh = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.48, 0.48), matPeltier);
    tec1Mesh.position.set(-0.12, 0.35, 0);
    tecAssembly.add(tec1Mesh);

    const tec2Mesh = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.48, 0.48), matPeltier);
    tec2Mesh.position.set(-0.12, -0.35, 0);
    tecAssembly.add(tec2Mesh);
    partsMap[5] = tecAssembly;

    // Hot-side Copper Base (Component 9)
    const hotBaseMesh = new THREE.Mesh(new THREE.BoxGeometry(0.26, 1.45, 1.45), matCopper);
    hotBaseMesh.position.set(0.08, 0, 0);
    tecAssembly.add(hotBaseMesh);
    partsMap[9] = hotBaseMesh;

    // Sintered Copper Heat Pipes (4x curved heat pipes)
    const pipeMat = new THREE.MeshStandardMaterial({ color: 0xD97706, metalness: 0.95, roughness: 0.2 });
    for (let p = -0.45; p <= 0.45; p += 0.3) {
      const pipeGeo = new THREE.CylinderGeometry(0.04, 0.04, 0.7, 12);
      const pipe = new THREE.Mesh(pipeGeo, pipeMat);
      pipe.rotation.z = Math.PI / 2;
      pipe.position.set(0.45, p, 0);
      tecAssembly.add(pipe);
    }

    // Skived Extruded Fin Stack (Component 10: 24 aluminium fins)
    const finStackGroup = new THREE.Group();
    finStackGroup.position.set(0.9, 0, 0);
    for (let fy = -0.65; fy <= 0.65; fy += 0.055) {
      const finMesh = new THREE.Mesh(new THREE.BoxGeometry(1.0, 0.016, 1.45), matAluminium);
      finMesh.position.set(0, fy, 0);
      finStackGroup.add(finMesh);
    }
    tecAssembly.add(finStackGroup);
    partsMap[10] = finStackGroup;

    // Dual 80mm PWM Forced Convection Fans (Component 11)
    const fanAssembly = new THREE.Group();
    fanAssembly.position.set(1.52, 0, 0);

    const fan1Frame = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.76, 0.76), matFanHousing);
    fan1Frame.position.set(0, 0.42, 0);
    fanAssembly.add(fan1Frame);

    const fan2Frame = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.76, 0.76), matFanHousing);
    fan2Frame.position.set(0, -0.42, 0);
    fanAssembly.add(fan2Frame);

    // Rotating Blades
    const fanBlades1 = new THREE.Group();
    fanBlades1.position.set(0.1, 0.42, 0);
    for (let b = 0; b < 7; b++) {
      const blade = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.32, 0.09), matFanHousing);
      blade.rotation.x = (b * Math.PI * 2) / 7;
      fanBlades1.add(blade);
    }
    fanAssembly.add(fanBlades1);

    const fanBlades2 = new THREE.Group();
    fanBlades2.position.set(0.1, -0.42, 0);
    for (let b = 0; b < 7; b++) {
      const blade = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.32, 0.09), matFanHousing);
      blade.rotation.x = (b * Math.PI * 2) / 7;
      fanBlades2.add(blade);
    }
    fanAssembly.add(fanBlades2);

    tecAssembly.add(fanAssembly);
    partsMap[11] = fanAssembly;
    rootAssembly.add(tecAssembly);

    // F. Micro DC Diaphragm Pump & Teal Silicone Fluid Tubing
    const pumpMesh = new THREE.Mesh(
      new THREE.BoxGeometry(1.4, 0.65, 0.8),
      new THREE.MeshStandardMaterial({ color: 0x4338CA, metalness: 0.5, roughness: 0.3 })
    );
    pumpMesh.position.set(0.6, -2.15, 0.6);
    rootAssembly.add(pumpMesh);

    // Teal silicone tubing loops
    const tubeMat = new THREE.MeshStandardMaterial({ color: 0x06B6D4, roughness: 0.3, transparent: true, opacity: 0.85 });
    const tube1 = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.045, 2.2, 12), tubeMat);
    tube1.position.set(1.4, -1.0, 0.6);
    rootAssembly.add(tube1);

    // G. Control Electronics & OLED Display (Component 12)
    const ctrlGroup = new THREE.Group();
    ctrlGroup.position.set(0.6, 2.15, 0.6);
    const pcbMesh = new THREE.Mesh(new THREE.BoxGeometry(1.3, 0.12, 0.95), new THREE.MeshStandardMaterial({ color: 0x0F172A }));
    ctrlGroup.add(pcbMesh);

    // Illuminated OLED Screen
    const oledMesh = new THREE.Mesh(
      new THREE.BoxGeometry(0.42, 0.05, 0.32),
      new THREE.MeshStandardMaterial({ color: 0x000000, emissive: 0x0284C7, emissiveIntensity: 0.9 })
    );
    oledMesh.position.set(0.28, 0.07, 0);
    ctrlGroup.add(oledMesh);
    partsMap[12] = ctrlGroup;
    rootAssembly.add(ctrlGroup);

    // H. 12.8V 30Ah LiFePO4 Battery Pack (Component 13)
    const batGroup = new THREE.Group();
    batGroup.position.set(0.0, -2.25, 0.0);
    const batMesh = new THREE.Mesh(
      new THREE.BoxGeometry(3.2, 0.68, 2.3),
      new THREE.MeshStandardMaterial({ color: 0x1E293B, metalness: 0.4, roughness: 0.5 })
    );
    batMesh.castShadow = true;
    batGroup.add(batMesh);
    partsMap[13] = batGroup;
    rootAssembly.add(batGroup);

    // I. Openable Insulated Lid with Mechanical Latch
    const lidGroup = new THREE.Group();
    lidGroup.position.set(0, 1.9, -1.75); // Rear hinge pivot
    const lidMesh = new THREE.Mesh(new THREE.BoxGeometry(4.35, 0.45, 3.55), matOuterLLDPE);
    lidMesh.position.set(0, 0.22, 1.75);
    lidMesh.castShadow = true;
    lidGroup.add(lidMesh);

    // Front Chrome Cam Latch
    const latchMesh = new THREE.Mesh(
      new THREE.BoxGeometry(0.35, 0.5, 0.12),
      new THREE.MeshStandardMaterial({ color: 0x94A3B8, metalness: 0.9, roughness: 0.2 })
    );
    latchMesh.position.set(0, 0.1, 3.55);
    lidGroup.add(latchMesh);

    rootAssembly.add(lidGroup);

    // -----------------------------------------------------------
    // 5. UPGRADED REALISTIC 3D AIRFLOW & THERMAL VECTORS
    // -----------------------------------------------------------

    // A. Cool Intake Airflow Streamlines (Curved Blue Lines drawing into fans)
    const intakeLineCoords: number[] = [];
    for (let i = 0; i < 40; i++) {
      const startX = 5.2 + Math.random() * 1.5;
      const startY = (Math.random() - 0.5) * 2.2;
      const startZ = (Math.random() - 0.5) * 1.8;
      // Intake curves toward fan center at (3.9, y, 0)
      const fanCenterY = startY > 0 ? 0.47 : -0.37;
      intakeLineCoords.push(
        startX, startY, startZ,
        4.0, fanCenterY, startZ * 0.4
      );
    }
    const intakeGeo = new THREE.BufferGeometry();
    intakeGeo.setAttribute('position', new THREE.Float32BufferAttribute(intakeLineCoords, 3));
    const intakeMat = new THREE.LineBasicMaterial({ 
      color: 0x0284C7, 
      transparent: true, 
      opacity: 0.65,
      linewidth: 1.5
    });
    const airflowIntake = new THREE.LineSegments(intakeGeo, intakeMat);
    scene.add(airflowIntake);

    // B. Accelerated Fin Streamlines (Horizontal air vectors slicing between fins)
    const finLineCoords: number[] = [];
    for (let f = -0.55; f <= 0.55; f += 0.08) {
      for (let z = -0.6; z <= 0.6; z += 0.2) {
        finLineCoords.push(
          2.5, f, z,
          3.9, f, z
        );
      }
    }
    const finGeo = new THREE.BufferGeometry();
    finGeo.setAttribute('position', new THREE.Float32BufferAttribute(finLineCoords, 3));
    const finAirMat = new THREE.LineBasicMaterial({ 
      color: 0x38BDF8, 
      transparent: true, 
      opacity: 0.7 
    });
    const airflowFinStreamlines = new THREE.LineSegments(finGeo, finAirMat);
    scene.add(airflowFinStreamlines);

    // C. Heated Hot Exhaust Turbulent Airflow Plume (Expanding Orange/Red Stream)
    const exhaustCount = 550;
    const exhaustGeo = new THREE.BufferGeometry();
    const exhaustPos = new Float32Array(exhaustCount * 3);
    for (let i = 0; i < exhaustCount; i++) {
      exhaustPos[i * 3 + 0] = 4.0 + Math.random() * 2.8; // Moving outward to x = 6.8
      exhaustPos[i * 3 + 1] = (Math.random() - 0.5) * 1.6;
      exhaustPos[i * 3 + 2] = (Math.random() - 0.5) * 1.6;
    }
    exhaustGeo.setAttribute('position', new THREE.BufferAttribute(exhaustPos, 3));
    const exhaustMat = new THREE.PointsMaterial({
      color: 0xEA580C, // Hot Amber/Orange
      size: 0.09,
      transparent: true,
      opacity: 0.85,
      blending: THREE.NormalBlending
    });
    const airflowExhaustParticles = new THREE.Points(exhaustGeo, exhaustMat);
    scene.add(airflowExhaustParticles);

    // D. Cold-Side Thermal Extraction Particles (Payload to Cold Plate)
    const coldCount = 300;
    const geoCold = new THREE.BufferGeometry();
    const posCold = new Float32Array(coldCount * 3);
    for (let i = 0; i < coldCount; i++) {
      posCold[i * 3 + 0] = (Math.random() - 0.5) * 2.1;
      posCold[i * 3 + 1] = (Math.random() - 0.5) * 1.6;
      posCold[i * 3 + 2] = (Math.random() - 0.5) * 1.9;
    }
    geoCold.setAttribute('position', new THREE.BufferAttribute(posCold, 3));
    const matCold = new THREE.PointsMaterial({
      color: 0x0284C7,
      size: 0.075,
      transparent: true,
      opacity: 0.85
    });
    const flowParticlesCold = new THREE.Points(geoCold, matCold);
    scene.add(flowParticlesCold);

    // E. Liquid Coolant Loop Particles
    const fluidCount = 160;
    const geoFluid = new THREE.BufferGeometry();
    const posFluid = new Float32Array(fluidCount * 3);
    for (let i = 0; i < fluidCount; i++) {
      const angle = (i / fluidCount) * Math.PI * 2;
      posFluid[i * 3 + 0] = Math.cos(angle) * 1.3 + 0.6;
      posFluid[i * 3 + 1] = Math.sin(angle) * 0.7 - 0.2;
      posFluid[i * 3 + 2] = 0.95;
    }
    geoFluid.setAttribute('position', new THREE.BufferAttribute(posFluid, 3));
    const flowParticlesFluid = new THREE.Points(
      geoFluid, 
      new THREE.PointsMaterial({ color: 0x06B6D4, size: 0.065, transparent: true, opacity: 0.9 })
    );
    scene.add(flowParticlesFluid);

    // 6. Camera Orbit Spherical Controls
    const spherical = {
      radius: isSlideMode ? 10.5 : 11.5,
      theta: 0.85,
      phi: 1.15
    };
    const orbitTarget = new THREE.Vector3(0.5, 0.0, 0.0);

    const updateCameraPos = () => {
      camera.position.x = orbitTarget.x + spherical.radius * Math.sin(spherical.phi) * Math.sin(spherical.theta);
      camera.position.y = orbitTarget.y + spherical.radius * Math.cos(spherical.phi);
      camera.position.z = orbitTarget.z + spherical.radius * Math.sin(spherical.phi) * Math.cos(spherical.theta);
      camera.lookAt(orbitTarget);
    };
    updateCameraPos();

    // Mouse & Touch Orbit Controls
    let isDragging = false;
    let prevMouseX = 0;
    let prevMouseY = 0;
    const dom = renderer.domElement;

    const onMouseDown = (e: MouseEvent) => {
      isDragging = true;
      prevMouseX = e.clientX;
      prevMouseY = e.clientY;
    };

    const onMouseMove = (e: MouseEvent) => {
      if (!isDragging) return;
      const deltaX = e.clientX - prevMouseX;
      const deltaY = e.clientY - prevMouseY;
      prevMouseX = e.clientX;
      prevMouseY = e.clientY;

      spherical.theta -= deltaX * 0.007;
      spherical.phi = Math.max(0.2, Math.min(Math.PI / 2 + 0.25, spherical.phi - deltaY * 0.007));
      updateCameraPos();
    };

    const onMouseUp = () => {
      isDragging = false;
    };

    const onWheel = (e: WheelEvent) => {
      e.preventDefault();
      spherical.radius = Math.max(5.0, Math.min(20.0, spherical.radius + e.deltaY * 0.012));
      updateCameraPos();
    };

    dom.addEventListener('mousedown', onMouseDown);
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
    dom.addEventListener('wheel', onWheel, { passive: false });

    // Touch support for tablet/laptop touchscreens
    const onTouchStart = (e: TouchEvent) => {
      if (e.touches.length === 1) {
        isDragging = true;
        prevMouseX = e.touches[0].clientX;
        prevMouseY = e.touches[0].clientY;
      }
    };
    const onTouchMove = (e: TouchEvent) => {
      if (!isDragging || e.touches.length !== 1) return;
      const deltaX = e.touches[0].clientX - prevMouseX;
      const deltaY = e.touches[0].clientY - prevMouseY;
      prevMouseX = e.touches[0].clientX;
      prevMouseY = e.touches[0].clientY;
      spherical.theta -= deltaX * 0.007;
      spherical.phi = Math.max(0.2, Math.min(Math.PI / 2 + 0.25, spherical.phi - deltaY * 0.007));
      updateCameraPos();
    };
    const onTouchEnd = () => {
      isDragging = false;
    };

    dom.addEventListener('touchstart', onTouchStart);
    window.addEventListener('touchmove', onTouchMove);
    window.addEventListener('touchend', onTouchEnd);

    const handleResize = () => {
      if (!mountRef.current) return;
      const w = mountRef.current.clientWidth;
      const h = mountRef.current.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };
    window.addEventListener('resize', handleResize);

    threeState.current = {
      scene,
      camera,
      renderer,
      parts: partsMap,
      lidGroup,
      cutawayGroup: enclosureGroup,
      airflowIntake,
      airflowExhaustParticles,
      airflowFinStreamlines,
      flowParticlesCold,
      flowParticlesFluid,
      fanBlades1,
      fanBlades2,
      orbitTarget,
      isDragging,
      prevMouseX,
      prevMouseY,
      spherical
    };

    // 7. Render Loop with Realistic Airflow Motion
    let animFrameId: number;
    const startTime = performance.now();

    const animate = () => {
      animFrameId = requestAnimationFrame(animate);
      const elapsedTime = (performance.now() - startTime) * 0.001;

      // Spin PWM Fan Blades
      fanBlades1.rotation.x += 0.28;
      fanBlades2.rotation.x += 0.28;

      // Animate Turbulent Hot Air Exhaust Plume (Outward velocity x -> 6.8)
      const hPos = airflowExhaustParticles.geometry.attributes.position.array as Float32Array;
      for (let i = 0; i < exhaustCount; i++) {
        hPos[i * 3 + 0] += 0.045; // Outward forced velocity
        hPos[i * 3 + 1] += Math.sin(elapsedTime * 3 + i) * 0.005;
        if (hPos[i * 3 + 0] > 6.8) {
          hPos[i * 3 + 0] = 4.0;
        }
      }
      airflowExhaustParticles.geometry.attributes.position.needsUpdate = true;

      // Animate Cold Extraction Flow toward Peltier
      const cPos = flowParticlesCold.geometry.attributes.position.array as Float32Array;
      for (let i = 0; i < coldCount; i++) {
        cPos[i * 3 + 0] += 0.016;
        if (cPos[i * 3 + 0] > 2.1) {
          cPos[i * 3 + 0] = -1.2;
        }
      }
      flowParticlesCold.geometry.attributes.position.needsUpdate = true;

      // Animate Fluid Loop Circulation
      flowParticlesFluid.rotation.z += 0.018;

      renderer.render(scene, camera);
    };

    animate();

    return () => {
      cancelAnimationFrame(animFrameId);
      dom.removeEventListener('mousedown', onMouseDown);
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('mouseup', onMouseUp);
      dom.removeEventListener('wheel', onWheel);
      dom.removeEventListener('touchstart', onTouchStart);
      window.removeEventListener('touchmove', onTouchMove);
      window.removeEventListener('touchend', onTouchEnd);
      window.removeEventListener('resize', handleResize);
      renderer.dispose();
    };
  }, [isSlideMode]);

  // Update Cutaway & Lid State
  useEffect(() => {
    if (!threeState.current) return;
    const { cutawayGroup, lidGroup } = threeState.current;

    cutawayGroup.traverse((child) => {
      if (child instanceof THREE.Mesh) {
        if (isCutaway) {
          child.material.transparent = true;
          child.material.opacity = 0.28;
        } else {
          child.material.transparent = false;
          child.material.opacity = 1.0;
        }
      }
    });

    lidGroup.rotation.x = isLidOpen ? -0.92 : 0.0;
  }, [isCutaway, isLidOpen]);

  // Update Exploded View
  useEffect(() => {
    if (!threeState.current) return;
    const { parts } = threeState.current;
    const offset = isExploded ? 1.6 : 0.0;

    if (parts[1]) parts[1].position.z = -offset * 0.8;
    if (parts[2]) parts[2].position.x = -offset * 0.7;
    if (parts[3]) parts[3].position.y = offset * 0.4;
    if (parts[5]) parts[5].position.x = 2.45 + offset * 1.1;
    if (parts[13]) parts[13].position.y = -2.25 - offset * 0.8;
    if (parts[12]) parts[12].position.y = 2.15 + offset * 0.7;
  }, [isExploded]);

  // Update Airflow & Thermal Visibility
  useEffect(() => {
    if (!threeState.current) return;
    const { 
      airflowIntake, 
      airflowExhaustParticles, 
      airflowFinStreamlines, 
      flowParticlesCold, 
      flowParticlesFluid 
    } = threeState.current;

    airflowIntake.visible = showAirflow;
    airflowExhaustParticles.visible = showAirflow;
    airflowFinStreamlines.visible = showAirflow;
    flowParticlesCold.visible = showThermalFlow;
    flowParticlesFluid.visible = showThermalFlow;
  }, [showAirflow, showThermalFlow]);

  const selectComponent = (comp: ComponentSpec) => {
    setSelectedComp(comp);
    sound.click();
    if (onSelectComponent) onSelectComponent(comp);

    if (threeState.current) {
      const { spherical } = threeState.current;
      if (comp.id === 5 || comp.id === 9 || comp.id === 10 || comp.id === 11) {
        spherical.theta = 0.45;
        spherical.phi = 1.25;
        spherical.radius = isSlideMode ? 8.0 : 8.8;
      } else if (comp.id === 13) {
        spherical.phi = 1.65;
        spherical.radius = isSlideMode ? 8.5 : 9.2;
      } else if (comp.id === 12) {
        spherical.phi = 0.75;
        spherical.radius = isSlideMode ? 8.0 : 8.8;
      } else {
        spherical.theta = 0.85;
        spherical.phi = 1.15;
        spherical.radius = isSlideMode ? 10.5 : 11.5;
      }
    }
  };

  const resetCamera = () => {
    sound.click();
    if (threeState.current) {
      threeState.current.spherical.radius = isSlideMode ? 10.5 : 11.5;
      threeState.current.spherical.theta = 0.85;
      threeState.current.spherical.phi = 1.15;
    }
  };

  const filteredComponents = COMPONENTS_3D.filter(c => 
    activeFilter === 'all' ? true : c.category === activeFilter
  );

  return (
    <div className={`relative w-full rounded-2xl overflow-hidden bg-white border border-slate-200 shadow-xl flex flex-col lg:flex-row ${
      isSlideMode ? 'h-[540px]' : 'h-[780px]'
    }`}>
      
      {/* 3D Canvas Area */}
      <div className="relative flex-1 h-[420px] lg:h-full bg-slate-50">
        <div ref={mountRef} className="w-full h-full cursor-grab active:cursor-grabbing" />

        {/* Top Badges */}
        <div className="absolute top-3 left-3 z-10 flex flex-wrap items-center gap-2">
          <span className="px-3 py-1 text-xs font-mono font-bold uppercase tracking-wider bg-[#0F766E] text-white rounded-full shadow-md">
            Interactive 3D Cutaway Box
          </span>
          <span className="px-3 py-1 text-xs font-mono text-slate-700 bg-white/90 rounded-full border border-slate-200 shadow-sm">
            Drag to Rotate • Pinch/Scroll to Zoom
          </span>
        </div>

        {/* Floating Toolbar Controls */}
        <div className="absolute bottom-4 left-3 z-10 flex flex-wrap gap-2 bg-white/95 backdrop-blur-md p-2 rounded-xl border border-slate-200 shadow-lg">
          <button
            onClick={() => { setIsCutaway(!isCutaway); sound.click(); }}
            className={`px-3 py-1.5 text-xs font-mono font-semibold rounded-lg flex items-center gap-1.5 transition-all ${
              isCutaway ? 'bg-[#0F766E] text-white shadow-sm' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
            }`}
          >
            <Eye className="w-3.5 h-3.5" />
            {isCutaway ? 'Cutaway ON' : 'Solid Shell'}
          </button>

          <button
            onClick={() => { setIsLidOpen(!isLidOpen); sound.click(); }}
            className={`px-3 py-1.5 text-xs font-mono font-semibold rounded-lg flex items-center gap-1.5 transition-all ${
              isLidOpen ? 'bg-cyan-600 text-white shadow-sm' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
            }`}
          >
            <Layers className="w-3.5 h-3.5" />
            {isLidOpen ? 'Lid OPEN' : 'Lid CLOSED'}
          </button>

          <button
            onClick={() => { setIsExploded(!isExploded); sound.click(); }}
            className={`px-3 py-1.5 text-xs font-mono font-semibold rounded-lg flex items-center gap-1.5 transition-all ${
              isExploded ? 'bg-amber-600 text-white shadow-sm' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
            }`}
          >
            <Compass className="w-3.5 h-3.5" />
            {isExploded ? 'Exploded ON' : 'Assemble Parts'}
          </button>

          <button
            onClick={() => { setShowAirflow(!showAirflow); sound.click(); }}
            className={`px-3 py-1.5 text-xs font-mono font-semibold rounded-lg flex items-center gap-1.5 transition-all ${
              showAirflow ? 'bg-indigo-600 text-white shadow-sm' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
            }`}
          >
            <Wind className="w-3.5 h-3.5" />
            Realistic Airflow
          </button>

          <button
            onClick={resetCamera}
            className="p-1.5 rounded-lg bg-slate-100 text-slate-700 hover:bg-slate-200 transition-colors"
            title="Reset Camera View"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
        </div>

        {/* First Law Physics Principle Floating Note */}
        <div className="absolute top-3 right-3 max-w-xs hidden sm:block z-10">
          <div className="bg-amber-50/95 border border-amber-300 rounded-xl p-3 shadow-md text-amber-900 text-xs">
            <div className="flex items-center gap-1.5 font-mono font-bold text-amber-800 mb-0.5">
              <AlertTriangle className="w-4 h-4 text-amber-600" />
              FIRST LAW THERMODYNAMICS
            </div>
            <p className="leading-snug text-[11px] text-amber-800">
              <strong>The Peltier does not destroy heat.</strong> Hot side must forcibly reject pumped cold heat + electrical waste:
            </p>
            <div className="mt-1 font-mono text-[10px] text-amber-900 font-bold bg-amber-100 px-2 py-0.5 rounded border border-amber-300">
              Q̇_hot = Q̇_cold + P_elec = 18.5W + 30W = 48.5 W
            </div>
          </div>
        </div>
      </div>

      {/* Right Sidebar: Subsystem Inspection & Technical Specs */}
      <div className="w-full lg:w-[380px] h-[340px] lg:h-full bg-white border-t lg:border-t-0 lg:border-l border-slate-200 flex flex-col">
        
        {/* Header & Category Filters */}
        <div className="p-3.5 border-b border-slate-200 bg-slate-50/80">
          <div className="flex items-center justify-between mb-2">
            <h3 className="font-serif-display text-base font-bold text-[#0B2545]">
              Subsystem Inspector
            </h3>
            <span className="text-[10px] font-mono text-[#0F766E] bg-teal-50 px-2 py-0.5 rounded-full border border-teal-200 font-semibold">
              13 Subsystems
            </span>
          </div>

          <div className="flex flex-wrap gap-1">
            {(['all', 'thermal', 'mechanical', 'electrical', 'sensing'] as const).map(cat => (
              <button
                key={cat}
                onClick={() => { setActiveFilter(cat); sound.click(); }}
                className={`px-2 py-0.5 text-[10px] font-mono uppercase rounded-md transition-colors ${
                  activeFilter === cat 
                    ? 'bg-[#0F766E] text-white font-bold' 
                    : 'bg-slate-200/80 text-slate-700 hover:bg-slate-300'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        {/* Selected Component Telemetry Details */}
        <div className="p-3.5 border-b border-slate-200 bg-white">
          <div className="flex items-start justify-between">
            <div>
              <span className="text-[9px] font-mono text-slate-500 uppercase tracking-widest block">
                ID #{selectedComp.id.toString().padStart(2, '0')} • {selectedComp.category}
              </span>
              <h4 className="font-bold text-[#0B2545] text-sm mt-0.5">
                {selectedComp.name}
              </h4>
            </div>
            <span className={`text-[9px] font-mono font-bold px-1.5 py-0.5 rounded ${
              selectedComp.heatFluxRole === 'cold' ? 'bg-cyan-100 text-cyan-800' :
              selectedComp.heatFluxRole === 'hot' ? 'bg-amber-100 text-amber-800' :
              selectedComp.heatFluxRole === 'passive' ? 'bg-emerald-100 text-emerald-800' :
              'bg-purple-100 text-purple-800'
            }`}>
              {selectedComp.heatFluxRole.toUpperCase()}
            </span>
          </div>

          <div className="mt-2 space-y-1.5 text-xs">
            <div>
              <span className="text-slate-500 font-mono text-[10px] block">Role:</span>
              <p className="text-slate-700 text-[11px] leading-tight">{selectedComp.role}</p>
            </div>
            <div>
              <span className="text-slate-500 font-mono text-[10px] block">Scientific Principle:</span>
              <p className="text-slate-700 text-[11px] italic leading-tight">{selectedComp.principle}</p>
            </div>
            <div className="bg-slate-50 p-2 rounded-lg border border-slate-200">
              <span className="text-[#0F766E] font-mono text-[10px] block font-bold">Specification:</span>
              <p className="text-slate-900 font-mono text-[10px] mt-0.5 leading-snug">{selectedComp.specs}</p>
            </div>
            <p className="text-slate-600 text-[10px] leading-relaxed pt-0.5 line-clamp-3">
              {selectedComp.details}
            </p>
          </div>
        </div>

        {/* Scrollable Subsystems List */}
        <div className="flex-1 overflow-y-auto p-2 space-y-1 divide-y divide-slate-100">
          {filteredComponents.map(c => (
            <button
              key={c.id}
              onClick={() => selectComponent(c)}
              className={`w-full text-left p-2 rounded-lg text-xs transition-all flex items-center justify-between ${
                selectedComp.id === c.id 
                  ? 'bg-teal-50 border border-teal-500 text-[#0F766E] font-bold' 
                  : 'text-slate-700 hover:bg-slate-50 border border-transparent'
              }`}
            >
              <div className="flex items-center gap-1.5">
                <span className="w-4 h-4 rounded-full bg-slate-200 text-[9px] font-mono flex items-center justify-center font-bold text-slate-700">
                  {c.id}
                </span>
                <span className="truncate max-w-[210px] text-[11px]">{c.name}</span>
              </div>
              <span className="text-[9px] font-mono text-slate-500 uppercase">
                {c.category.slice(0, 4)}
              </span>
            </button>
          ))}
        </div>

      </div>

    </div>
  );
};

import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import type { ComponentSpec } from '../data/sanjivaniData';
import { COMPONENTS_3D } from '../data/sanjivaniData';
import { 
  Eye, 
  RotateCcw, 
  Flame, 
  Snowflake, 
  Wind, 
  Maximize2,
  Layers,
  Sparkles
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
  const [showAirflow, setShowAirflow] = useState<boolean>(true);
  const [showThermalFlow, setShowThermalFlow] = useState<boolean>(true);
  const [activeFilter, setActiveFilter] = useState<'all' | 'thermal' | 'mechanical' | 'electrical' | 'sensing'>('all');
  const [explodedPercent, setExplodedPercent] = useState<number>(0); // 0 to 100%

  // Three.js instance state
  const threeState = useRef<{
    scene: THREE.Scene;
    camera: THREE.PerspectiveCamera;
    renderer: THREE.WebGLRenderer;
    parts: { [id: number]: THREE.Object3D };
    lidPivot: THREE.Group;
    frontWall: THREE.Mesh;
    frontCutawayRims: THREE.Group;
    pcmGroup: THREE.Group;
    payloadGroup: THREE.Group;
    peltierStackGroup: THREE.Group;
    heatSinkFanGroup: THREE.Group;
    liquidChamberGroup: THREE.Group;
    ctrlUnitGroup: THREE.Group;
    airflowExhaustParticles: THREE.Points;
    airflowIntakeLines: THREE.LineSegments;
    flowParticlesCold: THREE.Points;
    flowParticlesFluid: THREE.Points;
    fanBlades: THREE.Group;
    orbitTarget: THREE.Vector3;
    isDragging: boolean;
    prevMouseX: number;
    prevMouseY: number;
    spherical: { radius: number; theta: number; phi: number };
    currentExplode: number;
    targetExplode: number;
  } | null>(null);

  useEffect(() => {
    if (!mountRef.current) return;

    const width = mountRef.current.clientWidth;
    const height = mountRef.current.clientHeight;

    // 1. Scene, Camera, Renderer (Dark Sci-Fi Medical Studio)
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x060B14); // Deep Obsidian
    scene.fog = new THREE.FogExp2(0x060B14, 0.035);

    const camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 100);
    camera.position.set(6.8, 4.2, 8.5);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFShadowMap;

    mountRef.current.replaceChildren(renderer.domElement);

    // 2. High-Tech Studio Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.85);
    scene.add(ambientLight);

    const keyLight = new THREE.DirectionalLight(0xdbeafe, 1.8);
    keyLight.position.set(10, 16, 12);
    keyLight.castShadow = true;
    keyLight.shadow.mapSize.width = 2048;
    keyLight.shadow.mapSize.height = 2048;
    keyLight.shadow.bias = -0.0001;
    scene.add(keyLight);

    const fillLight = new THREE.DirectionalLight(0x0f766e, 1.2);
    fillLight.position.set(-10, 8, -8);
    scene.add(fillLight);

    const rimLight = new THREE.DirectionalLight(0x38bdf8, 1.4);
    rimLight.position.set(0, -6, 10);
    scene.add(rimLight);

    // Warm point light at heat sink exhaust
    const hotSinkLight = new THREE.PointLight(0xf59e0b, 2.8, 6);
    hotSinkLight.position.set(2.4, -0.6, 0.5);
    scene.add(hotSinkLight);

    // Cool point light inside vaccine cavity
    const coldCavityLight = new THREE.PointLight(0x38bdf8, 3.2, 5);
    coldCavityLight.position.set(-0.1, 0.9, 0.3);
    scene.add(coldCavityLight);

    // Sci-Fi Tech Ground Grid
    const gridHelper = new THREE.GridHelper(30, 30, 0x14b8a6, 0x1e293b);
    gridHelper.position.y = -2.3;
    scene.add(gridHelper);

    // -----------------------------------------------------------
    // 3. MATERIALS LIBRARY (High-Tech Medical Prototype)
    // -----------------------------------------------------------
    
    // Main Medical Cooler Outer Shell (Clean White with subtle pearl reflection)
    const matCoolerBody = new THREE.MeshStandardMaterial({
      color: 0xF8FAFC,
      roughness: 0.28,
      metalness: 0.15,
    });

    // Dark Medical Shell Interior
    const matCoolerDark = new THREE.MeshStandardMaterial({
      color: 0x0F172A,
      roughness: 0.45,
      metalness: 0.25,
    });

    // Vivid Royal Medical Blue for Corner Protectors & Latches
    const matBlueTrim = new THREE.MeshStandardMaterial({
      color: 0x1D4ED8,
      roughness: 0.3,
      metalness: 0.35,
    });

    // High-Density PU Foam Core Insulation
    const matPUFoam = new THREE.MeshStandardMaterial({
      color: 0xD4A373,
      roughness: 0.92,
      metalness: 0.05,
    });

    // Dark Gasket / Seal on Lid
    const matGasket = new THREE.MeshStandardMaterial({
      color: 0x0F172A,
      roughness: 0.8,
    });

    // 6061-T6 Aircraft Aluminium Heat Spreader & Shelf
    const matAluminium = new THREE.MeshStandardMaterial({
      color: 0xCBD5E1,
      roughness: 0.18,
      metalness: 0.92,
    });

    // Crystalline Translucent Bio-PCM Ice-Blue Packs with Inner Glow
    const matPCM = new THREE.MeshPhysicalMaterial({
      color: 0x38BDF8,
      emissive: 0x0284C7,
      emissiveIntensity: 0.35,
      roughness: 0.12,
      metalness: 0.05,
      transmission: 0.85,
      thickness: 1.1,
      transparent: true,
      opacity: 0.92,
    });

    // Pure Electrolytic Copper (Peltier base & heat pipes)
    const matCopper = new THREE.MeshStandardMaterial({
      color: 0xEA580C,
      roughness: 0.22,
      metalness: 0.94,
    });

    // Peltier Semiconductor Ceramic Substrate
    const matCeramicWhite = new THREE.MeshStandardMaterial({
      color: 0xF8FAFC,
      roughness: 0.25,
      metalness: 0.1,
    });

    // Clear Vaccine Glass Vials
    const matGlass = new THREE.MeshPhysicalMaterial({
      color: 0xFFFFFF,
      roughness: 0.05,
      metalness: 0.05,
      transmission: 0.96,
      thickness: 0.3,
      transparent: true,
      opacity: 0.94,
    });

    // Blue Vaccine Liquid Inside Vials
    const matVaccine = new THREE.MeshStandardMaterial({
      color: 0x0284C7,
      emissive: 0x0369A1,
      emissiveIntensity: 0.4,
      roughness: 0.2,
    });

    // Deep Blue Rubber Stopper
    const matVialCap = new THREE.MeshStandardMaterial({
      color: 0x1E3A8A,
      roughness: 0.4,
    });

    // Acrylic Fluid Chamber
    const matLiquidChamber = new THREE.MeshPhysicalMaterial({
      color: 0xE0F2FE,
      roughness: 0.08,
      metalness: 0.05,
      transmission: 0.94,
      thickness: 0.4,
      transparent: true,
      opacity: 0.88,
    });

    // Glowing Coolant Liquid
    const matCoolantFluid = new THREE.MeshStandardMaterial({
      color: 0x06B6D4,
      emissive: 0x0891B2,
      emissiveIntensity: 0.65,
    });

    // Bright Blue Silicone Flexible Fluid Tubing
    const matBlueTube = new THREE.MeshStandardMaterial({
      color: 0x0284C7,
      roughness: 0.25,
      transparent: true,
      opacity: 0.92,
    });

    // Matte Dark Fan Shroud
    const matFanShroud = new THREE.MeshStandardMaterial({
      color: 0x0F172A,
      roughness: 0.55,
      metalness: 0.25,
    });

    // Green Circuit Board PCB
    const matPCB = new THREE.MeshStandardMaterial({
      color: 0x15803D,
      roughness: 0.5,
      metalness: 0.3,
    });

    // Blue Illuminated LCD Display
    const matLCD = new THREE.MeshStandardMaterial({
      color: 0x0369A1,
      emissive: 0x0284C7,
      emissiveIntensity: 0.95,
    });

    const partsMap: { [id: number]: THREE.Object3D } = {};
    const rootAssembly = new THREE.Group();
    scene.add(rootAssembly);

    // -----------------------------------------------------------
    // 4. ASSEMBLY GEOMETRY WITH EXPLODED PIVOTS
    // -----------------------------------------------------------
    
    // A. Main Outer Cooler Enclosure (Component 1)
    const enclosureGroup = new THREE.Group();

    // Back Wall
    const backWall = new THREE.Mesh(new THREE.BoxGeometry(4.5, 3.2, 0.12), matCoolerBody);
    backWall.position.set(0, 0, -1.44);
    backWall.castShadow = true;
    enclosureGroup.add(backWall);

    // Bottom Wall
    const bottomWall = new THREE.Mesh(new THREE.BoxGeometry(4.5, 0.14, 3.0), matCoolerBody);
    bottomWall.position.set(0, -1.53, 0);
    bottomWall.castShadow = true;
    enclosureGroup.add(bottomWall);

    // Left Wall
    const leftWall = new THREE.Mesh(new THREE.BoxGeometry(0.14, 3.2, 3.0), matCoolerBody);
    leftWall.position.set(-2.18, 0, 0);
    leftWall.castShadow = true;
    enclosureGroup.add(leftWall);

    // Left Handle
    const handleCupLeft = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.5, 0.8), matBlueTrim);
    handleCupLeft.position.set(-2.23, 0.45, 0);
    enclosureGroup.add(handleCupLeft);

    // Right Wall
    const rightWall = new THREE.Mesh(new THREE.BoxGeometry(0.14, 3.2, 3.0), matCoolerBody);
    rightWall.position.set(2.18, 0, 0);
    rightWall.castShadow = true;
    enclosureGroup.add(rightWall);

    // Right Handle
    const handleCupRight = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.5, 0.8), matBlueTrim);
    handleCupRight.position.set(2.23, 0.45, 0);
    enclosureGroup.add(handleCupRight);

    // Front Wall (Removable on Cutaway)
    const frontWall = new THREE.Mesh(new THREE.BoxGeometry(4.5, 3.2, 0.12), matCoolerBody);
    frontWall.position.set(0, 0, 1.44);
    frontWall.castShadow = true;
    frontWall.visible = false;
    enclosureGroup.add(frontWall);

    // Latches
    const latchGeo = new THREE.BoxGeometry(0.24, 0.42, 0.08);
    const latch1 = new THREE.Mesh(latchGeo, matBlueTrim);
    latch1.position.set(-1.1, 1.0, 1.52);
    frontWall.add(latch1);

    const latch2 = new THREE.Mesh(latchGeo, matBlueTrim);
    latch2.position.set(1.1, 1.0, 1.52);
    frontWall.add(latch2);

    // Cutaway Rims
    const frontCutawayRims = new THREE.Group();
    const cutRimL = new THREE.Mesh(new THREE.BoxGeometry(0.16, 3.16, 0.08), matPUFoam);
    cutRimL.position.set(-2.17, 0, 1.46);
    frontCutawayRims.add(cutRimL);

    const cutRimR = new THREE.Mesh(new THREE.BoxGeometry(0.16, 3.16, 0.08), matPUFoam);
    cutRimR.position.set(2.17, 0, 1.46);
    frontCutawayRims.add(cutRimR);

    const cutRimB = new THREE.Mesh(new THREE.BoxGeometry(4.34, 0.16, 0.08), matPUFoam);
    cutRimB.position.set(0, -1.52, 1.46);
    frontCutawayRims.add(cutRimB);
    enclosureGroup.add(frontCutawayRims);

    // Corner Protectors
    const cornerGeo = new THREE.BoxGeometry(0.42, 0.42, 0.42);
    [[-2.16, -1.48, -1.39], [2.16, -1.48, -1.39], [-2.16, -1.48, 1.39], [2.16, -1.48, 1.39]].forEach(([cx, cy, cz]) => {
      const cMesh = new THREE.Mesh(cornerGeo, matBlueTrim);
      cMesh.position.set(cx, cy, cz);
      enclosureGroup.add(cMesh);
    });

    partsMap[1] = enclosureGroup;
    rootAssembly.add(enclosureGroup);

    // B. Horizontal Dividing Shelf
    const shelfMesh = new THREE.Mesh(new THREE.BoxGeometry(4.22, 0.08, 2.76), matAluminium);
    shelfMesh.position.set(0, 0.06, 0);
    shelfMesh.castShadow = true;
    rootAssembly.add(shelfMesh);

    // C. Upper Deck: Bio-PCM Packs (Component 2)
    const pcmGroup = new THREE.Group();
    const pcmGeo = new THREE.BoxGeometry(0.38, 1.45, 1.95);

    const pcmL1 = new THREE.Mesh(pcmGeo, matPCM);
    pcmL1.position.set(-1.72, 0.85, 0);
    pcmGroup.add(pcmL1);

    const pcmL2 = new THREE.Mesh(pcmGeo, matPCM);
    pcmL2.position.set(-1.28, 0.85, 0);
    pcmGroup.add(pcmL2);

    const pcmR1 = new THREE.Mesh(pcmGeo, matPCM);
    pcmR1.position.set(1.48, 0.85, 0);
    pcmGroup.add(pcmR1);

    const pcmR2 = new THREE.Mesh(pcmGeo, matPCM);
    pcmR2.position.set(1.92, 0.85, 0);
    pcmGroup.add(pcmR2);

    partsMap[2] = pcmGroup;
    rootAssembly.add(pcmGroup);

    // D. Upper Deck: Aluminium Heat Spreader Jacket (Component 7)
    const alSpreaderGroup = new THREE.Group();
    const alSpreaderBase = new THREE.Mesh(new THREE.BoxGeometry(2.18, 0.08, 2.05), matAluminium);
    alSpreaderBase.position.set(0.1, 0.12, 0);
    alSpreaderGroup.add(alSpreaderBase);

    const alSpreaderL = new THREE.Mesh(new THREE.BoxGeometry(0.08, 1.4, 2.05), matAluminium);
    alSpreaderL.position.set(-0.95, 0.82, 0);
    alSpreaderGroup.add(alSpreaderL);

    const alSpreaderR = new THREE.Mesh(new THREE.BoxGeometry(0.08, 1.4, 2.05), matAluminium);
    alSpreaderR.position.set(1.15, 0.82, 0);
    alSpreaderGroup.add(alSpreaderR);

    const alSpreaderB = new THREE.Mesh(new THREE.BoxGeometry(2.18, 1.4, 0.08), matAluminium);
    alSpreaderB.position.set(0.1, 0.82, -1.0);
    alSpreaderGroup.add(alSpreaderB);

    partsMap[7] = alSpreaderGroup;
    rootAssembly.add(alSpreaderGroup);

    // E. Upper Deck: Medical Payload Chamber & Vaccine Vials (Component 3)
    const payloadGroup = new THREE.Group();
    const trayMesh = new THREE.Mesh(
      new THREE.BoxGeometry(1.98, 0.16, 1.88),
      new THREE.MeshStandardMaterial({ color: 0xF8FAFC, roughness: 0.3 })
    );
    trayMesh.position.set(0.1, 0.22, 0);
    payloadGroup.add(trayMesh);

    const vialGeo = new THREE.CylinderGeometry(0.09, 0.09, 0.42, 16);
    const liqGeo = new THREE.CylinderGeometry(0.084, 0.084, 0.28, 16);
    const capGeo = new THREE.CylinderGeometry(0.095, 0.095, 0.07, 16);

    for (let x = -0.65; x <= 0.85; x += 0.25) {
      for (let z of [-0.4, 0.4]) {
        const vMesh = new THREE.Mesh(vialGeo, matGlass);
        vMesh.position.set(x, 0.52, z);
        const lMesh = new THREE.Mesh(liqGeo, matVaccine);
        lMesh.position.set(x, 0.46, z);
        const cMesh = new THREE.Mesh(capGeo, matVialCap);
        cMesh.position.set(x, 0.74, z);

        payloadGroup.add(vMesh);
        payloadGroup.add(lMesh);
        payloadGroup.add(cMesh);
      }
    }

    partsMap[3] = payloadGroup;
    rootAssembly.add(payloadGroup);

    // F. Upper Deck: Digital Sensor Probe (Component 4)
    const sensorGroup = new THREE.Group();
    const probeMesh = new THREE.Mesh(
      new THREE.CylinderGeometry(0.045, 0.045, 0.35, 12),
      new THREE.MeshStandardMaterial({ color: 0x0F172A, metalness: 0.8, roughness: 0.2 })
    );
    probeMesh.position.set(1.18, 1.1, 0.4);
    sensorGroup.add(probeMesh);

    const wireMat = new THREE.LineBasicMaterial({ color: 0x14B8A6, linewidth: 2 });
    const wireGeo = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(1.18, 1.0, 0.4),
      new THREE.Vector3(1.18, 0.1, 0.4),
      new THREE.Vector3(0.6, -0.6, 0.5),
      new THREE.Vector3(-0.6, -1.2, 0.6)
    ]);
    const wireLine = new THREE.Line(wireGeo, wireMat);
    sensorGroup.add(wireLine);

    partsMap[4] = sensorGroup;
    rootAssembly.add(sensorGroup);

    // G. Lower Deck: Peltier Thermoelectric Stack (Component 5, 6, 8, 9)
    const peltierStackGroup = new THREE.Group();
    peltierStackGroup.position.set(-0.6, -0.42, 0.1);

    const peltierTopAl = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.12, 1.2), matAluminium);
    peltierTopAl.position.set(0, 0.28, 0);
    peltierStackGroup.add(peltierTopAl);

    const ceramicUpper = new THREE.Mesh(new THREE.BoxGeometry(1.25, 0.06, 1.05), matCeramicWhite);
    ceramicUpper.position.set(0, 0.19, 0);
    peltierStackGroup.add(ceramicUpper);

    const semiconductorCore = new THREE.Mesh(new THREE.BoxGeometry(1.18, 0.10, 0.98), matCopper);
    semiconductorCore.position.set(0, 0.11, 0);
    peltierStackGroup.add(semiconductorCore);

    const ceramicLower = new THREE.Mesh(new THREE.BoxGeometry(1.25, 0.06, 1.05), matCeramicWhite);
    ceramicLower.position.set(0, 0.03, 0);
    peltierStackGroup.add(ceramicLower);

    const peltierExchanger = new THREE.Mesh(new THREE.BoxGeometry(1.45, 0.18, 1.25), matAluminium);
    peltierExchanger.position.set(0, -0.09, 0);
    peltierStackGroup.add(peltierExchanger);

    partsMap[5] = peltierStackGroup;
    partsMap[6] = semiconductorCore;
    partsMap[8] = peltierTopAl;
    partsMap[9] = peltierExchanger;
    rootAssembly.add(peltierStackGroup);

    // H. Lower Deck: Liquid Reservoir
    const liquidChamberGroup = new THREE.Group();
    liquidChamberGroup.position.set(0.32, -0.72, 0.35);

    const acrylicBottle = new THREE.Mesh(new THREE.BoxGeometry(0.52, 0.95, 0.52), matLiquidChamber);
    liquidChamberGroup.add(acrylicBottle);

    const liquidMesh = new THREE.Mesh(new THREE.BoxGeometry(0.46, 0.85, 0.46), matCoolantFluid);
    liquidChamberGroup.add(liquidMesh);

    const capMesh = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 0.1, 16), matBlueTrim);
    capMesh.position.set(0, 0.52, 0);
    liquidChamberGroup.add(capMesh);

    rootAssembly.add(liquidChamberGroup);

    // Tubes
    const tube1 = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.045, 0.95, 12), matBlueTube);
    tube1.rotation.z = Math.PI / 2;
    tube1.position.set(-0.15, -0.24, 0.35);
    rootAssembly.add(tube1);

    const tube2 = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.045, 0.85, 12), matBlueTube);
    tube2.rotation.z = Math.PI / 2;
    tube2.position.set(0.82, -0.24, 0.35);
    rootAssembly.add(tube2);

    // I. Lower Deck: Heat Sink Fan Assembly (Component 10, 11)
    const heatSinkFanGroup = new THREE.Group();
    heatSinkFanGroup.position.set(1.42, -0.65, 0.25);

    const finArrayGroup = new THREE.Group();
    finArrayGroup.position.set(0, 0, -0.32);
    for (let fy = -0.48; fy <= 0.48; fy += 0.065) {
      const fin = new THREE.Mesh(new THREE.BoxGeometry(1.05, 0.016, 0.72), matAluminium);
      fin.position.set(0, fy, 0);
      finArrayGroup.add(fin);
    }
    heatSinkFanGroup.add(finArrayGroup);
    partsMap[10] = finArrayGroup;

    // Copper Heat Pipes
    for (let py of [-0.25, 0.25]) {
      const hPipe = new THREE.Mesh(new THREE.CylinderGeometry(0.038, 0.038, 1.15, 12), matCopper);
      hPipe.rotation.z = Math.PI / 2;
      hPipe.position.set(0, py, -0.32);
      heatSinkFanGroup.add(hPipe);
    }

    const fanShroud = new THREE.Mesh(new THREE.BoxGeometry(1.15, 1.15, 0.28), matFanShroud);
    fanShroud.position.set(0, 0, 0.14);
    heatSinkFanGroup.add(fanShroud);

    const fanBlades = new THREE.Group();
    fanBlades.position.set(0, 0, 0.15);
    const fanHub = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.14, 0.12, 16), matFanShroud);
    fanHub.rotation.x = Math.PI / 2;
    fanBlades.add(fanHub);

    for (let b = 0; b < 7; b++) {
      const blade = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.36, 0.12), matFanShroud);
      blade.rotation.z = (b * Math.PI * 2) / 7;
      blade.position.set(Math.cos((b * Math.PI * 2) / 7) * 0.24, Math.sin((b * Math.PI * 2) / 7) * 0.24, 0);
      fanBlades.add(blade);
    }
    heatSinkFanGroup.add(fanBlades);

    partsMap[11] = heatSinkFanGroup;
    rootAssembly.add(heatSinkFanGroup);

    // J. Control Board (Component 12)
    const ctrlUnitGroup = new THREE.Group();
    ctrlUnitGroup.position.set(-0.85, -1.22, 0.45);

    const pcbBoard = new THREE.Mesh(new THREE.BoxGeometry(1.42, 0.08, 0.95), matPCB);
    ctrlUnitGroup.add(pcbBoard);

    const lcdScreen = new THREE.Mesh(new THREE.BoxGeometry(0.72, 0.08, 0.36), matLCD);
    lcdScreen.position.set(0.05, 0.08, 0);
    ctrlUnitGroup.add(lcdScreen);

    partsMap[12] = ctrlUnitGroup;
    rootAssembly.add(ctrlUnitGroup);

    // K. Insulated Lid
    const lidPivot = new THREE.Group();
    lidPivot.position.set(0, 1.6, -1.48);

    const lidSlab = new THREE.Mesh(new THREE.BoxGeometry(4.54, 0.34, 3.04), matCoolerBody);
    lidSlab.position.set(0, 0.17, 1.52);
    lidPivot.add(lidSlab);

    [[-2.18, 0.17, 0.06], [2.18, 0.17, 0.06], [-2.18, 0.17, 2.98], [2.18, 0.17, 2.98]].forEach(([lx, ly, lz]) => {
      const lc = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.36, 0.42), matBlueTrim);
      lc.position.set(lx, ly, lz);
      lidPivot.add(lc);
    });

    const lidPUFPlug = new THREE.Mesh(new THREE.BoxGeometry(4.15, 0.22, 2.65), matPUFoam);
    lidPUFPlug.position.set(0, -0.08, 1.52);
    lidPivot.add(lidPUFPlug);

    lidPivot.rotation.x = -1.15;
    rootAssembly.add(lidPivot);

    // -----------------------------------------------------------
    // 5. AIRFLOW & PARTICLES
    // -----------------------------------------------------------
    const intakeLineCoords: number[] = [];
    for (let i = 0; i < 35; i++) {
      intakeLineCoords.push(
        0.8 + (Math.random() - 0.5) * 0.8, -0.65 + (Math.random() - 0.5) * 0.8, 1.4 + Math.random() * 1.5,
        1.42, -0.65, 0.35
      );
    }
    const intakeGeo = new THREE.BufferGeometry();
    intakeGeo.setAttribute('position', new THREE.Float32BufferAttribute(intakeLineCoords, 3));
    const airflowIntakeLines = new THREE.LineSegments(
      intakeGeo,
      new THREE.LineBasicMaterial({ color: 0x38BDF8, transparent: true, opacity: 0.75, linewidth: 1.5 })
    );
    scene.add(airflowIntakeLines);

    // Exhaust Plume (Vivid Amber-Orange)
    const exhaustCount = 450;
    const exhaustGeo = new THREE.BufferGeometry();
    const exhaustPos = new Float32Array(exhaustCount * 3);
    for (let i = 0; i < exhaustCount; i++) {
      exhaustPos[i * 3 + 0] = 2.2 + Math.random() * 2.5;
      exhaustPos[i * 3 + 1] = -0.65 + (Math.random() - 0.5) * 1.2;
      exhaustPos[i * 3 + 2] = 0.25 + (Math.random() - 0.5) * 1.2;
    }
    exhaustGeo.setAttribute('position', new THREE.BufferAttribute(exhaustPos, 3));
    const airflowExhaustParticles = new THREE.Points(
      exhaustGeo,
      new THREE.PointsMaterial({ color: 0xF59E0B, size: 0.09, transparent: true, opacity: 0.9 })
    );
    scene.add(airflowExhaustParticles);

    // Cold Flow Particles (Cyan Extraction)
    const coldCount = 250;
    const geoCold = new THREE.BufferGeometry();
    const posCold = new Float32Array(coldCount * 3);
    for (let i = 0; i < coldCount; i++) {
      posCold[i * 3 + 0] = 0.1 + (Math.random() - 0.5) * 1.8;
      posCold[i * 3 + 1] = 0.8 + (Math.random() - 0.5) * 1.2;
      posCold[i * 3 + 2] = (Math.random() - 0.5) * 1.6;
    }
    geoCold.setAttribute('position', new THREE.BufferAttribute(posCold, 3));
    const flowParticlesCold = new THREE.Points(
      geoCold,
      new THREE.PointsMaterial({ color: 0x38BDF8, size: 0.075, transparent: true, opacity: 0.85 })
    );
    scene.add(flowParticlesCold);

    // Fluid Particles
    const fluidCount = 140;
    const geoFluid = new THREE.BufferGeometry();
    const posFluid = new Float32Array(fluidCount * 3);
    for (let i = 0; i < fluidCount; i++) {
      const t = i / fluidCount;
      posFluid[i * 3 + 0] = -0.6 + t * 2.0;
      posFluid[i * 3 + 1] = -0.24 + Math.sin(t * Math.PI * 4) * 0.05;
      posFluid[i * 3 + 2] = 0.35;
    }
    geoFluid.setAttribute('position', new THREE.BufferAttribute(posFluid, 3));
    const flowParticlesFluid = new THREE.Points(
      geoFluid,
      new THREE.PointsMaterial({ color: 0x06B6D4, size: 0.07, transparent: true, opacity: 0.95 })
    );
    scene.add(flowParticlesFluid);

    // -----------------------------------------------------------
    // 6. CAMERA & MOUSE CONTROLS
    // -----------------------------------------------------------
    const spherical = {
      radius: isSlideMode ? 10.2 : 11.2,
      theta: 0.85,
      phi: 1.15
    };
    const orbitTarget = new THREE.Vector3(0.0, 0.1, 0.0);

    const updateCameraPos = () => {
      camera.position.x = orbitTarget.x + spherical.radius * Math.sin(spherical.phi) * Math.sin(spherical.theta);
      camera.position.y = orbitTarget.y + spherical.radius * Math.cos(spherical.phi);
      camera.position.z = orbitTarget.z + spherical.radius * Math.sin(spherical.phi) * Math.cos(spherical.theta);
      camera.lookAt(orbitTarget);
    };
    updateCameraPos();

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
      spherical.phi = Math.max(0.15, Math.min(Math.PI / 2 + 0.25, spherical.phi - deltaY * 0.007));
      updateCameraPos();
    };

    const onMouseUp = () => { isDragging = false; };

    const onWheel = (e: WheelEvent) => {
      e.preventDefault();
      spherical.radius = Math.max(4.5, Math.min(18.0, spherical.radius + e.deltaY * 0.012));
      updateCameraPos();
    };

    dom.addEventListener('mousedown', onMouseDown);
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
    dom.addEventListener('wheel', onWheel, { passive: false });

    // Touch Support
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
      spherical.phi = Math.max(0.15, Math.min(Math.PI / 2 + 0.25, spherical.phi - deltaY * 0.007));
      updateCameraPos();
    };
    const onTouchEnd = () => { isDragging = false; };

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
      lidPivot,
      frontWall,
      frontCutawayRims,
      pcmGroup,
      payloadGroup,
      peltierStackGroup,
      heatSinkFanGroup,
      liquidChamberGroup,
      ctrlUnitGroup,
      airflowExhaustParticles,
      airflowIntakeLines,
      flowParticlesCold,
      flowParticlesFluid,
      fanBlades,
      orbitTarget,
      isDragging,
      prevMouseX,
      prevMouseY,
      spherical,
      currentExplode: 0,
      targetExplode: 0
    };

    // 7. Render Loop with Smooth Exploded View Lerping
    let animFrameId: number;
    const startTime = performance.now();

    const animate = () => {
      animFrameId = requestAnimationFrame(animate);
      const elapsedTime = (performance.now() - startTime) * 0.001;

      // Spin Fan Blades
      fanBlades.rotation.z += 0.32;

      // Smooth Exploded View Interpolation
      if (threeState.current) {
        const ts = threeState.current;
        ts.currentExplode += (ts.targetExplode - ts.currentExplode) * 0.08;
        const ex = ts.currentExplode; // 0 to 1

        // Explode Subsystems
        lidPivot.position.y = 1.6 + ex * 2.4;
        payloadGroup.position.y = ex * 1.5;
        pcmGroup.position.z = ex * 0.8;
        peltierStackGroup.position.y = -0.42 - ex * 1.6;
        heatSinkFanGroup.position.x = 1.42 + ex * 2.0;
        liquidChamberGroup.position.z = 0.35 + ex * 1.2;
        ctrlUnitGroup.position.y = -1.22 - ex * 1.0;
      }

      // Exhaust Particles Animation
      const hPos = airflowExhaustParticles.geometry.attributes.position.array as Float32Array;
      for (let i = 0; i < exhaustCount; i++) {
        hPos[i * 3 + 0] += 0.048;
        hPos[i * 3 + 1] += Math.sin(elapsedTime * 3 + i) * 0.004;
        if (hPos[i * 3 + 0] > 5.5) {
          hPos[i * 3 + 0] = 2.2;
        }
      }
      airflowExhaustParticles.geometry.attributes.position.needsUpdate = true;

      // Cold Flow Particles
      const cPos = flowParticlesCold.geometry.attributes.position.array as Float32Array;
      for (let i = 0; i < coldCount; i++) {
        cPos[i * 3 + 1] -= 0.012;
        if (cPos[i * 3 + 1] < 0.12) {
          cPos[i * 3 + 1] = 1.4;
        }
      }
      flowParticlesCold.geometry.attributes.position.needsUpdate = true;

      // Fluid Loop Particles
      const fPos = flowParticlesFluid.geometry.attributes.position.array as Float32Array;
      for (let i = 0; i < fluidCount; i++) {
        fPos[i * 3 + 0] += 0.024;
        if (fPos[i * 3 + 0] > 1.4) {
          fPos[i * 3 + 0] = -0.6;
        }
      }
      flowParticlesFluid.geometry.attributes.position.needsUpdate = true;

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
    const { frontWall, frontCutawayRims, lidPivot } = threeState.current;
    frontWall.visible = !isCutaway;
    frontCutawayRims.visible = isCutaway;
    lidPivot.rotation.x = isLidOpen ? -1.15 : 0;
  }, [isCutaway, isLidOpen]);

  // Update Exploded Slider Value
  useEffect(() => {
    if (threeState.current) {
      threeState.current.targetExplode = explodedPercent / 100;
    }
  }, [explodedPercent]);

  // Toggle Visibility of Airflow and Thermal Vectors
  useEffect(() => {
    if (!threeState.current) return;
    const { airflowIntakeLines, airflowExhaustParticles, flowParticlesCold, flowParticlesFluid } = threeState.current;
    airflowIntakeLines.visible = showAirflow;
    airflowExhaustParticles.visible = showAirflow;
    flowParticlesCold.visible = showThermalFlow;
    flowParticlesFluid.visible = showThermalFlow;
  }, [showAirflow, showThermalFlow]);

  const selectComponent = (comp: ComponentSpec) => {
    setSelectedComp(comp);
    sound.click();
    if (onSelectComponent) onSelectComponent(comp);

    if (threeState.current) {
      const { spherical } = threeState.current;
      if (comp.id === 2 || comp.id === 3) {
        spherical.theta = 0.85;
        spherical.phi = 0.95;
        spherical.radius = isSlideMode ? 8.2 : 9.0;
      } else if (comp.id === 5 || comp.id === 6 || comp.id === 8 || comp.id === 9) {
        spherical.theta = 1.05;
        spherical.phi = 1.25;
        spherical.radius = isSlideMode ? 7.5 : 8.2;
      } else if (comp.id === 10 || comp.id === 11) {
        spherical.theta = 0.45;
        spherical.phi = 1.25;
        spherical.radius = isSlideMode ? 7.8 : 8.5;
      } else if (comp.id === 12) {
        spherical.theta = 1.15;
        spherical.phi = 1.35;
        spherical.radius = isSlideMode ? 7.5 : 8.2;
      } else {
        spherical.theta = 0.85;
        spherical.phi = 1.15;
        spherical.radius = isSlideMode ? 10.2 : 11.2;
      }
    }
  };

  const resetCamera = () => {
    sound.click();
    if (threeState.current) {
      threeState.current.spherical.radius = isSlideMode ? 10.2 : 11.2;
      threeState.current.spherical.theta = 0.85;
      threeState.current.spherical.phi = 1.15;
    }
    setExplodedPercent(0);
  };

  const filteredComponents = COMPONENTS_3D.filter(c => 
    activeFilter === 'all' ? true : c.category === activeFilter
  );

  return (
    <div className={`relative w-full rounded-2xl overflow-hidden bg-[#060B14] border border-slate-800 shadow-2xl flex flex-col lg:flex-row select-none ${
      isSlideMode ? 'h-[540px]' : 'h-[750px]'
    }`}>
      
      {/* 3D Canvas Area */}
      <div className="flex-1 relative h-[380px] lg:h-full bg-gradient-to-b from-[#060B14] via-[#091222] to-[#040810] overflow-hidden select-none">
        
        {/* Three.js Canvas Mount */}
        <div ref={mountRef} className="w-full h-full cursor-grab active:cursor-grabbing" />

        {/* Top-Left Mode & Dimensions Badge */}
        <div className="absolute top-3.5 left-3.5 z-10 flex flex-wrap items-center gap-2 pointer-events-none">
          <span className="px-3 py-1 rounded-xl text-[10px] font-mono uppercase bg-slate-900/90 text-teal-300 border border-teal-500/30 font-bold shadow-lg backdrop-blur-md flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
            3D DIGITAL TWIN & EXPLODED SYSTEM
          </span>
          <span className="px-2.5 py-1 rounded-xl text-[10px] font-mono text-slate-400 bg-slate-900/80 border border-slate-800 font-semibold shadow-md backdrop-blur-md">
            450 × 300 × 320 mm • 5.2 kg
          </span>
        </div>

        {/* Interactive Overlay Action Bar */}
        <div className="absolute top-3.5 right-3.5 z-10 flex flex-wrap items-center gap-1.5 bg-slate-900/90 border border-slate-700/80 p-1.5 rounded-xl shadow-xl backdrop-blur-md">
          
          {/* Exploded View Slider */}
          <div className="flex items-center gap-2 px-2 py-1 bg-slate-950/70 rounded-lg border border-slate-800">
            <Layers className="w-3.5 h-3.5 text-teal-400" />
            <span className="text-[10px] font-mono text-slate-300 font-bold hidden sm:inline">EXPLODED:</span>
            <input 
              type="range" 
              min="0" 
              max="100" 
              value={explodedPercent}
              onChange={(e) => setExplodedPercent(Number(e.target.value))}
              className="w-16 sm:w-24 accent-teal-400 cursor-pointer"
            />
            <span className="font-mono text-[10px] text-teal-300 font-bold w-7 text-right">
              {explodedPercent}%
            </span>
          </div>

          {/* Toggle Cutaway View */}
          <button
            onClick={() => { setIsCutaway(!isCutaway); sound.click(); }}
            className={`px-2.5 py-1 text-xs font-mono rounded-lg transition-all flex items-center gap-1.5 cursor-pointer ${
              isCutaway 
                ? 'bg-teal-600 text-white font-bold shadow-md shadow-teal-900/50' 
                : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
            title="Toggle Front Cutaway Section"
          >
            <Eye className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Cutaway</span>
          </button>

          {/* Toggle Insulated Lid */}
          <button
            onClick={() => { setIsLidOpen(!isLidOpen); sound.click(); }}
            className={`px-2.5 py-1 text-xs font-mono rounded-lg transition-all flex items-center gap-1.5 cursor-pointer ${
              isLidOpen 
                ? 'bg-teal-600 text-white font-bold shadow-md shadow-teal-900/50' 
                : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
            title="Open / Close Insulated Lid"
          >
            <Maximize2 className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">{isLidOpen ? 'Close Lid' : 'Open Lid'}</span>
          </button>

          {/* Toggle Airflow */}
          <button
            onClick={() => { setShowAirflow(!showAirflow); sound.click(); }}
            className={`p-1.5 rounded-lg border transition-all cursor-pointer ${
              showAirflow 
                ? 'bg-amber-950/80 border-amber-500/50 text-amber-400 shadow-md' 
                : 'bg-slate-800 border-slate-700 text-slate-500 hover:text-slate-300'
            }`}
            title="Toggle Forced Airflow Streamlines"
          >
            <Wind className="w-3.5 h-3.5" />
          </button>

          {/* Toggle Thermal Transport */}
          <button
            onClick={() => { setShowThermalFlow(!showThermalFlow); sound.click(); }}
            className={`p-1.5 rounded-lg border transition-all cursor-pointer ${
              showThermalFlow 
                ? 'bg-sky-950/80 border-sky-500/50 text-sky-400 shadow-md' 
                : 'bg-slate-800 border-slate-700 text-slate-500 hover:text-slate-300'
            }`}
            title="Toggle Thermal Fluid Loop & Cold Extraction"
          >
            <Snowflake className="w-3.5 h-3.5" />
          </button>

          {/* Reset Camera Orbit */}
          <button
            onClick={resetCamera}
            className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors cursor-pointer"
            title="Reset Camera View & Assembly"
          >
            <RotateCcw className="w-3.5 h-3.5" />
          </button>

        </div>

        {/* Bottom Legend & First Law Statement */}
        <div className="absolute bottom-3 left-3 right-3 z-10 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 pointer-events-none">
          <div className="flex flex-wrap items-center gap-2 pointer-events-auto">
            <span className="flex items-center gap-1.5 text-[10px] font-mono font-bold bg-slate-900/90 border border-slate-800 text-teal-300 px-2.5 py-1 rounded-lg shadow-md backdrop-blur-md">
              <span className="w-2 h-2 rounded-full bg-[#38BDF8] animate-pulse"></span>
              Cold Zone: 4.8kg Bio-PCM (+5.0°C)
            </span>
            <span className="flex items-center gap-1.5 text-[10px] font-mono font-bold bg-slate-900/90 border border-slate-800 text-amber-300 px-2.5 py-1 rounded-lg shadow-md backdrop-blur-md">
              <span className="w-2 h-2 rounded-full bg-[#F59E0B] animate-pulse"></span>
              Hot Zone: 48.5 W Forced Heat Dissipation
            </span>
            <span className="flex items-center gap-1.5 text-[10px] font-mono font-bold bg-slate-900/90 border border-slate-800 text-cyan-300 px-2.5 py-1 rounded-lg shadow-md backdrop-blur-md">
              <span className="w-2 h-2 rounded-full bg-[#06B6D4]"></span>
              Liquid Loop Transfer
            </span>
          </div>

          <div className="hidden md:block pointer-events-auto bg-slate-900/90 border border-amber-500/30 rounded-xl p-2.5 px-3.5 shadow-xl max-w-sm backdrop-blur-md">
            <div className="flex items-center gap-1.5 text-[10px] font-mono font-bold text-amber-400">
              <Flame className="w-3.5 h-3.5 text-amber-500" />
              FIRST LAW THERMODYNAMICS
            </div>
            <p className="text-[10px] text-slate-300 leading-tight mt-0.5">
              Thermoelectric heat pump obeys energy conservation:
            </p>
            <div className="font-mono text-[9px] text-amber-300 font-bold mt-0.5">
              Q̇_hot = Q̇_cold + P_elec = 18.5W + 30.0W = 48.5 W
            </div>
          </div>
        </div>
      </div>

      {/* Right Sidebar: Subsystem Inspector */}
      <div className="w-full lg:w-[380px] h-[340px] lg:h-full bg-[#08101E] border-t lg:border-t-0 lg:border-l border-slate-800 flex flex-col">
        
        {/* Header & Category Filters */}
        <div className="p-3.5 border-b border-slate-800 bg-slate-900/90 backdrop-blur-md">
          <div className="flex items-center justify-between mb-2">
            <h3 className="font-serif-display text-base font-bold text-white flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-teal-400" />
              Subsystem Inspector
            </h3>
            <span className="text-[10px] font-mono text-teal-400 bg-teal-950/80 px-2.5 py-0.5 rounded-full border border-teal-500/40 font-bold">
              13 Subsystems
            </span>
          </div>

          <div className="flex flex-wrap gap-1">
            {(['all', 'thermal', 'mechanical', 'electrical', 'sensing'] as const).map(cat => (
              <button
                key={cat}
                onClick={() => { setActiveFilter(cat); sound.click(); }}
                className={`px-2 py-0.5 text-[10px] font-mono uppercase rounded-md transition-colors cursor-pointer ${
                  activeFilter === cat 
                    ? 'bg-teal-600 text-white font-bold shadow-md shadow-teal-950/50' 
                    : 'bg-slate-800/80 text-slate-400 hover:bg-slate-700 hover:text-slate-200'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        {/* Selected Component Telemetry Details */}
        <div className="p-3.5 border-b border-slate-800 bg-[#0A1324]">
          <div className="flex items-start justify-between">
            <div>
              <span className="text-[9px] font-mono text-teal-400 uppercase tracking-widest block font-bold">
                ID #{selectedComp.id.toString().padStart(2, '0')} • {selectedComp.category}
              </span>
              <h4 className="font-bold text-white text-sm mt-0.5">
                {selectedComp.name}
              </h4>
            </div>
            <span className={`text-[9px] font-mono font-bold px-2 py-0.5 rounded-full border ${
              selectedComp.heatFluxRole === 'cold' ? 'bg-sky-950/80 text-sky-300 border-sky-500/40' :
              selectedComp.heatFluxRole === 'hot' ? 'bg-amber-950/80 text-amber-300 border-amber-500/40' :
              selectedComp.heatFluxRole === 'passive' ? 'bg-emerald-950/80 text-emerald-300 border-emerald-500/40' :
              'bg-purple-950/80 text-purple-300 border-purple-500/40'
            }`}>
              {selectedComp.heatFluxRole.toUpperCase()}
            </span>
          </div>

          <div className="mt-2 space-y-1.5 text-xs">
            <div>
              <span className="text-slate-400 font-mono text-[9px] block">Role:</span>
              <p className="text-slate-200 text-[11px] leading-tight">{selectedComp.role}</p>
            </div>
            <div>
              <span className="text-slate-400 font-mono text-[9px] block">Scientific Principle:</span>
              <p className="text-teal-300/90 text-[11px] italic leading-tight">{selectedComp.principle}</p>
            </div>
            <div className="bg-slate-900/90 p-2 rounded-lg border border-slate-800">
              <span className="text-teal-400 font-mono text-[9px] block font-bold">Hardware Specification:</span>
              <p className="text-slate-100 font-mono text-[10px] mt-0.5 leading-snug">{selectedComp.specs}</p>
            </div>
            <p className="text-slate-400 text-[10px] leading-relaxed pt-0.5 line-clamp-2">
              {selectedComp.details}
            </p>
          </div>
        </div>

        {/* Scrollable Subsystems List */}
        <div className="flex-1 overflow-y-auto p-1.5 space-y-1 divide-y divide-slate-800/40">
          {filteredComponents.map(c => (
            <button
              key={c.id}
              onClick={() => selectComponent(c)}
              className={`w-full text-left p-2 rounded-xl text-xs transition-all flex items-center justify-between cursor-pointer ${
                selectedComp.id === c.id 
                  ? 'bg-teal-950/70 border border-teal-500/60 text-teal-300 font-bold shadow-md shadow-teal-950/50' 
                  : 'text-slate-300 hover:bg-slate-800/50 border border-transparent'
              }`}
            >
              <div className="flex items-center gap-2">
                <span className="w-5 h-5 rounded-full bg-slate-800 border border-slate-700 text-[10px] font-mono flex items-center justify-center font-bold text-teal-400">
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

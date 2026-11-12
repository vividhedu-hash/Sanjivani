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
  const [showAirflow, setShowAirflow] = useState<boolean>(true);
  const [showThermalFlow, setShowThermalFlow] = useState<boolean>(true);
  const [activeFilter, setActiveFilter] = useState<'all' | 'thermal' | 'mechanical' | 'electrical' | 'sensing'>('all');

  // Three.js instance state
  const threeState = useRef<{
    scene: THREE.Scene;
    camera: THREE.PerspectiveCamera;
    renderer: THREE.WebGLRenderer;
    parts: { [id: number]: THREE.Object3D };
    lidPivot: THREE.Group;
    frontWall: THREE.Mesh;
    frontCutawayRims: THREE.Group;
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
  } | null>(null);

  useEffect(() => {
    if (!mountRef.current) return;

    const width = mountRef.current.clientWidth;
    const height = mountRef.current.clientHeight;

    // 1. Scene, Camera, Renderer
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xF8FAFC); // Clean Scientific Studio Off-White

    const camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 100);
    camera.position.set(6.8, 4.2, 8.5);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFShadowMap;

    mountRef.current.replaceChildren(renderer.domElement);

    // 2. High-End Studio Lighting for Light Mode Medical Enclosure
    const ambientLight = new THREE.AmbientLight(0xffffff, 1.25);
    scene.add(ambientLight);

    const keyLight = new THREE.DirectionalLight(0xffffff, 1.6);
    keyLight.position.set(10, 16, 12);
    keyLight.castShadow = true;
    keyLight.shadow.mapSize.width = 2048;
    keyLight.shadow.mapSize.height = 2048;
    keyLight.shadow.bias = -0.0001;
    scene.add(keyLight);

    const fillLight = new THREE.DirectionalLight(0xdbeafe, 0.85);
    fillLight.position.set(-10, 8, -8);
    scene.add(fillLight);

    const rimLight = new THREE.DirectionalLight(0xffffff, 0.6);
    rimLight.position.set(0, -6, 10);
    scene.add(rimLight);

    // Soft warm point light at heat sink exhaust
    const hotSinkLight = new THREE.PointLight(0xf59e0b, 1.8, 5);
    hotSinkLight.position.set(2.4, -0.6, 0.5);
    scene.add(hotSinkLight);

    // Soft cool point light inside vaccine cavity
    const coldCavityLight = new THREE.PointLight(0x38bdf8, 2.2, 4);
    coldCavityLight.position.set(-0.1, 0.9, 0.3);
    scene.add(coldCavityLight);

    // Shadow Catcher Ground Plane
    const groundGeo = new THREE.PlaneGeometry(30, 30);
    const groundMat = new THREE.ShadowMaterial({ opacity: 0.10 });
    const groundMesh = new THREE.Mesh(groundGeo, groundMat);
    groundMesh.rotation.x = -Math.PI / 2;
    groundMesh.position.y = -2.3;
    groundMesh.receiveShadow = true;
    scene.add(groundMesh);

    // -----------------------------------------------------------
    // 3. MATERIALS LIBRARY (Matching Schematic: White Cooler + Blue Trim)
    // -----------------------------------------------------------
    
    // Main White / Off-White Medical Cooler Outer Shell
    const matCoolerBody = new THREE.MeshStandardMaterial({
      color: 0xF1F5F9, // Clean Medical Cooler Off-White
      roughness: 0.38,
      metalness: 0.12,
    });

    // Vivid Royal Medical Blue for Corner Protectors, Cam Latches & Trim
    const matBlueTrim = new THREE.MeshStandardMaterial({
      color: 0x1E40AF, // Deep Royal Blue
      roughness: 0.35,
      metalness: 0.25,
    });

    // Sandy Beige PU Foam Core Insulation
    const matPUFoam = new THREE.MeshStandardMaterial({
      color: 0xE8DBBF, // Warm Sandy Tan PU Foam Core
      roughness: 0.92,
      metalness: 0.05,
    });

    // Dark Gasket / Seal on Lid
    const matGasket = new THREE.MeshStandardMaterial({
      color: 0x334155, // Slate Gasket
      roughness: 0.8,
    });

    // 6061-T6 Aircraft Aluminium Heat Spreader & Interior Dividing Shelf
    const matAluminium = new THREE.MeshStandardMaterial({
      color: 0xCBD5E1, // Brushed Silver Aluminium
      roughness: 0.22,
      metalness: 0.88,
    });

    // Crystalline Translucent Bio-PCM Ice-Blue Packs
    const matPCM = new THREE.MeshPhysicalMaterial({
      color: 0x38BDF8, // Vivid Ice Blue
      roughness: 0.14,
      metalness: 0.05,
      transmission: 0.82,
      thickness: 0.9,
      transparent: true,
      opacity: 0.90,
    });

    // Pure Electrolytic Copper (Peltier base & heat pipes)
    const matCopper = new THREE.MeshStandardMaterial({
      color: 0xEA580C, // Vibrant Copper
      roughness: 0.25,
      metalness: 0.92,
    });

    // Peltier Semiconductor Ceramic Substrate
    const matCeramicWhite = new THREE.MeshStandardMaterial({
      color: 0xF8FAFC,
      roughness: 0.3,
    });

    // Clear Vaccine Glass Vials
    const matGlass = new THREE.MeshPhysicalMaterial({
      color: 0xFFFFFF,
      roughness: 0.08,
      metalness: 0.05,
      transmission: 0.94,
      thickness: 0.3,
      transparent: true,
      opacity: 0.92,
    });

    // Blue Vaccine Liquid Inside Vials
    const matVaccine = new THREE.MeshStandardMaterial({
      color: 0x0284C7,
      roughness: 0.2,
    });

    // Deep Blue Rubber Stopper / Vial Cap
    const matVialCap = new THREE.MeshStandardMaterial({
      color: 0x1E3A8A,
      roughness: 0.45,
    });

    // Clear Acrylic Liquid Reservoir Chamber
    const matLiquidChamber = new THREE.MeshPhysicalMaterial({
      color: 0xE0F2FE,
      roughness: 0.1,
      metalness: 0.05,
      transmission: 0.92,
      thickness: 0.4,
      transparent: true,
      opacity: 0.88,
    });

    // Glowing Coolant Liquid in Reservoir
    const matCoolantFluid = new THREE.MeshStandardMaterial({
      color: 0x06B6D4,
      emissive: 0x0891B2,
      emissiveIntensity: 0.45,
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
      color: 0x1E293B,
      roughness: 0.6,
      metalness: 0.2,
    });

    // Green Circuit Board PCB
    const matPCB = new THREE.MeshStandardMaterial({
      color: 0x15803D, // Industrial FR4 Green
      roughness: 0.55,
      metalness: 0.25,
    });

    // Blue Illuminated 16x2 LCD Display
    const matLCD = new THREE.MeshStandardMaterial({
      color: 0x0369A1,
      emissive: 0x0284C7,
      emissiveIntensity: 0.85,
    });

    const partsMap: { [id: number]: THREE.Object3D } = {};
    const rootAssembly = new THREE.Group();
    scene.add(rootAssembly);

    // -----------------------------------------------------------
    // 4. ASSEMBLY GEOMETRY (Exact Match to Concept Schematic)
    // -----------------------------------------------------------
    
    // A. Main Outer Cooler Enclosure (Component 1)
    const enclosureGroup = new THREE.Group();

    // Box dimensions: Width = 4.5, Height = 3.2, Depth = 3.0
    // Back Wall
    const backWall = new THREE.Mesh(new THREE.BoxGeometry(4.5, 3.2, 0.12), matCoolerBody);
    backWall.position.set(0, 0, -1.44);
    backWall.castShadow = true;
    backWall.receiveShadow = true;
    enclosureGroup.add(backWall);

    // Bottom Wall
    const bottomWall = new THREE.Mesh(new THREE.BoxGeometry(4.5, 0.14, 3.0), matCoolerBody);
    bottomWall.position.set(0, -1.53, 0);
    bottomWall.castShadow = true;
    bottomWall.receiveShadow = true;
    enclosureGroup.add(bottomWall);

    // Left Wall
    const leftWall = new THREE.Mesh(new THREE.BoxGeometry(0.14, 3.2, 3.0), matCoolerBody);
    leftWall.position.set(-2.18, 0, 0);
    leftWall.castShadow = true;
    leftWall.receiveShadow = true;
    enclosureGroup.add(leftWall);

    // Left Recessed Side Handle with Blue Cup
    const handleCupLeft = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.5, 0.8), matBlueTrim);
    handleCupLeft.position.set(-2.23, 0.45, 0);
    enclosureGroup.add(handleCupLeft);

    // Right Wall (with circular heat sink exhaust vent)
    const rightWall = new THREE.Mesh(new THREE.BoxGeometry(0.14, 3.2, 3.0), matCoolerBody);
    rightWall.position.set(2.18, 0, 0);
    rightWall.castShadow = true;
    rightWall.receiveShadow = true;
    enclosureGroup.add(rightWall);

    // Right Recessed Side Handle with Blue Cup
    const handleCupRight = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.5, 0.8), matBlueTrim);
    handleCupRight.position.set(2.23, 0.45, 0);
    enclosureGroup.add(handleCupRight);

    // Front Wall (Removable on Cutaway)
    const frontWall = new THREE.Mesh(new THREE.BoxGeometry(4.5, 3.2, 0.12), matCoolerBody);
    frontWall.position.set(0, 0, 1.44);
    frontWall.castShadow = true;
    frontWall.visible = false; // Initially in cutaway view
    enclosureGroup.add(frontWall);

    // Two Blue Cam Latches on Front Wall
    const latchGeo = new THREE.BoxGeometry(0.24, 0.42, 0.08);
    const latch1 = new THREE.Mesh(latchGeo, matBlueTrim);
    latch1.position.set(-1.1, 1.0, 1.52);
    frontWall.add(latch1);

    const latch2 = new THREE.Mesh(latchGeo, matBlueTrim);
    latch2.position.set(1.1, 1.0, 1.52);
    frontWall.add(latch2);

    // Cutaway Cross-Section Rim (Shows the thick Sandy Tan PU Foam insulation wall)
    const frontCutawayRims = new THREE.Group();
    // Left Cut Rim
    const cutRimL = new THREE.Mesh(new THREE.BoxGeometry(0.16, 3.16, 0.08), matPUFoam);
    cutRimL.position.set(-2.17, 0, 1.46);
    frontCutawayRims.add(cutRimL);

    // Right Cut Rim
    const cutRimR = new THREE.Mesh(new THREE.BoxGeometry(0.16, 3.16, 0.08), matPUFoam);
    cutRimR.position.set(2.17, 0, 1.46);
    frontCutawayRims.add(cutRimR);

    // Bottom Cut Rim
    const cutRimB = new THREE.Mesh(new THREE.BoxGeometry(4.34, 0.16, 0.08), matPUFoam);
    cutRimB.position.set(0, -1.52, 1.46);
    frontCutawayRims.add(cutRimB);

    enclosureGroup.add(frontCutawayRims);

    // 4 Royal Blue Corner Bumpers at Bottom
    const cornerGeo = new THREE.BoxGeometry(0.42, 0.42, 0.42);
    const corners = [
      [-2.16, -1.48, -1.39],
      [2.16, -1.48, -1.39],
      [-2.16, -1.48, 1.39],
      [2.16, -1.48, 1.39]
    ];
    corners.forEach(([cx, cy, cz]) => {
      const cMesh = new THREE.Mesh(cornerGeo, matBlueTrim);
      cMesh.position.set(cx, cy, cz);
      enclosureGroup.add(cMesh);
    });

    partsMap[1] = enclosureGroup;
    rootAssembly.add(enclosureGroup);

    // B. Horizontal Aluminium Dividing Shelf (separates cold upper deck from active lower bay)
    const shelfMesh = new THREE.Mesh(new THREE.BoxGeometry(4.22, 0.08, 2.76), matAluminium);
    shelfMesh.position.set(0, 0.06, 0);
    shelfMesh.castShadow = true;
    shelfMesh.receiveShadow = true;
    rootAssembly.add(shelfMesh);

    // C. Upper Deck: Bio-PCM Packs (Component 2: Left & Right vertical packs)
    const pcmGroup = new THREE.Group();
    const pcmGeo = new THREE.BoxGeometry(0.38, 1.45, 1.95);

    // Left Side 2 PCM Packs
    const pcmL1 = new THREE.Mesh(pcmGeo, matPCM);
    pcmL1.position.set(-1.72, 0.85, 0);
    pcmGroup.add(pcmL1);

    const pcmL2 = new THREE.Mesh(pcmGeo, matPCM);
    pcmL2.position.set(-1.28, 0.85, 0);
    pcmGroup.add(pcmL2);

    // Right Side 2 PCM Packs
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
    // U-shaped / rectangular spreader surrounding the payload cavity
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
    
    // Clinical white vaccine holding tray
    const trayMesh = new THREE.Mesh(
      new THREE.BoxGeometry(1.98, 0.16, 1.88),
      new THREE.MeshStandardMaterial({ color: 0xF8FAFC, roughness: 0.3 })
    );
    trayMesh.position.set(0.1, 0.22, 0);
    payloadGroup.add(trayMesh);

    // 2 Rows of Vaccine Vials (Matching the Concept Schematic)
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

    // F. Upper Deck: Digital Temperature Sensor (Component 4)
    const sensorGroup = new THREE.Group();
    const probeMesh = new THREE.Mesh(
      new THREE.CylinderGeometry(0.045, 0.045, 0.35, 12),
      new THREE.MeshStandardMaterial({ color: 0x0F172A, metalness: 0.8, roughness: 0.2 })
    );
    probeMesh.position.set(1.18, 1.1, 0.4);
    sensorGroup.add(probeMesh);

    // Sensor cable routing down to control board
    const wireMat = new THREE.LineBasicMaterial({ color: 0x1E293B, linewidth: 2 });
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

    // G. Lower Deck: Peltier Thermoelectric Module Stack (Component 5 & 6 & 8 & 9)
    const peltierStackGroup = new THREE.Group();
    peltierStackGroup.position.set(-0.6, -0.42, 0.1);

    // Top Cold-Side Aluminium Spreader Plate
    const peltierTopAl = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.12, 1.2), matAluminium);
    peltierTopAl.position.set(0, 0.28, 0);
    peltierStackGroup.add(peltierTopAl);

    // Ceramic Upper Substrate
    const ceramicUpper = new THREE.Mesh(new THREE.BoxGeometry(1.25, 0.06, 1.05), matCeramicWhite);
    ceramicUpper.position.set(0, 0.19, 0);
    peltierStackGroup.add(ceramicUpper);

    // Semiconductor Layer (Bismuth Telluride Copper/Terracotta Core)
    const semiconductorCore = new THREE.Mesh(new THREE.BoxGeometry(1.18, 0.10, 0.98), matCopper);
    semiconductorCore.position.set(0, 0.11, 0);
    peltierStackGroup.add(semiconductorCore);

    // Ceramic Lower Substrate
    const ceramicLower = new THREE.Mesh(new THREE.BoxGeometry(1.25, 0.06, 1.05), matCeramicWhite);
    ceramicLower.position.set(0, 0.03, 0);
    peltierStackGroup.add(ceramicLower);

    // Liquid Cold/Hot Heat Exchanger Base Block
    const peltierExchanger = new THREE.Mesh(new THREE.BoxGeometry(1.45, 0.18, 1.25), matAluminium);
    peltierExchanger.position.set(0, -0.09, 0);
    peltierStackGroup.add(peltierExchanger);

    // Red & Black Silicone Power Wire Leads
    const redWireGeo = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(-0.55, 0.11, 0.3),
      new THREE.Vector3(-0.8, -0.2, 0.4),
      new THREE.Vector3(-0.8, -1.0, 0.5)
    ]);
    const redWire = new THREE.Line(redWireGeo, new THREE.LineBasicMaterial({ color: 0xDC2626, linewidth: 2 }));
    peltierStackGroup.add(redWire);

    const blkWireGeo = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(-0.55, 0.11, -0.3),
      new THREE.Vector3(-0.85, -0.2, -0.1),
      new THREE.Vector3(-0.85, -1.0, 0.4)
    ]);
    const blkWire = new THREE.Line(blkWireGeo, new THREE.LineBasicMaterial({ color: 0x0F172A, linewidth: 2 }));
    peltierStackGroup.add(blkWire);

    partsMap[5] = peltierStackGroup;
    partsMap[6] = semiconductorCore;
    partsMap[8] = peltierTopAl;
    partsMap[9] = peltierExchanger;
    rootAssembly.add(peltierStackGroup);

    // H. Lower Deck: Liquid Thermal-Transfer Chamber & Tubes
    const liquidChamberGroup = new THREE.Group();
    liquidChamberGroup.position.set(0.32, -0.72, 0.35);

    // Transparent Rectangular Acrylic Bottle
    const acrylicBottle = new THREE.Mesh(new THREE.BoxGeometry(0.52, 0.95, 0.52), matLiquidChamber);
    acrylicBottle.castShadow = true;
    liquidChamberGroup.add(acrylicBottle);

    // Internal Glowing Blue Coolant Liquid
    const liquidMesh = new THREE.Mesh(new THREE.BoxGeometry(0.46, 0.85, 0.46), matCoolantFluid);
    liquidChamberGroup.add(liquidMesh);

    // Reservoir Cap
    const capMesh = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 0.1, 16), matBlueTrim);
    capMesh.position.set(0, 0.52, 0);
    liquidChamberGroup.add(capMesh);

    rootAssembly.add(liquidChamberGroup);

    // Fluid Tubes (Blue Silicone Fluid Loop)
    // Tube 1: From Peltier block to Liquid Chamber
    const tube1 = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.045, 0.95, 12), matBlueTube);
    tube1.rotation.z = Math.PI / 2;
    tube1.position.set(-0.15, -0.24, 0.35);
    rootAssembly.add(tube1);

    // Tube 2: From Liquid Chamber across to Heatsink Radiator
    const tube2 = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.045, 0.85, 12), matBlueTube);
    tube2.rotation.z = Math.PI / 2;
    tube2.position.set(0.82, -0.24, 0.35);
    rootAssembly.add(tube2);

    // I. Lower Deck: Heat Sink with Fan (Component 10 & 11)
    const heatSinkFanGroup = new THREE.Group();
    heatSinkFanGroup.position.set(1.42, -0.65, 0.25);

    // Dense Metallic Aluminium Heatsink Fin Array (behind fan)
    const finArrayGroup = new THREE.Group();
    finArrayGroup.position.set(0, 0, -0.32);
    for (let fy = -0.48; fy <= 0.48; fy += 0.065) {
      const fin = new THREE.Mesh(new THREE.BoxGeometry(1.05, 0.016, 0.72), matAluminium);
      fin.position.set(0, fy, 0);
      finArrayGroup.add(fin);
    }
    heatSinkFanGroup.add(finArrayGroup);
    partsMap[10] = finArrayGroup;

    // Copper Heat Pipes through fins
    for (let py of [-0.25, 0.25]) {
      const hPipe = new THREE.Mesh(new THREE.CylinderGeometry(0.038, 0.038, 1.15, 12), matCopper);
      hPipe.rotation.z = Math.PI / 2;
      hPipe.position.set(0, py, -0.32);
      heatSinkFanGroup.add(hPipe);
    }

    // Square Axial Fan Shroud Housing (80mm)
    const fanShroud = new THREE.Mesh(new THREE.BoxGeometry(1.15, 1.15, 0.28), matFanShroud);
    fanShroud.position.set(0, 0, 0.14);
    heatSinkFanGroup.add(fanShroud);

    // Circular Fan Intake Aperture Rim
    const fanAperture = new THREE.Mesh(
      new THREE.CylinderGeometry(0.48, 0.48, 0.30, 24),
      new THREE.MeshStandardMaterial({ color: 0x0F172A })
    );
    fanAperture.rotation.x = Math.PI / 2;
    fanAperture.position.set(0, 0, 0.14);
    heatSinkFanGroup.add(fanAperture);

    // Rotating Fan Blades
    const fanBlades = new THREE.Group();
    fanBlades.position.set(0, 0, 0.15);
    // Center Hub
    const fanHub = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.14, 0.12, 16), matFanShroud);
    fanHub.rotation.x = Math.PI / 2;
    fanBlades.add(fanHub);

    // 7 Aerodynamic Curved Blades
    for (let b = 0; b < 7; b++) {
      const blade = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.36, 0.12), matFanShroud);
      blade.rotation.z = (b * Math.PI * 2) / 7;
      blade.position.set(
        Math.cos((b * Math.PI * 2) / 7) * 0.24,
        Math.sin((b * Math.PI * 2) / 7) * 0.24,
        0
      );
      fanBlades.add(blade);
    }
    heatSinkFanGroup.add(fanBlades);

    partsMap[11] = heatSinkFanGroup;
    rootAssembly.add(heatSinkFanGroup);

    // J. Lower Deck: Control Unit (Microcontroller + Relay + LCD) (Component 12)
    const ctrlUnitGroup = new THREE.Group();
    ctrlUnitGroup.position.set(-0.85, -1.22, 0.45);

    // Green Industrial FR4 PCB Board
    const pcbBoard = new THREE.Mesh(new THREE.BoxGeometry(1.42, 0.08, 0.95), matPCB);
    pcbBoard.castShadow = true;
    ctrlUnitGroup.add(pcbBoard);

    // Blue 16x2 LCD Display Screen
    const lcdScreen = new THREE.Mesh(new THREE.BoxGeometry(0.72, 0.08, 0.36), matLCD);
    lcdScreen.position.set(0.05, 0.08, 0);
    ctrlUnitGroup.add(lcdScreen);

    // Microcontroller IC Chip
    const icChip = new THREE.Mesh(
      new THREE.BoxGeometry(0.24, 0.06, 0.24),
      new THREE.MeshStandardMaterial({ color: 0x000000, roughness: 0.3 })
    );
    icChip.position.set(-0.48, 0.06, 0.15);
    ctrlUnitGroup.add(icChip);

    // Blue Relay Cube
    const relayCube = new THREE.Mesh(
      new THREE.BoxGeometry(0.26, 0.18, 0.22),
      new THREE.MeshStandardMaterial({ color: 0x1D4ED8, roughness: 0.4 })
    );
    relayCube.position.set(0.52, 0.12, 0.15);
    ctrlUnitGroup.add(relayCube);

    partsMap[12] = ctrlUnitGroup;
    rootAssembly.add(ctrlUnitGroup);

    // K. Insulated Lid with Openable Rear Hinge
    const lidPivot = new THREE.Group();
    lidPivot.position.set(0, 1.6, -1.48); // Rear top hinge position

    // Outer White Lid Slab
    const lidSlab = new THREE.Mesh(new THREE.BoxGeometry(4.54, 0.34, 3.04), matCoolerBody);
    lidSlab.position.set(0, 0.17, 1.52);
    lidSlab.castShadow = true;
    lidPivot.add(lidSlab);

    // 4 Blue Corner Protectors on Lid
    const lidCorners = [
      [-2.18, 0.17, 0.06],
      [2.18, 0.17, 0.06],
      [-2.18, 0.17, 2.98],
      [2.18, 0.17, 2.98]
    ];
    lidCorners.forEach(([lx, ly, lz]) => {
      const lc = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.36, 0.42), matBlueTrim);
      lc.position.set(lx, ly, lz);
      lidPivot.add(lc);
    });

    // Sandy Beige PU Foam Insulation Core Plug on Underbelly of Lid
    const lidPUFPlug = new THREE.Mesh(new THREE.BoxGeometry(4.15, 0.22, 2.65), matPUFoam);
    lidPUFPlug.position.set(0, -0.08, 1.52);
    lidPivot.add(lidPUFPlug);

    // Dark Gasket Perimeter Trim
    const lidGasketMesh = new THREE.Mesh(new THREE.BoxGeometry(4.28, 0.04, 2.78), matGasket);
    lidGasketMesh.position.set(0, 0.02, 1.52);
    lidPivot.add(lidGasketMesh);

    // Initial Lid Open Angle (~65 degrees)
    lidPivot.rotation.x = -1.15;

    rootAssembly.add(lidPivot);

    // -----------------------------------------------------------
    // 5. REALISTIC 3D AIRFLOW & THERMAL TRANSPORT DYNAMICS
    // -----------------------------------------------------------

    // A. Cool Ambient Intake Streamlines (Blue curved streamlines drawing into fan)
    const intakeLineCoords: number[] = [];
    for (let i = 0; i < 35; i++) {
      const startX = 0.8 + (Math.random() - 0.5) * 0.8;
      const startY = -0.65 + (Math.random() - 0.5) * 0.8;
      const startZ = 1.4 + Math.random() * 1.5;
      intakeLineCoords.push(
        startX, startY, startZ,
        1.42, -0.65, 0.35
      );
    }
    const intakeGeo = new THREE.BufferGeometry();
    intakeGeo.setAttribute('position', new THREE.Float32BufferAttribute(intakeLineCoords, 3));
    const airflowIntakeLines = new THREE.LineSegments(
      intakeGeo,
      new THREE.LineBasicMaterial({ color: 0x0284C7, transparent: true, opacity: 0.7, linewidth: 1.5 })
    );
    scene.add(airflowIntakeLines);

    // B. Hot Air Forced Exhaust Plume (Vivid Orange/Amber discharge out the right side)
    const exhaustCount = 450;
    const exhaustGeo = new THREE.BufferGeometry();
    const exhaustPos = new Float32Array(exhaustCount * 3);
    for (let i = 0; i < exhaustCount; i++) {
      exhaustPos[i * 3 + 0] = 2.2 + Math.random() * 2.5; // Expanding rightwards
      exhaustPos[i * 3 + 1] = -0.65 + (Math.random() - 0.5) * 1.2;
      exhaustPos[i * 3 + 2] = 0.25 + (Math.random() - 0.5) * 1.2;
    }
    exhaustGeo.setAttribute('position', new THREE.BufferAttribute(exhaustPos, 3));
    const airflowExhaustParticles = new THREE.Points(
      exhaustGeo,
      new THREE.PointsMaterial({ color: 0xEA580C, size: 0.085, transparent: true, opacity: 0.88 })
    );
    scene.add(airflowExhaustParticles);

    // C. Cold-Side Heat Absorption Vectors (Payload into Spreader and Peltier)
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
      new THREE.PointsMaterial({ color: 0x0284C7, size: 0.07, transparent: true, opacity: 0.85 })
    );
    scene.add(flowParticlesCold);

    // D. Circulating Coolant Fluid Loop Particles
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
      new THREE.PointsMaterial({ color: 0x06B6D4, size: 0.065, transparent: true, opacity: 0.95 })
    );
    scene.add(flowParticlesFluid);

    // -----------------------------------------------------------
    // 6. CAMERA ORBIT & INTERACTION CONTROLS
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

    // Mouse & Touch Dragging
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

    const onMouseUp = () => {
      isDragging = false;
    };

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
      lidPivot,
      frontWall,
      frontCutawayRims,
      airflowExhaustParticles,
      airflowIntakeLines,
      flowParticlesCold,
      flowParticlesFluid,
      fanBlades,
      orbitTarget,
      isDragging,
      prevMouseX,
      prevMouseY,
      spherical
    };

    // 7. Render Animation Loop
    let animFrameId: number;
    const startTime = performance.now();

    const animate = () => {
      animFrameId = requestAnimationFrame(animate);
      const elapsedTime = (performance.now() - startTime) * 0.001;

      // Spin Fan Blades
      fanBlades.rotation.z += 0.32;

      // Animate Turbulent Hot Air Exhaust Plume (Outward velocity x -> 5.5)
      const hPos = airflowExhaustParticles.geometry.attributes.position.array as Float32Array;
      for (let i = 0; i < exhaustCount; i++) {
        hPos[i * 3 + 0] += 0.048; // Outward velocity
        hPos[i * 3 + 1] += Math.sin(elapsedTime * 3 + i) * 0.004;
        if (hPos[i * 3 + 0] > 5.5) {
          hPos[i * 3 + 0] = 2.2;
        }
      }
      airflowExhaustParticles.geometry.attributes.position.needsUpdate = true;

      // Animate Cold Extraction Flow (descending toward lower deck)
      const cPos = flowParticlesCold.geometry.attributes.position.array as Float32Array;
      for (let i = 0; i < coldCount; i++) {
        cPos[i * 3 + 1] -= 0.012;
        if (cPos[i * 3 + 1] < 0.12) {
          cPos[i * 3 + 1] = 1.4;
        }
      }
      flowParticlesCold.geometry.attributes.position.needsUpdate = true;

      // Animate Coolant Fluid Loop Particles (circulating along tubes)
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

    // Cutaway: toggle between open sectional view and closed outer shell
    frontWall.visible = !isCutaway;
    frontCutawayRims.visible = isCutaway;

    // Lid animation: rotate open or flat closed
    lidPivot.rotation.x = isLidOpen ? -1.15 : 0;
  }, [isCutaway, isLidOpen]);

  // Toggle Visibility of Airflow and Thermal Vectors
  useEffect(() => {
    if (!threeState.current) return;
    const { airflowIntakeLines, airflowExhaustParticles, flowParticlesCold, flowParticlesFluid } = threeState.current;
    airflowIntakeLines.visible = showAirflow;
    airflowExhaustParticles.visible = showAirflow;
    flowParticlesCold.visible = showThermalFlow;
    flowParticlesFluid.visible = showThermalFlow;
  }, [showAirflow, showThermalFlow]);

  // Handle Component Selection & Smooth Camera Orbit
  const selectComponent = (comp: ComponentSpec) => {
    setSelectedComp(comp);
    sound.click();
    if (onSelectComponent) onSelectComponent(comp);

    if (threeState.current) {
      const { spherical } = threeState.current;
      if (comp.id === 2 || comp.id === 3) {
        // Upper deck focus
        spherical.theta = 0.85;
        spherical.phi = 0.95;
        spherical.radius = isSlideMode ? 8.2 : 9.0;
      } else if (comp.id === 5 || comp.id === 6 || comp.id === 8 || comp.id === 9) {
        // Peltier focus
        spherical.theta = 1.05;
        spherical.phi = 1.25;
        spherical.radius = isSlideMode ? 7.5 : 8.2;
      } else if (comp.id === 10 || comp.id === 11) {
        // Fan & Heat Sink focus
        spherical.theta = 0.45;
        spherical.phi = 1.25;
        spherical.radius = isSlideMode ? 7.8 : 8.5;
      } else if (comp.id === 12) {
        // Control board focus
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
  };

  const filteredComponents = COMPONENTS_3D.filter(c => 
    activeFilter === 'all' ? true : c.category === activeFilter
  );

  return (
    <div className={`relative w-full rounded-2xl overflow-hidden bg-white border border-slate-200 shadow-xl flex flex-col lg:flex-row ${
      isSlideMode ? 'h-[520px]' : 'h-[740px]'
    }`}>
      
      {/* 3D Canvas Area */}
      <div className="flex-1 relative h-[360px] lg:h-full bg-gradient-to-b from-[#F8FAFC] to-[#F1F5F9] overflow-hidden select-none">
        
        {/* Three.js Canvas Mount */}
        <div ref={mountRef} className="w-full h-full cursor-grab active:cursor-grabbing" />

        {/* Top-Left Mode & State Badges */}
        <div className="absolute top-3.5 left-3.5 z-10 flex flex-wrap items-center gap-2 pointer-events-none">
          <span className="px-2.5 py-1 rounded-lg text-[10px] font-mono uppercase bg-white/95 text-[#0F766E] border border-slate-200 font-bold shadow-sm backdrop-blur-md">
            SANJIVANI 3D SYSTEM SCHEMATIC
          </span>
          <span className="px-2.5 py-1 rounded-lg text-[10px] font-mono text-slate-600 bg-white/90 border border-slate-200 font-semibold shadow-sm backdrop-blur-md">
            450 × 300 × 320 mm
          </span>
        </div>

        {/* Interactive Overlay Action Bar */}
        <div className="absolute top-3.5 right-3.5 z-10 flex items-center gap-1.5 bg-white/95 border border-slate-200 p-1 rounded-xl shadow-md backdrop-blur-md">
          
          {/* Toggle Cutaway View */}
          <button
            onClick={() => { setIsCutaway(!isCutaway); sound.click(); }}
            className={`px-2.5 py-1 text-xs font-mono rounded-lg transition-all flex items-center gap-1.5 cursor-pointer ${
              isCutaway 
                ? 'bg-[#0F766E] text-white font-bold shadow-sm' 
                : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
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
                ? 'bg-[#0F766E] text-white font-bold shadow-sm' 
                : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
            }`}
            title="Open / Close Insulated Lid"
          >
            <Maximize2 className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">{isLidOpen ? 'Close Lid' : 'Open Lid'}</span>
          </button>

          {/* Toggle Airflow Dynamics */}
          <button
            onClick={() => { setShowAirflow(!showAirflow); sound.click(); }}
            className={`p-1.5 rounded-lg border transition-all cursor-pointer ${
              showAirflow 
                ? 'bg-amber-50 border-amber-300 text-amber-700 shadow-sm' 
                : 'bg-slate-100 border-slate-200 text-slate-400 hover:text-slate-700'
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
                ? 'bg-sky-50 border-sky-300 text-sky-700 shadow-sm' 
                : 'bg-slate-100 border-slate-200 text-slate-400 hover:text-slate-700'
            }`}
            title="Toggle Thermal Fluid Loop & Cold Extraction"
          >
            <Snowflake className="w-3.5 h-3.5" />
          </button>

          {/* Reset Camera Orbit */}
          <button
            onClick={resetCamera}
            className="p-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 transition-colors cursor-pointer"
            title="Reset Camera View"
          >
            <RotateCcw className="w-3.5 h-3.5" />
          </button>

        </div>

        {/* Bottom Legend & First Law Thermodynamic Statement */}
        <div className="absolute bottom-3 left-3 right-3 z-10 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 pointer-events-none">
          <div className="flex flex-wrap items-center gap-2 pointer-events-auto">
            <span className="flex items-center gap-1.5 text-[10px] font-mono font-bold bg-white/90 border border-slate-200 text-[#0F766E] px-2 py-0.5 rounded-md shadow-sm">
              <span className="w-2 h-2 rounded-full bg-[#38BDF8]"></span>
              Cold Side: 4.8kg Bio-PCM (+5.0°C)
            </span>
            <span className="flex items-center gap-1.5 text-[10px] font-mono font-bold bg-white/90 border border-slate-200 text-amber-800 px-2 py-0.5 rounded-md shadow-sm">
              <span className="w-2 h-2 rounded-full bg-[#EA580C]"></span>
              Hot Side Rejection: 48.5 W Exhaust
            </span>
            <span className="flex items-center gap-1.5 text-[10px] font-mono font-bold bg-white/90 border border-slate-200 text-cyan-800 px-2 py-0.5 rounded-md shadow-sm">
              <span className="w-2 h-2 rounded-full bg-[#06B6D4]"></span>
              Liquid Loop: Heat Transport
            </span>
          </div>

          <div className="hidden md:block pointer-events-auto bg-amber-50/95 border border-amber-300 rounded-xl p-2 px-3 shadow-md max-w-sm">
            <div className="flex items-center gap-1.5 text-[10px] font-mono font-bold text-amber-900">
              <Flame className="w-3.5 h-3.5 text-amber-600" />
              FIRST LAW THERMODYNAMICS
            </div>
            <p className="text-[10px] text-slate-700 leading-tight mt-0.5">
              The Peltier does not destroy heat. Hot side forcibly rejects:
            </p>
            <div className="font-mono text-[9px] text-amber-900 font-bold mt-0.5">
              Q̇_hot = Q̇_cold + P_elec = 18.5W + 30W = 48.5 W
            </div>
          </div>
        </div>
      </div>

      {/* Right Sidebar: Subsystem Inspection & Technical Specs */}
      <div className="w-full lg:w-[360px] h-[320px] lg:h-full bg-white border-t lg:border-t-0 lg:border-l border-slate-200 flex flex-col">
        
        {/* Header & Category Filters */}
        <div className="p-3 border-b border-slate-200 bg-slate-50/90">
          <div className="flex items-center justify-between mb-1.5">
            <h3 className="font-serif-display text-base font-bold text-[#0B2545]">
              Subsystem Inspector
            </h3>
            <span className="text-[10px] font-mono text-[#0F766E] bg-teal-50 px-2 py-0.5 rounded-full border border-teal-200 font-bold">
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
                    : 'bg-slate-200 text-slate-700 hover:bg-slate-300'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        {/* Selected Component Telemetry Details */}
        <div className="p-3 border-b border-slate-200 bg-white">
          <div className="flex items-start justify-between">
            <div>
              <span className="text-[9px] font-mono text-slate-500 uppercase tracking-widest block font-semibold">
                ID #{selectedComp.id.toString().padStart(2, '0')} • {selectedComp.category}
              </span>
              <h4 className="font-bold text-[#0B2545] text-sm mt-0.5">
                {selectedComp.name}
              </h4>
            </div>
            <span className={`text-[9px] font-mono font-bold px-1.5 py-0.5 rounded ${
              selectedComp.heatFluxRole === 'cold' ? 'bg-sky-100 text-sky-800' :
              selectedComp.heatFluxRole === 'hot' ? 'bg-amber-100 text-amber-800' :
              selectedComp.heatFluxRole === 'passive' ? 'bg-emerald-100 text-emerald-800' :
              'bg-purple-100 text-purple-800'
            }`}>
              {selectedComp.heatFluxRole.toUpperCase()}
            </span>
          </div>

          <div className="mt-1.5 space-y-1 text-xs">
            <div>
              <span className="text-slate-500 font-mono text-[9px] block">Role:</span>
              <p className="text-slate-700 text-[11px] leading-tight">{selectedComp.role}</p>
            </div>
            <div>
              <span className="text-slate-500 font-mono text-[9px] block">Scientific Principle:</span>
              <p className="text-slate-700 text-[11px] italic leading-tight">{selectedComp.principle}</p>
            </div>
            <div className="bg-slate-50 p-1.5 rounded-lg border border-slate-200">
              <span className="text-[#0F766E] font-mono text-[9px] block font-bold">Specification:</span>
              <p className="text-slate-900 font-mono text-[10px] mt-0.5 leading-snug">{selectedComp.specs}</p>
            </div>
            <p className="text-slate-600 text-[10px] leading-relaxed pt-0.5 line-clamp-2">
              {selectedComp.details}
            </p>
          </div>
        </div>

        {/* Scrollable Subsystems List */}
        <div className="flex-1 overflow-y-auto p-1.5 space-y-1 divide-y divide-slate-100">
          {filteredComponents.map(c => (
            <button
              key={c.id}
              onClick={() => selectComponent(c)}
              className={`w-full text-left p-1.5 rounded-lg text-xs transition-all flex items-center justify-between cursor-pointer ${
                selectedComp.id === c.id 
                  ? 'bg-teal-50 border border-teal-500 text-[#0F766E] font-bold' 
                  : 'text-slate-700 hover:bg-slate-50 border border-transparent'
              }`}
            >
              <div className="flex items-center gap-1.5">
                <span className="w-4 h-4 rounded-full bg-slate-200 text-[9px] font-mono flex items-center justify-center font-bold text-slate-700">
                  {c.id}
                </span>
                <span className="truncate max-w-[200px] text-[11px]">{c.name}</span>
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

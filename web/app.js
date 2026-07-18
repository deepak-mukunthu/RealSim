const DEFAULT_SCENARIO = {
  name: "Warehouse Delivery Starter",
  description: "One autonomous cart learns to move from inbound staging to the packing lane while avoiding shelf rows.",
  world_size: [82, 56],
  metadata: {
    use_case: "single_robot_delivery",
    units: "meters",
    max_steps: 850,
    future_extensions: [
      "multi_robot_task_assignment",
      "lidar_noise",
      "dynamic_people_and_forklifts",
      "ros2_bridge",
      "sim_to_real_policy_export"
    ]
  },
  robots: [
    {
      name: "Cart A",
      position: [8, 46],
      max_speed: 8,
      acceleration: 18,
      sensor_range: 9
    }
  ],
  targets: [
    {
      name: "Packing Lane",
      kind: "dropoff",
      position: [72, 46]
    }
  ],
  zones: [
    { name: "Inbound", kind: "pickup", position: [8, 46], size: [10, 8] },
    { name: "Pack", kind: "dropoff", position: [72, 46], size: [10, 8] },
    { name: "Charge", kind: "charging", position: [72, 10], size: [9, 7] }
  ],
  obstacles: [
    { name: "Shelf A1", kind: "shelf", position: [24, 17], size: [18, 3] },
    { name: "Shelf A2", kind: "shelf", position: [24, 29], size: [18, 3] },
    { name: "Shelf A3", kind: "shelf", position: [24, 41], size: [18, 3] },
    { name: "Shelf B1", kind: "shelf", position: [47, 13], size: [18, 3] },
    { name: "Shelf B2", kind: "shelf", position: [47, 25], size: [18, 3] },
    { name: "Shelf B3", kind: "shelf", position: [47, 37], size: [18, 3] },
    { name: "Packing Buffer", kind: "station", position: [66, 19], size: [6, 8] },
    { name: "Pillar", kind: "obstacle", position: [60, 8], size: 2.2 }
  ]
};

const ACTIONS = [
  [0, 0],
  [1, 0],
  [-1, 0],
  [0, 1],
  [0, -1],
  [1, 1],
  [1, -1],
  [-1, 1],
  [-1, -1]
];

const COLORS = {
  floor: "#f8fafc",
  grid: "#d7e0ea",
  text: "#1f2937",
  muted: "#64748b",
  blue: "#2563eb",
  blueSoft: "rgba(37, 99, 235, 0.14)",
  green: "#1f8e4b",
  cyan: "#0891b2",
  amber: "#d97706",
  purple: "#6e5bd3",
  red: "#c2410c",
  shelf: "#54627a",
  station: "#6e5bd3",
  obstacle: "#677488",
  selection: "#eab308"
};

const els = {};
const state = {
  scenario: clone(DEFAULT_SCENARIO),
  robots: [],
  qTable: new Map(),
  running: false,
  training: true,
  editMode: "select",
  selected: null,
  stepsPerFrame: 4,
  sensorRayCount: 16,
  step: 0,
  episode: 0,
  currentReward: 0,
  bestReward: 0,
  rewardHistory: [],
  collisionTotal: 0,
  lastCollisions: 0,
  explorationRate: 1,
  minExploration: 0.08,
  explorationDecay: 0.92,
  goalBias: 0.65,
  gridSize: 4,
  waypointStride: 5.5,
  dt: 1 / 60,
  viewport: { scale: 1, offsetX: 0, offsetY: 0 }
};

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function byId(id) {
  return document.getElementById(id);
}

function init() {
  [
    "worldCanvas",
    "rewardChart",
    "runState",
    "goalState",
    "scenarioSubtitle",
    "episodeMetric",
    "stepMetric",
    "rewardMetric",
    "bestMetric",
    "exploreMetric",
    "statesMetric",
    "distanceMetric",
    "collisionMetric",
    "playPauseBtn",
    "stepBtn",
    "resetBtn",
    "episodeBtn",
    "trainingToggle",
    "speedSlider",
    "speedValue",
    "raySlider",
    "rayValue",
    "propName",
    "propKind",
    "propX",
    "propY",
    "propW",
    "propH",
    "applyPropsBtn",
    "deleteSelectedBtn",
    "objectList",
    "scenarioName",
    "worldW",
    "worldH",
    "scenarioJson",
    "loadJsonBtn",
    "downloadJsonBtn",
    "copyJsonBtn"
  ].forEach((id) => {
    els[id] = byId(id);
  });

  resetTraining();
  resetEpisode();
  syncJsonPanel();
  bindEvents();
  requestAnimationFrame(loop);
}

function bindEvents() {
  document.querySelectorAll(".tab").forEach((button) => {
    button.addEventListener("click", () => setTab(button.dataset.tab));
  });

  document.querySelectorAll(".mode-button").forEach((button) => {
    button.addEventListener("click", () => setMode(button.dataset.mode));
  });

  els.playPauseBtn.addEventListener("click", toggleRun);
  els.stepBtn.addEventListener("click", () => {
    stepSimulation();
    render();
  });
  els.resetBtn.addEventListener("click", () => {
    state.running = false;
    resetEpisode();
    render();
  });
  els.episodeBtn.addEventListener("click", runEpisode);

  els.trainingToggle.addEventListener("change", () => {
    state.training = els.trainingToggle.checked;
  });
  els.speedSlider.addEventListener("input", () => {
    state.stepsPerFrame = Number(els.speedSlider.value);
    els.speedValue.textContent = String(state.stepsPerFrame);
  });
  els.raySlider.addEventListener("input", () => {
    state.sensorRayCount = Number(els.raySlider.value);
    els.rayValue.textContent = String(state.sensorRayCount);
  });

  els.worldCanvas.addEventListener("click", handleCanvasClick);
  els.applyPropsBtn.addEventListener("click", applyProperties);
  els.deleteSelectedBtn.addEventListener("click", deleteSelected);
  els.loadJsonBtn.addEventListener("click", loadScenarioFromText);
  els.downloadJsonBtn.addEventListener("click", downloadScenarioJson);
  els.copyJsonBtn.addEventListener("click", copyScenarioJson);

  [els.scenarioName, els.worldW, els.worldH].forEach((input) => {
    input.addEventListener("change", applyScenarioHeader);
  });

  window.addEventListener("resize", render);
}

function setTab(tabName) {
  document.querySelectorAll(".tab").forEach((button) => {
    button.classList.toggle("active", button.dataset.tab === tabName);
  });
  document.querySelectorAll(".panel-section").forEach((panel) => {
    panel.classList.remove("active");
  });
  byId(`${tabName}Panel`).classList.add("active");
}

function setMode(mode) {
  state.editMode = mode;
  document.querySelectorAll(".mode-button").forEach((button) => {
    button.classList.toggle("active", button.dataset.mode === mode);
  });
}

function normalizeScenario(raw) {
  const scenario = clone(raw);
  scenario.name = scenario.name || "Untitled Scenario";
  scenario.description = scenario.description || "";
  scenario.world_size = Array.isArray(scenario.world_size) ? scenario.world_size : [80, 56];
  scenario.metadata = scenario.metadata || {};
  scenario.metadata.max_steps = Number(scenario.metadata.max_steps || 850);
  scenario.robots = Array.isArray(scenario.robots) ? scenario.robots : [];
  scenario.targets = Array.isArray(scenario.targets) ? scenario.targets : [];
  scenario.zones = Array.isArray(scenario.zones) ? scenario.zones : [];
  scenario.obstacles = Array.isArray(scenario.obstacles) ? scenario.obstacles : [];

  if (scenario.robots.length === 0) {
    scenario.robots.push({
      name: "Cart A",
      position: [8, scenario.world_size[1] - 10],
      max_speed: 8,
      acceleration: 18,
      sensor_range: 9
    });
  }

  if (scenario.targets.length === 0) {
    scenario.targets.push({
      name: "Goal",
      kind: "dropoff",
      position: [scenario.world_size[0] - 8, scenario.world_size[1] - 10]
    });
  }

  return scenario;
}

function resetTraining() {
  state.qTable = new Map();
  state.episode = 0;
  state.currentReward = 0;
  state.bestReward = 0;
  state.rewardHistory = [];
  state.explorationRate = 1;
  state.collisionTotal = 0;
}

function resetEpisode() {
  const scenario = normalizeScenario(state.scenario);
  state.scenario = scenario;
  state.robots = scenario.robots.map((robot, index) => ({
    name: robot.name || `Robot ${index + 1}`,
    position: [Number(robot.position[0]), Number(robot.position[1])],
    velocity: [0, 0],
    waypoint: [...scenario.targets[Math.min(index, scenario.targets.length - 1)].position],
    maxSpeed: Number(robot.max_speed || 8),
    acceleration: Number(robot.acceleration || 18),
    sensorRange: Number(robot.sensor_range || 9),
    size: 0.5,
    trail: [[Number(robot.position[0]), Number(robot.position[1])]],
    arrived: false,
    arrivalAwarded: false
  }));
  state.step = 0;
  state.currentReward = 0;
  state.collisionTotal = 0;
  state.lastCollisions = 0;
  updateObjectList();
  populateProperties();
  syncJsonPanel();
}

function toggleRun() {
  state.running = !state.running;
  render();
}

function loop() {
  if (state.running) {
    for (let i = 0; i < state.stepsPerFrame; i += 1) {
      stepSimulation();
    }
  }
  render();
  requestAnimationFrame(loop);
}

function stepSimulation() {
  if (state.robots.length === 0) {
    resetEpisode();
  }

  const maxSteps = Number(state.scenario.metadata?.max_steps || 850);
  const robot = state.robots[0];
  const target = targetForRobot(0);
  const previousKey = encodeState(robot, target);
  const actionIndex = state.training ? selectActionIndex(robot, target) : null;

  if (state.training) {
    robot.waypoint = actionToWaypoint(robot, target, actionIndex);
  } else {
    robot.waypoint = [...target.position];
  }

  const previousDistances = state.robots.map((item, index) => distance(item.position, targetForRobot(index).position));
  const previousPositions = state.robots.map((item) => [...item.position]);

  state.lastCollisions = 0;
  state.robots.forEach((item, index) => updateRobot(item, index));
  resolveCollisions(previousPositions);

  const reward = calculateReward(previousDistances);
  state.currentReward += reward;
  state.step += 1;

  if (state.training && actionIndex !== null) {
    const nextKey = encodeState(robot, target);
    updateQ(previousKey, actionIndex, reward, nextKey, allArrived() || state.step >= maxSteps);
  }

  if (allArrived() || state.step >= maxSteps) {
    finishEpisode();
    return true;
  }

  return false;
}

function runEpisode() {
  const startEpisode = state.episode;
  let guard = 0;
  while (state.episode === startEpisode && guard < 5000) {
    stepSimulation();
    guard += 1;
  }
  state.running = false;
  render();
}

function finishEpisode() {
  state.episode += 1;
  state.rewardHistory.push(state.currentReward);
  state.bestReward = Math.max(...state.rewardHistory);
  state.explorationRate = Math.max(state.minExploration, state.explorationRate * state.explorationDecay);
  resetEpisode();
}

function updateRobot(robot, index) {
  if (robot.arrivalAwarded) {
    robot.velocity[0] *= 0.8;
    robot.velocity[1] *= 0.8;
    return;
  }

  const target = targetForRobot(index);
  if (distance(robot.position, target.position) < 0.5) {
    robot.arrived = true;
    robot.velocity[0] *= 0.75;
    robot.velocity[1] *= 0.75;
    return;
  }

  const dx = robot.waypoint[0] - robot.position[0];
  const dy = robot.waypoint[1] - robot.position[1];
  const length = Math.hypot(dx, dy);
  if (length > 0.001) {
    const desired = [(dx / length) * robot.maxSpeed, (dy / length) * robot.maxSpeed];
    const steering = [desired[0] - robot.velocity[0], desired[1] - robot.velocity[1]];
    const steeringLength = Math.hypot(steering[0], steering[1]);
    const maxSteer = robot.acceleration * state.dt;
    if (steeringLength > maxSteer) {
      steering[0] = (steering[0] / steeringLength) * maxSteer;
      steering[1] = (steering[1] / steeringLength) * maxSteer;
    }
    robot.velocity[0] += steering[0];
    robot.velocity[1] += steering[1];
  }

  const speed = Math.hypot(robot.velocity[0], robot.velocity[1]);
  if (speed > robot.maxSpeed) {
    robot.velocity[0] = (robot.velocity[0] / speed) * robot.maxSpeed;
    robot.velocity[1] = (robot.velocity[1] / speed) * robot.maxSpeed;
  }

  robot.position[0] += robot.velocity[0] * state.dt;
  robot.position[1] += robot.velocity[1] * state.dt;
  robot.position[0] = clamp(robot.position[0], robot.size, state.scenario.world_size[0] - robot.size);
  robot.position[1] = clamp(robot.position[1], robot.size, state.scenario.world_size[1] - robot.size);

  if (robot.trail.length === 0 || distance(robot.position, robot.trail[robot.trail.length - 1]) > 0.08) {
    robot.trail.push([...robot.position]);
  }
  if (robot.trail.length > 220) {
    robot.trail.shift();
  }
}

function resolveCollisions(previousPositions) {
  state.robots.forEach((robot, index) => {
    const hit = state.scenario.obstacles.some((obstacle) => circleObstacleCollision(robot.position, robot.size, obstacle));
    if (hit) {
      robot.position = [...previousPositions[index]];
      robot.velocity[0] *= -0.15;
      robot.velocity[1] *= -0.15;
      state.lastCollisions += 1;
      state.collisionTotal += 1;
    }
  });
}

function calculateReward(previousDistances) {
  let reward = -0.02 * state.robots.length;
  state.robots.forEach((robot, index) => {
    const target = targetForRobot(index);
    const newDistance = distance(robot.position, target.position);
    const progress = previousDistances[index] - newDistance;
    reward += progress * 0.8;

    if (newDistance < 0.5) {
      if (!robot.arrivalAwarded) {
        reward += 25;
      }
      robot.arrivalAwarded = true;
      robot.arrived = true;
      robot.waypoint = [...robot.position];
    } else {
      reward -= newDistance * 0.002;
    }
  });

  if (state.lastCollisions > 0) {
    reward -= state.lastCollisions * 6;
  }

  return reward;
}

function selectActionIndex(robot, target) {
  const key = encodeState(robot, target);
  const values = getQValues(key);

  if (Math.random() < state.explorationRate) {
    if (Math.random() < state.goalBias) {
      return goalDirectedAction(robot, target);
    }
    return Math.floor(Math.random() * ACTIONS.length);
  }

  const maxValue = Math.max(...values);
  if (maxValue <= 0) {
    return goalDirectedAction(robot, target);
  }
  return values.indexOf(maxValue);
}

function getQValues(key) {
  if (!state.qTable.has(key)) {
    state.qTable.set(key, new Array(ACTIONS.length).fill(0));
  }
  return state.qTable.get(key);
}

function updateQ(key, actionIndex, reward, nextKey, done) {
  const values = getQValues(key);
  const nextValues = getQValues(nextKey);
  const oldValue = values[actionIndex];
  const nextBest = done ? 0 : Math.max(...nextValues);
  const target = reward + 0.94 * nextBest;
  values[actionIndex] = oldValue + 0.18 * (target - oldValue);
}

function encodeState(robot, target) {
  const px = Math.floor(robot.position[0] / state.gridSize);
  const py = Math.floor(robot.position[1] / state.gridSize);
  const tx = Math.floor(target.position[0] / state.gridSize);
  const ty = Math.floor(target.position[1] / state.gridSize);
  return `${px},${py},${tx},${ty}`;
}

function goalDirectedAction(robot, target) {
  const dx = target.position[0] - robot.position[0];
  const dy = target.position[1] - robot.position[1];
  const sx = Math.abs(dx) > state.gridSize * 0.5 ? Math.sign(dx) : 0;
  const sy = Math.abs(dy) > state.gridSize * 0.5 ? Math.sign(dy) : 0;
  return ACTIONS.findIndex((action) => action[0] === sx && action[1] === sy);
}

function actionToWaypoint(robot, target, actionIndex) {
  const delta = ACTIONS[actionIndex] || [0, 0];
  const length = Math.hypot(delta[0], delta[1]);
  const goalDistance = distance(robot.position, target.position);
  if (goalDistance <= state.waypointStride) {
    return [...target.position];
  }
  if (length === 0) {
    return [...robot.position];
  }
  return [
    clamp(robot.position[0] + (delta[0] / length) * state.waypointStride, 0, state.scenario.world_size[0]),
    clamp(robot.position[1] + (delta[1] / length) * state.waypointStride, 0, state.scenario.world_size[1])
  ];
}

function allArrived() {
  return state.robots.every((robot) => robot.arrivalAwarded);
}

function targetForRobot(index) {
  const target = state.scenario.targets[Math.min(index, state.scenario.targets.length - 1)];
  return target || { name: "Goal", kind: "dropoff", position: [state.scenario.world_size[0] - 8, state.scenario.world_size[1] - 8] };
}

function render() {
  resizeCanvas(els.worldCanvas);
  resizeCanvas(els.rewardChart);
  drawWorld();
  drawRewardChart();
  updateMetrics();
}

function resizeCanvas(canvas) {
  const dpr = window.devicePixelRatio || 1;
  const rect = canvas.getBoundingClientRect();
  const width = Math.max(1, Math.floor(rect.width * dpr));
  const height = Math.max(1, Math.floor(rect.height * dpr));
  if (canvas.width !== width || canvas.height !== height) {
    canvas.width = width;
    canvas.height = height;
  }
}

function drawWorld() {
  const canvas = els.worldCanvas;
  const ctx = canvas.getContext("2d");
  const worldW = state.scenario.world_size[0];
  const worldH = state.scenario.world_size[1];
  const margin = 36 * (window.devicePixelRatio || 1);
  const scale = Math.min((canvas.width - margin * 2) / worldW, (canvas.height - margin * 2) / worldH);
  state.viewport.scale = scale;
  state.viewport.offsetX = (canvas.width - worldW * scale) / 2;
  state.viewport.offsetY = (canvas.height - worldH * scale) / 2;

  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = COLORS.floor;
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  drawGrid(ctx, worldW, worldH);

  state.scenario.zones.forEach((zone, index) => drawZone(ctx, zone, isSelected("zone", index)));
  state.scenario.obstacles.forEach((obstacle, index) => drawObstacle(ctx, obstacle, isSelected("obstacle", index)));
  state.scenario.targets.forEach((target, index) => drawTarget(ctx, target, isSelected("target", index)));
  state.robots.forEach((robot, index) => drawRobot(ctx, robot, index, isSelected("robot", index)));

  ctx.strokeStyle = COLORS.text;
  ctx.lineWidth = 1;
  const topLeft = worldToScreen([0, 0]);
  const bottomRight = worldToScreen([worldW, worldH]);
  ctx.strokeRect(topLeft[0], topLeft[1], bottomRight[0] - topLeft[0], bottomRight[1] - topLeft[1]);
}

function drawGrid(ctx, worldW, worldH) {
  const spacing = 5;
  ctx.strokeStyle = COLORS.grid;
  ctx.lineWidth = 1;
  for (let x = 0; x <= worldW; x += spacing) {
    const a = worldToScreen([x, 0]);
    const b = worldToScreen([x, worldH]);
    ctx.beginPath();
    ctx.moveTo(a[0], a[1]);
    ctx.lineTo(b[0], b[1]);
    ctx.stroke();
  }
  for (let y = 0; y <= worldH; y += spacing) {
    const a = worldToScreen([0, y]);
    const b = worldToScreen([worldW, y]);
    ctx.beginPath();
    ctx.moveTo(a[0], a[1]);
    ctx.lineTo(b[0], b[1]);
    ctx.stroke();
  }
}

function drawZone(ctx, zone, selected) {
  const color = zoneColor(zone.kind);
  const [x, y] = worldToScreen([zone.position[0] - zone.size[0] / 2, zone.position[1] - zone.size[1] / 2]);
  const [w, h] = worldSizeToScreen(zone.size);
  ctx.fillStyle = color.alpha;
  ctx.strokeStyle = selected ? COLORS.selection : color.stroke;
  ctx.lineWidth = selected ? 4 : 2;
  ctx.fillRect(x, y, w, h);
  ctx.strokeRect(x, y, w, h);
  drawLabel(ctx, zone.name, zone.position, color.stroke);
}

function drawObstacle(ctx, obstacle, selected) {
  const color = obstacleColor(obstacle.kind);
  ctx.fillStyle = color;
  ctx.strokeStyle = selected ? COLORS.selection : COLORS.text;
  ctx.lineWidth = selected ? 4 : 1.5;
  if (Array.isArray(obstacle.size)) {
    const [x, y] = worldToScreen([obstacle.position[0] - obstacle.size[0] / 2, obstacle.position[1] - obstacle.size[1] / 2]);
    const [w, h] = worldSizeToScreen(obstacle.size);
    ctx.fillRect(x, y, w, h);
    ctx.strokeRect(x, y, w, h);
    drawLabel(ctx, obstacle.name, obstacle.position, "#ffffff");
  } else {
    const [x, y] = worldToScreen(obstacle.position);
    ctx.beginPath();
    ctx.arc(x, y, obstacle.size * state.viewport.scale, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
  }
}

function drawTarget(ctx, target, selected) {
  const [x, y] = worldToScreen(target.position);
  ctx.strokeStyle = selected ? COLORS.selection : COLORS.green;
  ctx.fillStyle = COLORS.green;
  ctx.lineWidth = selected ? 4 : 3;
  ctx.beginPath();
  ctx.arc(x, y, 10 * (window.devicePixelRatio || 1), 0, Math.PI * 2);
  ctx.stroke();
  ctx.beginPath();
  ctx.arc(x, y, 3 * (window.devicePixelRatio || 1), 0, Math.PI * 2);
  ctx.fill();
  drawLabel(ctx, target.name, [target.position[0] + 4, target.position[1] - 2], COLORS.green);
}

function drawRobot(ctx, robot, index, selected) {
  if (robot.trail.length > 1) {
    ctx.strokeStyle = "rgba(83, 145, 245, 0.75)";
    ctx.lineWidth = 2;
    ctx.beginPath();
    robot.trail.forEach((point, pointIndex) => {
      const [x, y] = worldToScreen(point);
      if (pointIndex === 0) {
        ctx.moveTo(x, y);
      } else {
        ctx.lineTo(x, y);
      }
    });
    ctx.stroke();
  }

  drawSensorRays(ctx, robot);

  const [x, y] = worldToScreen(robot.position);
  const radius = Math.max(6, robot.size * state.viewport.scale);
  ctx.fillStyle = robot.arrivalAwarded ? COLORS.green : COLORS.blue;
  ctx.strokeStyle = selected ? COLORS.selection : "#ffffff";
  ctx.lineWidth = selected ? 4 : 2;
  ctx.beginPath();
  ctx.arc(x, y, radius, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  const speed = Math.hypot(robot.velocity[0], robot.velocity[1]);
  if (speed > 0.1) {
    const end = worldToScreen([robot.position[0] + robot.velocity[0] * 0.7, robot.position[1] + robot.velocity[1] * 0.7]);
    ctx.strokeStyle = COLORS.red;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(end[0], end[1]);
    ctx.stroke();
  }

  drawLabel(ctx, robot.name || `Robot ${index + 1}`, [robot.position[0] + 2, robot.position[1] + 2], COLORS.text);
}

function drawSensorRays(ctx, robot) {
  const origin = worldToScreen(robot.position);
  for (let i = 0; i < state.sensorRayCount; i += 1) {
    const angle = (i / state.sensorRayCount) * Math.PI * 2;
    const distanceValue = sensorDistance(robot.position, angle, robot.sensorRange);
    const end = worldToScreen([
      robot.position[0] + Math.cos(angle) * distanceValue,
      robot.position[1] + Math.sin(angle) * distanceValue
    ]);
    ctx.strokeStyle = distanceValue < robot.sensorRange * 0.35 ? "rgba(194, 65, 12, 0.55)" : "rgba(8, 145, 178, 0.35)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(origin[0], origin[1]);
    ctx.lineTo(end[0], end[1]);
    ctx.stroke();
  }
}

function drawLabel(ctx, text, position, color) {
  const [x, y] = worldToScreen(position);
  ctx.font = `${12 * (window.devicePixelRatio || 1)}px Inter, sans-serif`;
  ctx.fillStyle = color;
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText(text || "", x, y);
}

function drawRewardChart() {
  const canvas = els.rewardChart;
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "#ffffff";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  const padding = 26 * (window.devicePixelRatio || 1);
  const rewards = state.rewardHistory;
  ctx.strokeStyle = COLORS.grid;
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(padding, padding);
  ctx.lineTo(padding, canvas.height - padding);
  ctx.lineTo(canvas.width - padding, canvas.height - padding);
  ctx.stroke();

  if (rewards.length === 0) {
    ctx.fillStyle = COLORS.muted;
    ctx.font = `${12 * (window.devicePixelRatio || 1)}px Inter, sans-serif`;
    ctx.fillText("Reward history", padding + 8, padding + 14);
    return;
  }

  const minReward = Math.min(...rewards, 0);
  const maxReward = Math.max(...rewards, 1);
  const range = maxReward - minReward || 1;
  ctx.strokeStyle = COLORS.blue;
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  rewards.forEach((reward, index) => {
    const x = padding + (index / Math.max(1, rewards.length - 1)) * (canvas.width - padding * 2);
    const y = canvas.height - padding - ((reward - minReward) / range) * (canvas.height - padding * 2);
    if (index === 0) {
      ctx.moveTo(x, y);
    } else {
      ctx.lineTo(x, y);
    }
  });
  ctx.stroke();
}

function updateMetrics() {
  const arrived = state.robots.filter((robot) => robot.arrivalAwarded).length;
  const total = state.robots.length || 1;
  const avgDistance = state.robots.reduce((sum, robot, index) => sum + distance(robot.position, targetForRobot(index).position), 0) / total;

  els.runState.textContent = state.running ? "Running" : "Stopped";
  els.runState.classList.toggle("running", state.running);
  els.goalState.textContent = `${arrived}/${total} Arrived`;
  els.scenarioSubtitle.textContent = state.scenario.name;
  els.episodeMetric.textContent = String(state.episode);
  els.stepMetric.textContent = `${state.step}/${state.scenario.metadata?.max_steps || 850}`;
  els.rewardMetric.textContent = state.currentReward.toFixed(1);
  els.bestMetric.textContent = state.bestReward.toFixed(1);
  els.exploreMetric.textContent = `${Math.round(state.explorationRate * 100)}%`;
  els.statesMetric.textContent = String(state.qTable.size);
  els.distanceMetric.textContent = avgDistance.toFixed(1);
  els.collisionMetric.textContent = String(state.collisionTotal);

  const playSpan = els.playPauseBtn.querySelector("span");
  playSpan.textContent = state.running ? "Pause" : "Start";
}

function sensorDistance(position, angle, maxRange) {
  for (let value = 0.4; value <= maxRange; value += 0.4) {
    const point = [position[0] + Math.cos(angle) * value, position[1] + Math.sin(angle) * value];
    if (pointHitsWorldOrObstacle(point)) {
      return value;
    }
  }
  return maxRange;
}

function pointHitsWorldOrObstacle(point) {
  const [worldW, worldH] = state.scenario.world_size;
  if (point[0] < 0 || point[1] < 0 || point[0] > worldW || point[1] > worldH) {
    return true;
  }
  return state.scenario.obstacles.some((obstacle) => pointInObstacle(point, obstacle));
}

function handleCanvasClick(event) {
  const point = screenToWorld([event.offsetX * (window.devicePixelRatio || 1), event.offsetY * (window.devicePixelRatio || 1)]);
  if (!point) {
    return;
  }

  if (state.editMode === "select") {
    state.selected = findObjectAt(point);
  } else {
    addObjectAt(point, state.editMode);
  }
  populateProperties();
  updateObjectList();
  syncJsonPanel();
  render();
}

function findObjectAt(point) {
  for (let i = 0; i < state.robots.length; i += 1) {
    if (distance(point, state.robots[i].position) < 1.5) {
      return { type: "robot", index: i };
    }
  }
  for (let i = 0; i < state.scenario.targets.length; i += 1) {
    if (distance(point, state.scenario.targets[i].position) < 1.7) {
      return { type: "target", index: i };
    }
  }
  for (let i = 0; i < state.scenario.obstacles.length; i += 1) {
    if (pointInObstacle(point, state.scenario.obstacles[i])) {
      return { type: "obstacle", index: i };
    }
  }
  for (let i = 0; i < state.scenario.zones.length; i += 1) {
    if (pointInRect(point, state.scenario.zones[i].position, state.scenario.zones[i].size)) {
      return { type: "zone", index: i };
    }
  }
  return null;
}

function addObjectAt(point, type) {
  if (type === "shelf") {
    state.scenario.obstacles.push({
      name: `Shelf ${state.scenario.obstacles.length + 1}`,
      kind: "shelf",
      position: roundPair(point),
      size: [10, 3]
    });
    state.selected = { type: "obstacle", index: state.scenario.obstacles.length - 1 };
  }

  if (type === "zone") {
    state.scenario.zones.push({
      name: `Zone ${state.scenario.zones.length + 1}`,
      kind: "staging",
      position: roundPair(point),
      size: [10, 8]
    });
    state.selected = { type: "zone", index: state.scenario.zones.length - 1 };
  }

  if (type === "target") {
    state.scenario.targets[0] = {
      name: "Packing Lane",
      kind: "dropoff",
      position: roundPair(point)
    };
    state.selected = { type: "target", index: 0 };
  }

  if (type === "robot") {
    state.scenario.robots[0] = {
      name: "Cart A",
      position: roundPair(point),
      max_speed: 8,
      acceleration: 18,
      sensor_range: 9
    };
    state.selected = { type: "robot", index: 0 };
  }

  resetTraining();
  resetEpisode();
}

function getSelectedObject() {
  if (!state.selected) {
    return null;
  }
  const { type, index } = state.selected;
  if (type === "robot") {
    return state.scenario.robots[index];
  }
  if (type === "target") {
    return state.scenario.targets[index];
  }
  if (type === "obstacle") {
    return state.scenario.obstacles[index];
  }
  if (type === "zone") {
    return state.scenario.zones[index];
  }
  return null;
}

function populateProperties() {
  const object = getSelectedObject();
  const fields = [els.propName, els.propKind, els.propX, els.propY, els.propW, els.propH];
  if (!object) {
    fields.forEach((field) => {
      field.value = "";
      field.disabled = true;
    });
    return;
  }

  fields.forEach((field) => {
    field.disabled = false;
  });
  els.propName.value = object.name || "";
  els.propKind.value = object.kind || state.selected.type;
  els.propX.value = Number(object.position?.[0] || 0).toFixed(1);
  els.propY.value = Number(object.position?.[1] || 0).toFixed(1);

  if (Array.isArray(object.size)) {
    els.propW.value = Number(object.size[0]).toFixed(1);
    els.propH.value = Number(object.size[1]).toFixed(1);
  } else if (typeof object.size === "number") {
    els.propW.value = Number(object.size * 2).toFixed(1);
    els.propH.value = Number(object.size * 2).toFixed(1);
  } else {
    els.propW.value = "";
    els.propH.value = "";
  }
}

function applyProperties() {
  const object = getSelectedObject();
  if (!object) {
    return;
  }

  object.name = els.propName.value.trim() || object.name;
  object.kind = els.propKind.value.trim() || object.kind;
  object.position = [Number(els.propX.value || 0), Number(els.propY.value || 0)];

  if (state.selected.type === "obstacle") {
    const width = Number(els.propW.value || 2);
    const height = Number(els.propH.value || width);
    object.size = Math.abs(width - height) < 0.001 && object.kind === "obstacle" ? width / 2 : [width, height];
  }

  if (state.selected.type === "zone") {
    object.size = [Number(els.propW.value || 10), Number(els.propH.value || 8)];
  }

  resetTraining();
  resetEpisode();
  syncJsonPanel();
  render();
}

function deleteSelected() {
  if (!state.selected) {
    return;
  }
  const { type, index } = state.selected;
  if (type === "obstacle") {
    state.scenario.obstacles.splice(index, 1);
  }
  if (type === "zone") {
    state.scenario.zones.splice(index, 1);
  }
  if (type === "robot" && state.scenario.robots.length > 1) {
    state.scenario.robots.splice(index, 1);
  }
  if (type === "target" && state.scenario.targets.length > 1) {
    state.scenario.targets.splice(index, 1);
  }
  state.selected = null;
  resetTraining();
  resetEpisode();
  syncJsonPanel();
  render();
}

function updateObjectList() {
  const rows = [];
  const addRows = (items, type) => {
    items.forEach((item, index) => {
      rows.push({ type, index, name: item.name || `${type} ${index + 1}`, position: item.position });
    });
  };
  addRows(state.scenario.robots, "robot");
  addRows(state.scenario.targets, "target");
  addRows(state.scenario.obstacles, "obstacle");
  addRows(state.scenario.zones, "zone");

  els.objectList.innerHTML = "";
  rows.forEach((row) => {
    const button = document.createElement("button");
    button.className = `object-row${isSelected(row.type, row.index) ? " active" : ""}`;
    button.innerHTML = `<span>${row.type}</span><strong></strong><em>${row.position.map((v) => Number(v).toFixed(0)).join(", ")}</em>`;
    button.querySelector("strong").textContent = row.name;
    button.addEventListener("click", () => {
      state.selected = { type: row.type, index: row.index };
      setMode("select");
      populateProperties();
      updateObjectList();
      render();
    });
    els.objectList.appendChild(button);
  });
}

function syncJsonPanel() {
  els.scenarioName.value = state.scenario.name;
  els.worldW.value = state.scenario.world_size[0];
  els.worldH.value = state.scenario.world_size[1];
  els.scenarioJson.value = JSON.stringify(state.scenario, null, 2);
}

function applyScenarioHeader() {
  state.scenario.name = els.scenarioName.value.trim() || "Untitled Scenario";
  state.scenario.world_size = [
    Number(els.worldW.value || state.scenario.world_size[0]),
    Number(els.worldH.value || state.scenario.world_size[1])
  ];
  resetTraining();
  resetEpisode();
  syncJsonPanel();
  render();
}

function loadScenarioFromText() {
  try {
    state.scenario = normalizeScenario(JSON.parse(els.scenarioJson.value));
    state.selected = null;
    state.running = false;
    resetTraining();
    resetEpisode();
    render();
  } catch (error) {
    els.scenarioJson.focus();
    window.alert(`Invalid scenario JSON: ${error.message}`);
  }
}

function downloadScenarioJson() {
  const blob = new Blob([JSON.stringify(state.scenario, null, 2)], { type: "application/json" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = `${state.scenario.name.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "scenario"}.json`;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(link.href);
}

async function copyScenarioJson() {
  const text = JSON.stringify(state.scenario, null, 2);
  if (navigator.clipboard) {
    await navigator.clipboard.writeText(text);
  } else {
    els.scenarioJson.select();
    document.execCommand("copy");
  }
}

function isSelected(type, index) {
  return state.selected && state.selected.type === type && state.selected.index === index;
}

function worldToScreen(point) {
  return [
    state.viewport.offsetX + point[0] * state.viewport.scale,
    state.viewport.offsetY + point[1] * state.viewport.scale
  ];
}

function screenToWorld(point) {
  const x = (point[0] - state.viewport.offsetX) / state.viewport.scale;
  const y = (point[1] - state.viewport.offsetY) / state.viewport.scale;
  if (x < 0 || y < 0 || x > state.scenario.world_size[0] || y > state.scenario.world_size[1]) {
    return null;
  }
  return [x, y];
}

function worldSizeToScreen(size) {
  return [size[0] * state.viewport.scale, size[1] * state.viewport.scale];
}

function pointInObstacle(point, obstacle) {
  if (Array.isArray(obstacle.size)) {
    return pointInRect(point, obstacle.position, obstacle.size);
  }
  return distance(point, obstacle.position) <= obstacle.size;
}

function pointInRect(point, center, size) {
  return (
    point[0] >= center[0] - size[0] / 2 &&
    point[0] <= center[0] + size[0] / 2 &&
    point[1] >= center[1] - size[1] / 2 &&
    point[1] <= center[1] + size[1] / 2
  );
}

function circleObstacleCollision(position, radius, obstacle) {
  if (!Array.isArray(obstacle.size)) {
    return distance(position, obstacle.position) < radius + obstacle.size;
  }

  const left = obstacle.position[0] - obstacle.size[0] / 2;
  const right = obstacle.position[0] + obstacle.size[0] / 2;
  const top = obstacle.position[1] - obstacle.size[1] / 2;
  const bottom = obstacle.position[1] + obstacle.size[1] / 2;
  const closestX = clamp(position[0], left, right);
  const closestY = clamp(position[1], top, bottom);
  return Math.hypot(position[0] - closestX, position[1] - closestY) < radius;
}

function zoneColor(kind) {
  const map = {
    pickup: { stroke: COLORS.cyan, alpha: "rgba(8, 145, 178, 0.16)" },
    dropoff: { stroke: COLORS.green, alpha: "rgba(31, 142, 75, 0.16)" },
    charging: { stroke: COLORS.amber, alpha: "rgba(217, 119, 6, 0.18)" },
    staging: { stroke: COLORS.purple, alpha: "rgba(110, 91, 211, 0.14)" }
  };
  return map[kind] || { stroke: COLORS.muted, alpha: "rgba(100, 116, 139, 0.14)" };
}

function obstacleColor(kind) {
  const map = {
    shelf: COLORS.shelf,
    station: COLORS.purple,
    charger: COLORS.cyan,
    obstacle: COLORS.obstacle
  };
  return map[kind] || COLORS.obstacle;
}

function distance(a, b) {
  return Math.hypot(a[0] - b[0], a[1] - b[1]);
}

function clamp(value, min, max) {
  return Math.min(max, Math.max(min, value));
}

function roundPair(point) {
  return [Math.round(point[0] * 2) / 2, Math.round(point[1] * 2) / 2];
}

init();

# Dynamic Obstacles Feature

## Overview

The warehouse simulation now includes **dynamic moving obstacles** that add realism and challenge to robot navigation scenarios.

## Movement Patterns

Four distinct movement patterns are available:

1. **Linear** ⚡ - Moves in straight lines, bouncing off boundaries
2. **Circular** 🔄 - Rotates around a fixed center point
3. **Patrol** 📍 - Moves between predefined waypoints
4. **Random** 🚶 - Wanders with periodic direction changes

## Obstacle Types

### Moving Forklift 🚛
- **Pattern**: Patrol (waypoints)
- **Size**: 1.5 units
- **Speed**: 3.0 units/sec
- **Color**: Red (#ef4444)
- Simulates warehouse material handling equipment

### Roaming Person 🚶
- **Pattern**: Random walking
- **Size**: 0.4 units
- **Speed**: 1.2 units/sec
- **Color**: Orange (#f59e0b)
- Changes direction every 2-5 seconds
- Simulates warehouse workers moving around

### Circular Obstacle 🔄
- **Pattern**: Circular motion
- **Size**: 1.2 units
- **Speed**: 2.5 units/sec
- **Color**: Purple (#8b5cf6)
- Generic moving obstacle for testing

## Usage

### Web UI (Streamlit)

1. Launch the web app:
   ```bash
   ./launch_webapp.sh
   ```

2. In the sidebar, toggle **"🚛 Dynamic Obstacles"**

3. Adjust the number of moving obstacles using the slider (1-5)

4. Click **"🔄 Reset"** to regenerate with new settings

### Programmatic API

```python
from simulations.warehouse.environment import WarehouseEnv

# Create environment with dynamic obstacles
env = WarehouseEnv(
    scenario="configs/warehouse_delivery.json",
    enable_dynamic_obstacles=True,
    num_dynamic_obstacles=3,
)

# Access dynamic obstacles
for obstacle in env.dynamic_obstacles:
    print(f"{obstacle.name}: {obstacle.movement_pattern}")
    print(f"Position: {obstacle.position}")
    print(f"Trail length: {len(obstacle.trail)}")
```

### Desktop UI (Pygame)

Dynamic obstacles can be added to the desktop app by modifying `app.py`:

```python
env = WarehouseEnv(
    # ... other parameters
    enable_dynamic_obstacles=True,
    num_dynamic_obstacles=3,
)
```

## Visualization Features

- **Motion Trails**: Fading dotted lines show recent movement paths
- **Direction Arrows**: White-bordered arrows indicate current direction
- **Pattern Icons**: Emoji indicators show movement type
- **Glow Effects**: Pulsing glow around moving obstacles for visibility
- **Color Coding**: Different colors for different obstacle types

## Collision Detection

Dynamic obstacles are fully integrated with the physics system:

- Robots detect and avoid dynamic obstacles
- Collisions with moving obstacles are penalized
- Dynamic obstacles interact with world boundaries
- Movement updates occur every physics timestep (60 FPS)

## Technical Details

### Implementation

**File**: `simulations/core/dynamic_entity.py`
- `DynamicObstacle` - Base class for moving obstacles
- `MovingForklift` - Patrol pattern specialization
- `ConveyorBelt` - Linear movement specialization
- `RoamingPerson` - Random walking specialization

### Physics Integration

Dynamic obstacles update position each frame:
```python
for dyn_obs in env.dynamic_obstacles:
    dyn_obs.update(dt)
```

Trail history is maintained for visualization:
- Max trail length: 50 positions
- Records position every 0.2 units of movement
- Used for rendering motion paths

### Performance

- Minimal overhead: ~0.1ms per dynamic obstacle per frame
- Scales well to 5+ moving obstacles at 60 FPS
- Trail rendering optimized with alpha gradients

## Training Impact

Dynamic obstacles increase task difficulty:

- **Static scenario**: Average reward ~15-20
- **With 3 dynamic obstacles**: Average reward ~10-15
- Requires more sophisticated policies
- Encourages better collision avoidance
- Tests temporal prediction capabilities

## Future Enhancements

Potential improvements:

1. **Predictive indicators** - Show predicted path ahead
2. **Obstacle coordination** - Synchronized movement patterns
3. **Speed variation** - Random speed changes
4. **Smart obstacles** - React to robot presence
5. **Conveyor belt zones** - Push robots along path
6. **Traffic patterns** - Simulate rush hour scenarios

## Examples

### Basic Usage
```python
# Simple setup with dynamic obstacles
env = WarehouseEnv(
    enable_dynamic_obstacles=True,
    num_dynamic_obstacles=3,
)
env.reset()

# Run simulation
for _ in range(1000):
    action = env.action_space.sample()
    obs, reward, done, truncated, info = env.step(action)
```

### Custom Dynamic Obstacle
```python
from simulations.core.dynamic_entity import DynamicObstacle

# Create custom patrol obstacle
waypoints = [(20, 20), (80, 20), (80, 60), (20, 60)]
obstacle = DynamicObstacle(
    position=waypoints[0],
    size=2.0,
    name="Custom Patrol",
    movement_pattern="patrol",
    speed=2.5,
    waypoints=waypoints,
    bounds=(100, 75),
)

# Add to environment
env.dynamic_obstacles.append(obstacle)
```

## Troubleshooting

**Issue**: Dynamic obstacles not visible
- **Solution**: Ensure `enable_dynamic_obstacles=True` when creating environment

**Issue**: Obstacles move too fast/slow
- **Solution**: Adjust `speed` parameter when creating custom obstacles

**Issue**: Collision detection seems off
- **Solution**: Check obstacle `size` matches visual appearance

**Issue**: Trail not showing
- **Solution**: Ensure at least one `update()` call has occurred

## Related Files

- [simulations/core/dynamic_entity.py](simulations/core/dynamic_entity.py) - Implementation
- [simulations/warehouse/environment.py](simulations/warehouse/environment.py) - Integration
- [streamlit_app.py](streamlit_app.py) - Web UI with controls
- [simulations/core/physics.py](simulations/core/physics.py) - Collision detection

---

**Last Updated**: 2026-07-17

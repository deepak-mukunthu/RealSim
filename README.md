# RealSim RL Lab 🤖

> **Professional Reinforcement Learning Simulation Platform**

Build, train, and visualize intelligent agents in realistic simulated environments. Perfect for learning RL, experimenting with algorithms, or demonstrating autonomous systems.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 🎬 Demo

> 🎥 **Demo video coming soon!** See [DEMO_QUICK_START.md](DEMO_QUICK_START.md) to create your own.

Watch robots learn from random exploration to optimal behavior in real-time!

## ✨ Features

- 🎯 **Gymnasium-Compatible** - Standard RL environment interface
- 🖥️ **Dual UI** - Desktop (Pygame) and Web (Streamlit) interfaces
- 🤖 **Multi-Agent** - Coordinate multiple robots simultaneously
- 🚛 **Dynamic Obstacles** - Moving forklifts, people, conveyor belts
- 📊 **Live Visualization** - Watch learning in real-time
- 📈 **Performance Tracking** - Charts, metrics, and learning curves
- 🎓 **Educational** - Built-in explanations of RL concepts
- 🔧 **Extensible** - Easy to add new environments and algorithms

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/RealSim.git
cd RealSim

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Web App

```bash
streamlit run streamlit_app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

### Run the Desktop App

```bash
python app.py
```

## 📚 Documentation

- [Getting Started Guide](GET_STARTED.md)
- [Web App Guide](WEB_APP.md)
- [RL Concepts Explained](docs/RL_EXPLAINED.md)
- [Architecture Overview](docs/ARCHITECTURE.md)
- [Educational Features](EDUCATIONAL_FEATURES.md)
- [Dynamic Obstacles](DYNAMIC_OBSTACLES.md)

## 🎓 Learning Reinforcement Learning

RealSim is designed to make RL concepts intuitive:

### 1. **Visual Learning Phases**

Watch robots progress through learning:
- 🔍 **Exploring** - Trying random actions
- 📚 **Learning** - Balancing exploration and knowledge
- 🎯 **Exploiting** - Using learned strategies

### 2. **Interactive Controls**

- Adjust sensor rays to see perception impact
- Toggle dynamic obstacles for difficulty
- Compare trained vs untrained behavior

### 3. **Real-time Feedback**

- Live reward tracking
- Performance charts
- Learning progress indicators

## 🔬 Example Usage

### Basic Training Loop

```python
from simulations.warehouse.environment import WarehouseEnv
from examples.q_learning_agent import QLearningGridAgent

# Create environment
env = WarehouseEnv(
    scenario="configs/warehouse_delivery.json",
    enable_dynamic_obstacles=True
)

# Create agent
agent = QLearningGridAgent(world_size=env.world_size)

# Training loop
for episode in range(100):
    obs, info = env.reset()
    done = False
    total_reward = 0
    
    while not done:
        # Agent selects action
        action = agent.act(obs)
        
        # Environment step
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        
        # Agent learns
        agent.learn(obs, action, reward, done)
        total_reward += reward
    
    print(f"Episode {episode}: Reward = {total_reward:.2f}")
```

### Custom Environment

```python
from simulations.warehouse.environment import WarehouseEnv

env = WarehouseEnv(
    num_robots=5,
    world_size=(150, 100),
    num_obstacles=15,
    enable_dynamic_obstacles=True,
    num_dynamic_obstacles=5,
    sensor_ray_count=16
)
```

## 🏗️ Architecture

```
RealSim/
├── simulations/
│   ├── core/              # Core simulation engine
│   │   ├── entity.py      # Robots, obstacles, zones
│   │   ├── physics.py     # Collision detection, movement
│   │   ├── renderer.py    # Pygame visualization
│   │   ├── scenario.py    # Configuration loader
│   │   └── dynamic_entity.py  # Moving obstacles
│   └── warehouse/         # Warehouse scenario
│       ├── environment.py # Gymnasium environment
│       └── robot.py       # Robot behavior
├── examples/              # Training scripts and agents
│   ├── q_learning_agent.py
│   └── visualize_learning.py
├── configs/               # Scenario configurations
├── tests/                 # Unit tests
├── docs/                  # Documentation
├── app.py                 # Desktop UI
└── streamlit_app.py       # Web UI
```

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Ways to Contribute

- 🐛 Report bugs
- ✨ Suggest new features
- 📝 Improve documentation
- 🧪 Add tests
- 🎨 Create new environments
- 🤖 Implement new RL algorithms

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Gymnasium](https://gymnasium.farama.org/) for RL compatibility
- Visualizations powered by [Pygame](https://www.pygame.org/) and [Streamlit](https://streamlit.io/)
- Inspired by real-world warehouse automation challenges

## 🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

## 📬 Contact

Have questions or suggestions? Open an issue or start a discussion!

## 🎬 Creating Your Own Demo

Want to record a demo video for your fork or showcase custom environments?

**Quick start:**
```bash
./setup_demo.sh  # Interactive demo recording setup
```

**Full guide:** See [DEMO_QUICK_START.md](DEMO_QUICK_START.md) or [DEMO_RECORDING_GUIDE.md](DEMO_RECORDING_GUIDE.md)

---

**Made with ❤️ for the RL community**

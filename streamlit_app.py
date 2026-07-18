"""Professional Streamlit web application for RealSim RL Lab."""

from __future__ import annotations

import time
from pathlib import Path

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from matplotlib.patches import FancyBboxPatch

from examples.q_learning_agent import QLearningGridAgent
from simulations.warehouse.environment import WarehouseEnv


DEFAULT_SCENARIO = Path(__file__).parent / "configs" / "warehouse_delivery.json"


# Professional page config
st.set_page_config(
    page_title="RealSim RL Lab - Professional Edition",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Professional custom CSS
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global styles */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main container */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }

    /* Content wrapper */
    .block-container {
        background: #ffffff;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }

    /* Professional header */
    .pro-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }

    .pro-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }

    .pro-subtitle {
        font-size: 1.1rem;
        color: #e0e7ff;
        text-align: center;
        margin-top: 0.5rem;
        font-weight: 400;
    }

    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
    }

    .metric-label {
        font-size: 0.85rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1e293b;
        line-height: 1;
    }

    .metric-delta {
        font-size: 0.9rem;
        color: #10b981;
        margin-top: 0.5rem;
        font-weight: 500;
    }

    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 0.5rem 0;
    }

    .status-training {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }

    .status-exploring {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
    }

    .status-exploiting {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }

    /* Info cards */
    .info-card {
        background: white;
        border-left: 4px solid #667eea;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }

    .info-card-success {
        border-left-color: #10b981;
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
    }

    .info-card-warning {
        border-left-color: #f59e0b;
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
    }

    .info-card-info {
        border-left-color: #3b82f6;
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
    }

    /* Buttons styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
    }

    /* Progress bars */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }

    /* Section headers */
    .section-header {
        font-size: 1.3rem;
        font-weight: 700;
        color: #1e293b;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
    }

    /* Performance indicator */
    .perf-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    .perf-high { background: #10b981; }
    .perf-medium { background: #f59e0b; }
    .perf-low { background: #ef4444; }

    /* Chart container */
    .chart-container {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        margin: 1rem 0;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Responsive */
    @media (max-width: 768px) {
        .pro-title { font-size: 1.8rem; }
        .metric-value { font-size: 1.5rem; }
    }
</style>
""", unsafe_allow_html=True)


def init_state():
    """Initialize session state."""
    defaults = {
        "env": None,
        "agent": None,
        "obs": None,
        "info": {},
        "running": False,
        "episode_count": 0,
        "episode_rewards": [],
        "step_count": 0,
        "current_reward": 0.0,
        "total_collisions": 0,
        "training_mode": True,
        "sensor_rays": 16,
        "best_reward": float('-inf'),
        "avg_reward_10": 0.0,
        "dynamic_obstacles": False,
        "num_dynamic": 3,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def create_environment(training_mode: bool, sensor_rays: int, dynamic_obstacles: bool = False, num_dynamic: int = 3):
    """Create warehouse environment."""
    env = WarehouseEnv(
        scenario=DEFAULT_SCENARIO,
        render_mode=None,
        sensor_ray_count=sensor_rays,
        enable_dynamic_obstacles=dynamic_obstacles,
        num_dynamic_obstacles=num_dynamic,
    )
    obs, info = env.reset(seed=7)
    agent = QLearningGridAgent(world_size=tuple(env.world_size), waypoint_stride=5.5) if training_mode else None
    return env, agent, obs, info


def reset_environment():
    """Reset the environment."""
    env, agent, obs, info = create_environment(
        st.session_state.training_mode,
        st.session_state.sensor_rays,
        st.session_state.dynamic_obstacles,
        st.session_state.num_dynamic,
    )
    st.session_state.env = env
    st.session_state.agent = agent
    st.session_state.obs = obs
    st.session_state.info = info
    st.session_state.running = False
    st.session_state.episode_count = 0
    st.session_state.episode_rewards = []
    st.session_state.step_count = 0
    st.session_state.current_reward = 0.0
    st.session_state.total_collisions = 0
    st.session_state.best_reward = float('-inf')
    st.session_state.avg_reward_10 = 0.0


def guided_action(env: WarehouseEnv, obs: np.ndarray):
    """Generate guided action toward goal."""
    shaped = obs.reshape(env.num_robots, 7)
    return shaped[:, 4:6]


def run_step():
    """Execute one simulation step."""
    env = st.session_state.env
    obs = st.session_state.obs
    agent = st.session_state.agent

    if env is None or obs is None:
        reset_environment()
        env = st.session_state.env
        obs = st.session_state.obs
        agent = st.session_state.agent

    if agent:
        action_index, action = agent.select_action(obs)
    else:
        action_index = None
        action = guided_action(env, obs)

    next_obs, reward, terminated, truncated, info = env.step(action)
    done = terminated or truncated

    if agent and action_index is not None:
        agent.update(obs, action_index, reward, next_obs, done)

    st.session_state.obs = next_obs
    st.session_state.info = info
    st.session_state.current_reward += reward
    st.session_state.step_count += 1
    st.session_state.total_collisions += info.get("collisions", 0)

    if done:
        finish_episode()


def finish_episode():
    """Complete current episode."""
    agent = st.session_state.agent
    env = st.session_state.env

    if agent:
        agent.finish_episode(
            st.session_state.current_reward,
            st.session_state.step_count,
            st.session_state.total_collisions,
        )

    st.session_state.episode_count += 1
    st.session_state.episode_rewards.append(st.session_state.current_reward)

    # Update best and average
    st.session_state.best_reward = max(st.session_state.best_reward, st.session_state.current_reward)
    if len(st.session_state.episode_rewards) >= 10:
        st.session_state.avg_reward_10 = np.mean(st.session_state.episode_rewards[-10:])
    else:
        st.session_state.avg_reward_10 = np.mean(st.session_state.episode_rewards)

    st.session_state.obs, st.session_state.info = env.reset(seed=7 + st.session_state.episode_count)
    st.session_state.current_reward = 0.0
    st.session_state.step_count = 0
    st.session_state.total_collisions = 0


def run_episode():
    """Run complete episode."""
    if st.session_state.env is None:
        reset_environment()

    env = st.session_state.env
    start_episode = st.session_state.episode_count
    while st.session_state.episode_count == start_episode:
        run_step()
        if st.session_state.step_count >= env.max_steps:
            break


def create_professional_visualization(env: WarehouseEnv):
    """Create professional-looking matplotlib visualization."""
    # Use professional style
    plt.style.use('seaborn-v0_8-darkgrid')

    fig, ax = plt.subplots(figsize=(12, 8), facecolor='#f8fafc')
    ax.set_facecolor('#ffffff')

    ax.set_xlim(-2, env.world_size[0] + 2)
    ax.set_ylim(-2, env.world_size[1] + 2)
    ax.set_aspect('equal')

    # Professional grid
    ax.grid(True, alpha=0.15, linewidth=0.5, color='#cbd5e1')
    ax.set_axisbelow(True)

    # Color scheme
    zone_colors = {
        "pickup": "#3b82f6",
        "dropoff": "#10b981",
        "charging": "#f59e0b",
        "staging": "#8b5cf6",
    }
    obstacle_colors = {
        "shelf": "#475569",
        "station": "#7c3aed",
        "charger": "#0891b2",
        "obstacle": "#64748b",
    }

    # Draw zones with gradient effect
    for zone in env.zones:
        color = zone_colors.get(zone.kind, "#64748b")
        rect = FancyBboxPatch(
            (zone.position[0] - zone.width / 2, zone.position[1] - zone.height / 2),
            zone.width,
            zone.height,
            boxstyle="round,pad=0.1",
            linewidth=2,
            edgecolor=color,
            facecolor=color,
            alpha=0.15,
        )
        ax.add_patch(rect)

        # Zone label with background
        ax.text(
            zone.position[0], zone.position[1], zone.name,
            ha="center", va="center",
            fontsize=9, fontweight='600',
            color=color,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor=color, alpha=0.9)
        )

    # Draw obstacles with professional styling
    for obstacle in env.obstacles:
        color = obstacle_colors.get(obstacle.kind, "#64748b")
        if obstacle.shape == "rect":
            rect = FancyBboxPatch(
                (obstacle.position[0] - obstacle.width / 2, obstacle.position[1] - obstacle.height / 2),
                obstacle.width,
                obstacle.height,
                boxstyle="round,pad=0.2",
                linewidth=1.5,
                edgecolor='#1e293b',
                facecolor=color,
                alpha=0.9,
            )
            ax.add_patch(rect)
            ax.text(
                obstacle.position[0], obstacle.position[1],
                obstacle.name,
                ha="center", va="center",
                fontsize=8, fontweight='600',
                color='white'
            )
        else:
            circle = plt.Circle(obstacle.position, obstacle.size, color=color, alpha=0.85, linewidth=2, edgecolor='#1e293b')
            ax.add_patch(circle)

    # Draw dynamic obstacles with motion trails
    for dyn_obs in env.dynamic_obstacles:
        dyn_color = '#ef4444' if dyn_obs.kind == 'forklift' else '#f59e0b' if dyn_obs.kind == 'person' else '#8b5cf6'

        # Draw trail with fading effect
        if len(dyn_obs.trail) > 1:
            trail = np.array(dyn_obs.trail)
            for i in range(len(trail) - 1):
                alpha = 0.2 + (i / len(trail)) * 0.5
                ax.plot(
                    trail[i:i+2, 0], trail[i:i+2, 1],
                    color=dyn_color, linewidth=2, alpha=alpha, linestyle=':'
                )

        # Draw motion indicator (arrow)
        if np.linalg.norm(dyn_obs.direction) > 0:
            arrow_scale = 2.0
            ax.arrow(
                dyn_obs.position[0], dyn_obs.position[1],
                dyn_obs.direction[0] * arrow_scale, dyn_obs.direction[1] * arrow_scale,
                head_width=0.6, head_length=0.8,
                fc=dyn_color, ec='white', linewidth=1.5, alpha=0.8
            )

        # Draw obstacle with pulsing glow
        glow = plt.Circle(dyn_obs.position, dyn_obs.size * 1.8, color=dyn_color, alpha=0.15)
        ax.add_patch(glow)

        circle = plt.Circle(
            dyn_obs.position, dyn_obs.size,
            color=dyn_color, alpha=0.9,
            linewidth=2.5, edgecolor='white'
        )
        ax.add_patch(circle)

        # Label with movement pattern
        pattern_icon = "⚡" if dyn_obs.movement_pattern == "linear" else "🔄" if dyn_obs.movement_pattern == "circular" else "🚶" if dyn_obs.movement_pattern == "random" else "📍"
        ax.text(
            dyn_obs.position[0], dyn_obs.position[1],
            pattern_icon,
            ha="center", va="center",
            fontsize=12, color='white'
        )

    # Draw targets with modern design
    for index, target in enumerate(env.targets):
        name = env.target_names[index] if index < len(env.target_names) else f"Goal {index + 1}"

        # Outer glow
        glow = plt.Circle(target, 1.8, color='#10b981', alpha=0.1)
        ax.add_patch(glow)

        # Target rings
        target_ring1 = plt.Circle(target, 1.2, color='#10b981', fill=False, linewidth=3)
        target_ring2 = plt.Circle(target, 0.7, color='#10b981', fill=False, linewidth=2)
        target_dot = plt.Circle(target, 0.3, color='#10b981', alpha=0.8)

        ax.add_patch(target_ring1)
        ax.add_patch(target_ring2)
        ax.add_patch(target_dot)

        # Label with background
        ax.text(
            target[0], target[1] - 2.2, name,
            fontsize=10, fontweight='700',
            color='#10b981',
            ha='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='#10b981', linewidth=2, alpha=0.95)
        )

    # Draw robots with professional styling
    for index, robot in enumerate(env.robots):
        arrived = env.has_reached_goal(index)
        color = '#10b981' if arrived else '#667eea'

        # Robot trail with gradient
        if len(robot.trail) > 1:
            trail = np.array(robot.trail[-150:])
            for i in range(len(trail) - 1):
                alpha = 0.3 + (i / len(trail)) * 0.5
                ax.plot(
                    trail[i:i+2, 0], trail[i:i+2, 1],
                    color=color, linewidth=2.5, alpha=alpha
                )

        # Sensor rays with modern look
        readings = env.get_sensor_readings(index)
        for ray_index, distance in enumerate(readings):
            angle = (ray_index / len(readings)) * np.pi * 2.0
            endpoint = robot.position + np.array([np.cos(angle), np.sin(angle)]) * distance
            ax.plot(
                [robot.position[0], endpoint[0]],
                [robot.position[1], endpoint[1]],
                color='#0891b2', linewidth=1, alpha=0.4, linestyle='--'
            )
            # Endpoint dot
            ax.plot(endpoint[0], endpoint[1], 'o', color='#0891b2', markersize=3, alpha=0.6)

        # Robot body with glow effect
        glow = plt.Circle(robot.position, robot.size * 2.5, color=color, alpha=0.15)
        ax.add_patch(glow)

        robot_circle = plt.Circle(
            robot.position, robot.size * 1.8,
            color=color, alpha=0.95,
            linewidth=3, edgecolor='white'
        )
        ax.add_patch(robot_circle)

        # Robot center indicator
        center = plt.Circle(robot.position, robot.size * 0.6, color='white', alpha=0.9)
        ax.add_patch(center)

        # Robot label
        ax.text(
            robot.position[0], robot.position[1] - 2.5,
            robot.name,
            ha="center", va="top",
            fontsize=9, fontweight='700',
            color=color,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor=color, linewidth=2, alpha=0.95)
        )

        # Status indicator
        if arrived:
            ax.text(
                robot.position[0], robot.position[1] + 2.5,
                "✓ ARRIVED",
                ha="center", va="bottom",
                fontsize=8, fontweight='700',
                color='white',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='#10b981', alpha=0.95)
            )

    # Professional axis styling
    ax.set_xlabel('Distance (meters)', fontsize=11, fontweight='600', color='#475569')
    ax.set_ylabel('Distance (meters)', fontsize=11, fontweight='600', color='#475569')

    title = env.scenario.name if env.scenario else "Warehouse Simulation"
    ax.set_title(
        title,
        fontsize=14, fontweight='700',
        color='#1e293b',
        pad=20
    )

    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#cbd5e1')
    ax.spines['bottom'].set_color('#cbd5e1')

    plt.tight_layout()
    return fig


def create_performance_chart():
    """Create professional performance chart."""
    if not st.session_state.episode_rewards:
        return None

    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(10, 5), facecolor='#f8fafc')
    ax.set_facecolor('#ffffff')

    episodes = list(range(1, len(st.session_state.episode_rewards) + 1))
    rewards = st.session_state.episode_rewards

    # Plot with gradient fill
    ax.plot(episodes, rewards, color='#667eea', linewidth=3, label='Episode Reward', marker='o', markersize=5, markerfacecolor='#764ba2', markeredgecolor='white', markeredgewidth=2)
    ax.fill_between(episodes, rewards, alpha=0.3, color='#667eea')

    # Moving average
    if len(rewards) >= 5:
        window = min(5, len(rewards))
        moving_avg = np.convolve(rewards, np.ones(window)/window, mode='valid')
        avg_episodes = list(range(window, len(rewards) + 1))
        ax.plot(avg_episodes, moving_avg, '--', color='#10b981', linewidth=2.5, label=f'{window}-Episode Average', alpha=0.8)

    # Best reward line
    if st.session_state.best_reward > float('-inf'):
        ax.axhline(y=st.session_state.best_reward, color='#f59e0b', linestyle=':', linewidth=2, label=f'Best: {st.session_state.best_reward:.1f}', alpha=0.7)

    ax.set_xlabel('Episode', fontsize=11, fontweight='600', color='#475569')
    ax.set_ylabel('Reward', fontsize=11, fontweight='600', color='#475569')
    ax.set_title('Learning Performance', fontsize=13, fontweight='700', color='#1e293b', pad=15)

    ax.legend(loc='lower right', frameon=True, fancybox=True, shadow=True, fontsize=9)
    ax.grid(True, alpha=0.2, linewidth=0.5)

    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#cbd5e1')
    ax.spines['bottom'].set_color('#cbd5e1')

    plt.tight_layout()
    return fig


def main():
    """Main application."""
    init_state()

    # Professional header
    st.markdown("""
    <div class="pro-header">
        <h1 class="pro-title">🤖 RealSim RL Lab</h1>
        <p class="pro-subtitle">Professional Reinforcement Learning Simulation Platform</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Control Center")

        # Training mode toggle with educational info
        training = st.toggle("🧠 Enable Q-Learning", value=st.session_state.training_mode, key="training_toggle",
                           help="Q-Learning is an RL algorithm where robots learn from trial-and-error by maximizing rewards")
        if training != st.session_state.training_mode:
            st.session_state.training_mode = training
            reset_environment()

        # Educational tooltip
        if st.session_state.training_mode and st.session_state.agent:
            epsilon = st.session_state.agent.exploration_rate
            if epsilon > 0.5:
                phase_icon = "🔍"
                phase = "Exploring"
                phase_desc = "Robot is trying random actions to discover what works"
            elif epsilon > 0.1:
                phase_icon = "📚"
                phase = "Learning"
                phase_desc = "Robot is balancing exploration with what it has learned"
            else:
                phase_icon = "🎯"
                phase = "Exploiting"
                phase_desc = "Robot is using its learned knowledge to act optimally"

            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 12px; border-radius: 8px; margin: 10px 0;">
                <div style="color: white; font-weight: 600; font-size: 14px;">
                    {phase_icon} {phase} Phase
                </div>
                <div style="color: #e0e7ff; font-size: 12px; margin-top: 4px;">
                    {phase_desc}
                </div>
                <div style="color: #fbbf24; font-size: 11px; margin-top: 6px;">
                    Exploration Rate: {epsilon:.1%}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Sensor rays slider with explanation
        sensor_rays = st.slider("📡 Sensor Rays", 4, 24, st.session_state.sensor_rays, 4,
                               help="Number of distance sensors around the robot. More rays = more detailed perception but slower learning")
        if sensor_rays != st.session_state.sensor_rays:
            st.session_state.sensor_rays = sensor_rays
            if st.session_state.env:
                reset_environment()

        st.markdown("---")

        # Dynamic obstacles toggle
        dynamic = st.toggle("🚛 Dynamic Obstacles", value=st.session_state.dynamic_obstacles, help="Add moving forklifts and people")
        if dynamic != st.session_state.dynamic_obstacles:
            st.session_state.dynamic_obstacles = dynamic
            reset_environment()

        if st.session_state.dynamic_obstacles:
            num_dyn = st.slider("# Moving Obstacles", 1, 5, st.session_state.num_dynamic)
            if num_dyn != st.session_state.num_dynamic:
                st.session_state.num_dynamic = num_dyn
                reset_environment()

        st.markdown("---")

        # Control buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Reset", use_container_width=True):
                reset_environment()
                st.rerun()

        with col2:
            if st.button("⏭️ Run Episode", use_container_width=True):
                run_episode()
                st.rerun()

        if st.button("▶️ Start" if not st.session_state.running else "⏸️ Pause", use_container_width=True):
            st.session_state.running = not st.session_state.running
            st.rerun()

        st.markdown("---")

        # Educational Section - How RL Works
        with st.expander("📚 How Reinforcement Learning Works", expanded=False):
            st.markdown("""
            **Reinforcement Learning** teaches robots through trial and error:

            **1. 🎯 Goal**: Navigate to target zones while avoiding obstacles

            **2. 👀 Observe**: Robots use sensors to see their surroundings

            **3. 🎬 Act**: Choose where to move next

            **4. 🎁 Reward**:
            - ✅ Positive: Reaching goals, making progress
            - ❌ Negative: Collisions, wasting time

            **5. 📚 Learn**: Remember which actions led to good rewards

            **6. 🔁 Repeat**: Get better with each episode!

            ---

            **Exploration vs Exploitation:**
            - 🔍 **Explore**: Try random actions (early learning)
            - 🎯 **Exploit**: Use learned knowledge (mastery)

            The robot gradually shifts from exploring to exploiting as it learns.
            """)

        st.markdown("---")

        # Status info
        if st.session_state.env:
            status = "🟢 Running" if st.session_state.running else "⏸️ Paused"
            mode = "🧠 Training" if st.session_state.training_mode else "🎮 Demo"

            st.markdown(f"""
            <div class="info-card info-card-info">
                <strong>Status:</strong> {status}<br>
                <strong>Mode:</strong> {mode}
            </div>
            """, unsafe_allow_html=True)

    # Main content
    if st.session_state.env is None:
        reset_environment()

    # Metrics row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card" title="Number of complete training episodes run">
            <div class="metric-label">📊 Episode</div>
            <div class="metric-value">{st.session_state.episode_count}</div>
            <div style="font-size: 10px; color: #64748b; margin-top: 4px;">Training attempts</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        reward_color = "#10b981" if st.session_state.current_reward > 0 else "#ef4444"
        reward_emoji = "🎉" if st.session_state.current_reward > 0 else "⚠️"
        st.markdown(f"""
        <div class="metric-card" title="Total reward from last episode">
            <div class="metric-label">{reward_emoji} Current Reward</div>
            <div class="metric-value" style="color: {reward_color};">{st.session_state.current_reward:.1f}</div>
            <div style="font-size: 10px; color: #64748b; margin-top: 4px;">{"Good!" if st.session_state.current_reward > 0 else "Needs work"}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        trend_emoji = "📈" if st.session_state.avg_reward_10 > 0 else "📉"
        st.markdown(f"""
        <div class="metric-card" title="Average reward over last 10 episodes - shows learning trend">
            <div class="metric-label">{trend_emoji} Avg Reward (10)</div>
            <div class="metric-value" style="color: #667eea;">{st.session_state.avg_reward_10:.1f}</div>
            <div style="font-size: 10px; color: #64748b; margin-top: 4px;">Learning trend</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        best_color = "#f59e0b" if st.session_state.best_reward > float('-inf') else "#64748b"
        best_val = st.session_state.best_reward if st.session_state.best_reward > float('-inf') else 0.0
        st.markdown(f"""
        <div class="metric-card" title="Highest reward achieved - the goal to beat">
            <div class="metric-label">🏆 Best Reward</div>
            <div class="metric-value" style="color: {best_color};">{best_val:.1f}</div>
            <div style="font-size: 10px; color: #64748b; margin-top: 4px;">Personal best</div>
        </div>
        """, unsafe_allow_html=True)

    # Beginner tip
    if st.session_state.episode_count == 0:
        st.info("💡 **Getting Started**: Enable Q-Learning in the sidebar, then click '▶️ Start' or '⏭️ Run Episode' to watch robots learn! They'll start by exploring randomly, then gradually improve as they learn which paths work best.")

    # Training status badge
    if st.session_state.training_mode and st.session_state.agent:
        explore_rate = st.session_state.agent.exploration_rate
        if explore_rate > 0.5:
            badge_class = "status-exploring"
            badge_text = f"🔴 EXPLORING ({explore_rate:.1%})"
            tip = "Robots are trying random actions to discover what works"
        elif explore_rate > 0.2:
            badge_class = "status-training"
            badge_text = f"🟡 LEARNING ({explore_rate:.1%})"
            tip = "Robots are balancing exploration with learned knowledge"
        else:
            badge_class = "status-exploiting"
            badge_text = f"🟢 EXPLOITING ({explore_rate:.1%})"
            tip = "Robots are using learned knowledge to act optimally"

        st.markdown(f'<div class="status-badge {badge_class}" title="{tip}">{badge_text}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Main visualization and chart
    col_left, col_right = st.columns([1.5, 1])

    with col_left:
        st.markdown('<div class="section-header">🎯 Live Simulation</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig = create_professional_visualization(st.session_state.env)
        st.pyplot(fig)
        plt.close()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="section-header">📈 Performance</div>', unsafe_allow_html=True)

        if st.session_state.episode_rewards:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            perf_fig = create_performance_chart()
            if perf_fig:
                st.pyplot(perf_fig)
                plt.close()
            st.markdown('</div>', unsafe_allow_html=True)

            # Additional stats
            if st.session_state.agent:
                stats = st.session_state.agent.get_stats()
                known_states = stats.get('known_states', 0)

                st.markdown(f"""
                <div class="info-card info-card-success">
                    <strong>🧠 Known States:</strong> {known_states}<br>
                    <strong>📊 Episodes Completed:</strong> {st.session_state.episode_count}<br>
                    <strong>🎯 Current Step:</strong> {st.session_state.step_count}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="info-card info-card-warning">
                <strong>⏳ Waiting for data...</strong><br>
                Click "Run Episode" to start training!
            </div>
            """, unsafe_allow_html=True)

    # Auto-refresh for running simulation
    if st.session_state.running and st.session_state.env is not None:
        time.sleep(0.05)
        run_step()
        st.rerun()


if __name__ == "__main__":
    main()

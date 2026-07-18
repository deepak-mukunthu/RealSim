"""Streamlit web application for RealSim RL Lab."""

from __future__ import annotations

import os
import time
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).parent / ".matplotlib-cache"))

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from examples.q_learning_agent import QLearningGridAgent
from simulations.warehouse.environment import WarehouseEnv


DEFAULT_SCENARIO = Path(__file__).parent / "configs" / "warehouse_delivery.json"


def init_state():
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
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def create_environment(training_mode: bool, sensor_rays: int):
    env = WarehouseEnv(
        scenario=DEFAULT_SCENARIO,
        render_mode=None,
        sensor_ray_count=sensor_rays,
    )
    obs, info = env.reset(seed=7)
    agent = QLearningGridAgent(world_size=tuple(env.world_size), waypoint_stride=5.5) if training_mode else None
    return env, agent, obs, info


def reset_environment():
    env, agent, obs, info = create_environment(
        st.session_state.training_mode,
        st.session_state.sensor_rays,
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


def guided_action(env: WarehouseEnv, obs: np.ndarray):
    shaped = obs.reshape(env.num_robots, 7)
    return shaped[:, 4:6]


def run_step():
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
    st.session_state.obs, st.session_state.info = env.reset(seed=7 + st.session_state.episode_count)
    st.session_state.current_reward = 0.0
    st.session_state.step_count = 0
    st.session_state.total_collisions = 0


def run_episode():
    if st.session_state.env is None:
        reset_environment()

    env = st.session_state.env
    start_episode = st.session_state.episode_count
    while st.session_state.episode_count == start_episode:
        run_step()
        if st.session_state.step_count >= env.max_steps:
            break


def visualize_environment(env: WarehouseEnv):
    fig, ax = plt.subplots(figsize=(11, 7.5))
    ax.set_xlim(0, env.world_size[0])
    ax.set_ylim(0, env.world_size[1])
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.22)
    ax.set_facecolor("#f6f8fb")

    zone_colors = {
        "pickup": "#0891b2",
        "dropoff": "#1f8e4b",
        "charging": "#eab308",
        "staging": "#6e5bd3",
    }
    obstacle_colors = {
        "shelf": "#54627a",
        "station": "#6e5bd3",
        "charger": "#0891b2",
        "obstacle": "#677488",
    }

    for zone in env.zones:
        rect = patches.Rectangle(
            (zone.position[0] - zone.width / 2, zone.position[1] - zone.height / 2),
            zone.width,
            zone.height,
            linewidth=1.5,
            edgecolor=zone_colors.get(zone.kind, "#64748b"),
            facecolor=zone_colors.get(zone.kind, "#64748b"),
            alpha=0.16,
        )
        ax.add_patch(rect)
        ax.text(zone.position[0], zone.position[1], zone.name, ha="center", va="center", fontsize=8)

    for obstacle in env.obstacles:
        color = obstacle_colors.get(obstacle.kind, "#677488")
        if obstacle.shape == "rect":
            rect = patches.Rectangle(
                (obstacle.position[0] - obstacle.width / 2, obstacle.position[1] - obstacle.height / 2),
                obstacle.width,
                obstacle.height,
                linewidth=1,
                edgecolor="#1d2939",
                facecolor=color,
                alpha=0.88,
            )
            ax.add_patch(rect)
            ax.text(obstacle.position[0], obstacle.position[1], obstacle.name, ha="center", va="center", fontsize=7, color="white")
        else:
            circle = plt.Circle(obstacle.position, obstacle.size, color=color, alpha=0.8)
            ax.add_patch(circle)

    for index, target in enumerate(env.targets):
        name = env.target_names[index] if index < len(env.target_names) else f"Goal {index + 1}"
        target_ring = plt.Circle(target, 1.0, color="#1f8e4b", fill=False, linewidth=2.5)
        target_dot = plt.Circle(target, 0.22, color="#1f8e4b")
        ax.add_patch(target_ring)
        ax.add_patch(target_dot)
        ax.text(target[0] + 1.4, target[1] + 0.4, name, fontsize=9, color="#1f8e4b")

    for index, robot in enumerate(env.robots):
        arrived = index < len(env._arrival_awarded) and env._arrival_awarded[index]
        color = "#1f8e4b" if arrived else "#2563eb"

        if len(robot.trail) > 1:
            trail = np.array(robot.trail[-120:])
            ax.plot(trail[:, 0], trail[:, 1], color="#5391f5", linewidth=1.5, alpha=0.75)

        readings = env.get_sensor_readings(index)
        for ray_index, distance in enumerate(readings):
            angle = (ray_index / len(readings)) * np.pi * 2.0
            endpoint = robot.position + np.array([np.cos(angle), np.sin(angle)]) * distance
            ax.plot([robot.position[0], endpoint[0]], [robot.position[1], endpoint[1]], color="#0891b2", linewidth=0.5, alpha=0.35)

        robot_circle = plt.Circle(robot.position, robot.size * 1.6, color=color, alpha=0.88)
        ax.add_patch(robot_circle)
        ax.text(robot.position[0], robot.position[1] - 1.6, robot.name, ha="center", va="top", fontsize=8)

    ax.set_xlabel("meters")
    ax.set_ylabel("meters")
    ax.set_title(env.scenario.name if env.scenario else "Warehouse")
    return fig


def sidebar_controls():
    st.sidebar.header("Simulation")
    st.sidebar.caption(str(DEFAULT_SCENARIO.relative_to(Path(__file__).parent)))

    training_mode = st.sidebar.checkbox("Q-learning", value=st.session_state.training_mode)
    sensor_rays = st.sidebar.slider("Sensor rays", 4, 24, st.session_state.sensor_rays)
    steps_per_refresh = st.sidebar.slider("Steps per refresh", 1, 12, 4)

    if training_mode != st.session_state.training_mode or sensor_rays != st.session_state.sensor_rays:
        st.session_state.training_mode = training_mode
        st.session_state.sensor_rays = sensor_rays
        reset_environment()
        st.rerun()

    col1, col2 = st.sidebar.columns(2)
    if col1.button("Reset", use_container_width=True):
        reset_environment()
        st.rerun()
    if col2.button("Step", use_container_width=True):
        run_step()
        st.rerun()

    col3, col4 = st.sidebar.columns(2)
    if col3.button("Run episode", use_container_width=True):
        run_episode()
        st.rerun()
    if col4.button("Pause" if st.session_state.running else "Start", use_container_width=True):
        st.session_state.running = not st.session_state.running
        st.rerun()

    return steps_per_refresh


def render_metrics():
    info = st.session_state.info or {}
    stats = st.session_state.agent.get_stats() if st.session_state.agent else {}

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Episode", st.session_state.episode_count)
    col2.metric("Step", st.session_state.step_count)
    col3.metric("Reward", f"{st.session_state.current_reward:.1f}")
    col4.metric("Arrived", f"{info.get('robots_arrived', 0)}/{info.get('total_robots', 1)}")

    if stats:
        col5, col6, col7, col8 = st.columns(4)
        col5.metric("Avg reward", f"{stats['avg_reward']:.1f}")
        col6.metric("Best reward", f"{stats['best_reward']:.1f}")
        col7.metric("Exploration", f"{stats['exploration_rate']:.1%}")
        col8.metric("Known states", stats["known_states"])


def render_reward_history():
    rewards = st.session_state.episode_rewards
    if not rewards:
        st.info("Run an episode to populate the reward chart.")
        return

    fig, ax = plt.subplots(figsize=(7, 3.2))
    ax.plot(range(1, len(rewards) + 1), rewards, color="#2563eb", linewidth=2)
    ax.set_xlabel("episode")
    ax.set_ylabel("reward")
    ax.set_title("Training reward")
    ax.grid(True, alpha=0.25)
    st.pyplot(fig)
    plt.close(fig)


def main():
    st.set_page_config(
        page_title="RealSim RL Lab",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    init_state()
    if st.session_state.env is None:
        reset_environment()

    steps_per_refresh = sidebar_controls()

    st.title("RealSim RL Lab")
    st.caption("Configurable visual environments for reinforcement learning and robotics prototypes.")

    render_metrics()

    left, right = st.columns([2.2, 1])
    with left:
        st.subheader("Scenario Map")
        fig = visualize_environment(st.session_state.env)
        st.pyplot(fig)
        plt.close(fig)

    with right:
        st.subheader("Reward History")
        render_reward_history()
        st.subheader("Scenario")
        st.write(st.session_state.env.scenario.description)
        st.write(f"World size: {tuple(st.session_state.env.world_size.astype(int))} meters")
        st.write(f"Obstacles: {len(st.session_state.env.obstacles)}")

    if st.session_state.running:
        for _ in range(steps_per_refresh):
            run_step()
        time.sleep(0.05)
        st.rerun()


if __name__ == "__main__":
    main()

"""Interactive UI application for the simulation platform."""

from pathlib import Path
from typing import Optional

import pygame
import numpy as np

from examples.q_learning_agent import QLearningGridAgent
from simulations.warehouse.environment import WarehouseEnv


DEFAULT_SCENARIO = Path(__file__).parent / "configs" / "warehouse_delivery.json"


class SimulationApp:
    """Interactive application with GUI controls."""

    def __init__(self):
        pygame.init()

        # Window setup
        self.sim_width = 900
        self.sim_height = 675
        self.panel_width = 350
        self.total_width = self.sim_width + self.panel_width
        self.screen = pygame.display.set_mode((self.total_width, self.sim_height))
        pygame.display.set_caption("AI Robotics Simulation - Interactive Demo")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 20)

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.DARK_GRAY = (100, 100, 100)
        self.BLUE = (37, 99, 235)
        self.GREEN = (31, 142, 75)
        self.RED = (211, 47, 47)
        self.LIGHT_BLUE = (191, 219, 254)

        # Simulation parameters
        self.scenario_path = DEFAULT_SCENARIO
        self.max_steps = 500
        self.steps_per_frame = 1
        self.sensor_rays = 16
        self.training_mode = False

        # State
        self.env: Optional[WarehouseEnv] = None
        self.agent: Optional[QLearningGridAgent] = None
        self.running = False
        self.paused = False
        self.episode_count = 0
        self.episode_reward = 0.0
        self.step_count = 0
        self.total_collisions = 0

        # UI elements
        self.buttons = []
        self.sliders = []
        self._create_ui_elements()

        # Initialize environment
        self._reset_simulation()

    def _create_ui_elements(self):
        """Create interactive UI elements."""
        panel_x = self.sim_width + 10
        y = 70

        # Buttons
        self.buttons = [
            Button(panel_x, y, 150, 40, "Start", self.GREEN, self._start_simulation),
            Button(panel_x + 160, y, 150, 40, "Pause", self.BLUE, self._pause_simulation),
            Button(panel_x, y + 50, 150, 40, "Reset", self.RED, self._reset_simulation),
            Button(panel_x + 160, y + 50, 150, 40, "New Episode", self.BLUE, self._new_episode),
        ]

        y += 120

        # Toggle training mode
        self.training_toggle = Button(
            panel_x, y, 330, 40,
            "Training: OFF",
            self.DARK_GRAY,
            self._toggle_training
        )
        self.buttons.append(self.training_toggle)

        y += 70

        # Sliders
        self.sliders = [
            Slider(panel_x, y, 330, "Steps/frame", 1, 8, self.steps_per_frame, self._on_steps_change),
            Slider(panel_x, y + 60, 330, "Sensor Rays", 4, 24, self.sensor_rays, self._on_sensor_rays_change),
        ]

    def _start_simulation(self):
        """Start or resume simulation."""
        self.running = True
        self.paused = False

    def _pause_simulation(self):
        """Pause simulation."""
        self.paused = not self.paused

    def _reset_simulation(self):
        """Reset entire simulation."""
        self.running = False
        self.paused = False
        self.episode_count = 0
        self.episode_reward = 0.0
        self.step_count = 0
        self.total_collisions = 0

        if self.env:
            self.env.close()

        self.env = WarehouseEnv(
            scenario=self.scenario_path,
            max_steps=self.max_steps,
            sensor_ray_count=self.sensor_rays,
            render_mode=None  # We'll render manually
        )

        if self.training_mode:
            self.agent = QLearningGridAgent(world_size=tuple(self.env.world_size), waypoint_stride=5.5)
        else:
            self.agent = None

        self.obs, self.info = self.env.reset()

    def _new_episode(self):
        """Start a new episode."""
        if self.env:
            self.obs, self.info = self.env.reset()
            self.episode_reward = 0.0
            self.step_count = 0
            self.total_collisions = 0

    def _toggle_training(self):
        """Toggle RL training mode."""
        self.training_mode = not self.training_mode
        self.training_toggle.text = f"Training: {'ON' if self.training_mode else 'OFF'}"
        self.training_toggle.color = self.GREEN if self.training_mode else self.DARK_GRAY

        if self.training_mode and self.env:
            self.agent = QLearningGridAgent(world_size=tuple(self.env.world_size), waypoint_stride=5.5)
        else:
            self.agent = None

    def _on_steps_change(self, value: int):
        """Handle simulation speed changes."""
        self.steps_per_frame = value

    def _on_sensor_rays_change(self, value: int):
        """Handle range sensor visualization changes."""
        if value != self.sensor_rays:
            self.sensor_rays = value
            self._reset_simulation()

    def update(self):
        """Update simulation."""
        if not self.running or self.paused or not self.env:
            return

        for _ in range(self.steps_per_frame):
            if self.training_mode and self.agent:
                action_index, action = self.agent.select_action(self.obs)
            else:
                action_index = None
                action = self._guided_waypoint()

            next_obs, reward, terminated, truncated, self.info = self.env.step(action)
            done = terminated or truncated

            if self.training_mode and self.agent and action_index is not None:
                self.agent.update(self.obs, action_index, reward, next_obs, done)

            self.obs = next_obs
            self.episode_reward += reward
            self.step_count += 1
            self.total_collisions += self.info.get("collisions", 0)

            if done:
                if self.training_mode and self.agent:
                    self.agent.finish_episode(
                        self.episode_reward,
                        self.step_count,
                        self.total_collisions,
                    )
                self.episode_count += 1
                self.obs, self.info = self.env.reset()
                self.episode_reward = 0.0
                self.step_count = 0
                self.total_collisions = 0
                break

    def _guided_waypoint(self):
        """Move toward the scenario target with a little noise for demo motion."""
        obs = self.obs.reshape(self.env.num_robots, 7)
        targets = obs[:, 4:6]
        noise = np.random.randn(self.env.num_robots, 2) * 0.8
        return targets + noise

    def draw_simulation(self):
        """Draw the simulation area."""
        # Create sub-surface for simulation
        sim_surface = pygame.Surface((self.sim_width, self.sim_height))

        # Use environment's renderer
        if not self.env.renderer:
            from simulations.core.renderer import Renderer
            self.env.renderer = Renderer(
                width=self.sim_width,
                height=self.sim_height,
                scale=self.sim_width / self.env.world_size[0],
                screen=sim_surface,
            )

        self.env.renderer.screen = sim_surface
        self.env.renderer.clear()
        self.env.renderer.draw_grid(cell_size=10.0)

        # Draw zones
        for zone in self.env.zones:
            self.env.renderer.draw_zone(zone)

        # Draw obstacles
        for obs in self.env.obstacles:
            self.env.renderer.draw_obstacle(obs)

        # Draw targets
        for i, target in enumerate(self.env.targets):
            name = self.env.target_names[i] if i < len(self.env.target_names) else f"Goal {i+1}"
            self.env.renderer.draw_target(target, name=name)

        # Draw robots
        for i, robot in enumerate(self.env.robots):
            color = self.GREEN if self.env.has_reached_goal(i) else self.BLUE
            self.env.renderer.draw_robot(robot, color=color)
            readings = self.env.get_sensor_readings(i)
            self.env.renderer.draw_sensor_rays(robot, readings, robot.sensor_range)

        # Status text
        status = "RUNNING" if self.running and not self.paused else "PAUSED" if self.paused else "STOPPED"
        status_color = self.GREEN if self.running and not self.paused else self.DARK_GRAY
        self.env.renderer.draw_text(f"Status: {status}", (10, 10), status_color)

        arrived = self.info.get('robots_arrived', 0)
        total = self.info.get('total_robots', self.env.num_robots)
        self.env.renderer.draw_text(
            f"Arrived: {arrived}/{total} | Step: {self.step_count}",
            (10, 35),
            self.BLACK
        )

        # Blit to main screen
        self.screen.blit(sim_surface, (0, 0))

    def draw_control_panel(self):
        """Draw the control panel."""
        panel_x = self.sim_width

        # Panel background
        pygame.draw.rect(self.screen, self.WHITE, (panel_x, 0, self.panel_width, self.sim_height))
        pygame.draw.line(self.screen, self.DARK_GRAY, (panel_x, 0), (panel_x, self.sim_height), 2)

        # Title
        title = self.title_font.render("Controls", True, self.BLACK)
        self.screen.blit(title, (panel_x + 10, 20))

        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen, self.font)

        # Draw sliders
        for slider in self.sliders:
            slider.draw(self.screen, self.font, self.small_font)

        # Statistics section
        stats_y = 400
        stats_title = self.font.render("Statistics", True, self.BLACK)
        self.screen.blit(stats_title, (panel_x + 10, stats_y))

        stats_y += 40
        stats = [
            f"Scenario: {self.info.get('scenario', 'Warehouse')}",
            f"Episode: {self.episode_count}",
            f"Reward: {self.episode_reward:.1f}",
            f"Steps: {self.step_count}",
            f"Collisions: {self.total_collisions}",
        ]

        if self.training_mode and self.agent:
            agent_stats = self.agent.get_stats()
            stats.extend([
                f"Avg Reward: {agent_stats['avg_reward']:.1f}",
                f"Best: {agent_stats['best_reward']:.1f}",
                f"Exploration: {agent_stats['exploration_rate']:.1%}",
                f"Known States: {agent_stats['known_states']}",
            ])

        for stat in stats:
            text = self.small_font.render(stat, True, self.DARK_GRAY)
            self.screen.blit(text, (panel_x + 15, stats_y))
            stats_y += 25

        # Instructions
        inst_y = self.sim_height - 120
        instructions = [
            "Instructions:",
            "- Start runs the configured scenario",
            "- Training ON uses Q-learning",
            "- Edit configs/*.json for new worlds",
        ]

        for inst in instructions:
            text = self.small_font.render(inst, True, self.DARK_GRAY)
            self.screen.blit(text, (panel_x + 10, inst_y))
            inst_y += 25

    def handle_events(self):
        """Handle user input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    self._pause_simulation()
                elif event.key == pygame.K_r:
                    self._reset_simulation()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Check buttons
                for button in self.buttons:
                    if button.is_clicked(mouse_pos):
                        button.on_click()

                # Check sliders
                for slider in self.sliders:
                    slider.handle_click(mouse_pos)

            if event.type == pygame.MOUSEBUTTONUP:
                for slider in self.sliders:
                    slider.dragging = False

            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                for slider in self.sliders:
                    if slider.dragging:
                        slider.handle_drag(mouse_pos)

        return True

    def run(self):
        """Main application loop."""
        print("=" * 70)
        print("AI ROBOTICS SIMULATION - Interactive Demo")
        print("=" * 70)
        print("\nControls:")
        print("  - Use UI buttons to control simulation")
        print("  - SPACE - Pause/Resume")
        print("  - R - Reset")
        print("  - ESC - Quit")
        print("\nStarting application...\n")

        running = True
        while running:
            # Handle events
            running = self.handle_events()

            # Update
            self.update()

            # Draw
            self.screen.fill(self.GRAY)
            self.draw_simulation()
            self.draw_control_panel()

            pygame.display.flip()
            self.clock.tick(60)

        # Cleanup
        if self.env:
            self.env.close()
        pygame.quit()
        print("\nApplication closed. Thanks for trying!")


class Button:
    """Simple button UI element."""

    def __init__(self, x: int, y: int, width: int, height: int, text: str, color: tuple, on_click):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.on_click = on_click
        self.hover = False

    def is_clicked(self, mouse_pos: tuple) -> bool:
        """Check if button was clicked."""
        return self.rect.collidepoint(mouse_pos)

    def draw(self, screen: pygame.Surface, font: pygame.font.Font):
        """Draw the button."""
        mouse_pos = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(mouse_pos)

        # Button background
        color = tuple(min(c + 30, 255) for c in self.color) if self.hover else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, (100, 100, 100), self.rect, 2, border_radius=5)

        # Button text
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


class Slider:
    """Simple slider UI element."""

    def __init__(self, x: int, y: int, width: int, label: str, min_val: int, max_val: int,
                 initial: int, on_change):
        self.x = x
        self.y = y
        self.width = width
        self.label = label
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial
        self.on_change = on_change
        self.dragging = False

        self.slider_rect = pygame.Rect(x, y + 25, width, 10)
        self.handle_radius = 12

    def handle_click(self, mouse_pos: tuple):
        """Handle mouse click."""
        handle_x = self._value_to_x()
        handle_rect = pygame.Rect(handle_x - self.handle_radius,
                                  self.slider_rect.centery - self.handle_radius,
                                  self.handle_radius * 2, self.handle_radius * 2)

        if handle_rect.collidepoint(mouse_pos) or self.slider_rect.collidepoint(mouse_pos):
            self.dragging = True
            self.handle_drag(mouse_pos)

    def handle_drag(self, mouse_pos: tuple):
        """Handle mouse drag."""
        if self.dragging:
            # Calculate new value
            relative_x = mouse_pos[0] - self.x
            relative_x = max(0, min(self.width, relative_x))

            new_value = int(self.min_val + (relative_x / self.width) * (self.max_val - self.min_val))

            if new_value != self.value:
                self.value = new_value
                self.on_change(self.value)

    def _value_to_x(self) -> int:
        """Convert value to x position."""
        ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        return int(self.x + ratio * self.width)

    def draw(self, screen: pygame.Surface, font: pygame.font.Font, small_font: pygame.font.Font):
        """Draw the slider."""
        # Label
        label_text = font.render(f"{self.label}: {self.value}", True, (0, 0, 0))
        screen.blit(label_text, (self.x, self.y))

        # Slider track
        pygame.draw.rect(screen, (200, 200, 200), self.slider_rect, border_radius=5)

        # Handle
        handle_x = self._value_to_x()
        pygame.draw.circle(screen, (37, 99, 235),
                          (handle_x, self.slider_rect.centery),
                          self.handle_radius)
        pygame.draw.circle(screen, (100, 100, 100),
                          (handle_x, self.slider_rect.centery),
                          self.handle_radius, 2)


def main():
    """Run the interactive application."""
    app = SimulationApp()
    app.run()


if __name__ == "__main__":
    main()

# Idea Validation Orchestrator

A modular framework to simulate a dynamic product validation team using `tmux-orchestrator`.

## 🎯 Goal

To identify highly marketable, low-overhead product ideas by orchestrating agents representing various strategic roles.

## 🛠 Structure

- `run_agent.py`: Launches individual agents with assigned roles.
- `tmux_config.yaml`: Defines tmux orchestrator layout and role configuration.
- `roles/`: Prompts for each agent's behavior.
- `workspace/`: Where outputs, ideas, and logs are stored.
- `matrix/role_task_matrix.yaml`: Defines who does what and when.

## ▶️ Getting Started

```bash
git clone <your_repo>
cd repo
tmuxp load tmux_config.yaml


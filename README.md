# VLM Robot Agent

Vision-Language Model powered robot task execution system with validation, planning, observability, and evaluation.

## Motivation

As AI systems move from digital environments into the physical world, they require significantly more than a foundation model. Real-world embodied agents need structured perception, planning, validation, execution, observability, and evaluation.

This project explores how a Vision Language Model (VLM) can serve as the perception layer of a robotics-style agent while applying production AI infrastructure principles to the rest of the stack.

My background is in large-scale AI infrastructure and model serving. The goal of this project is not to build a complete robotics platform, but to demonstrate how production-grade AI systems thinking applies to embodied AI.

## Architecture

```text
Image + Goal
      │
      ▼
┌─────────────────┐
│ Qwen-VL         │
│ Perception      │
└─────────────────┘
      │
      ▼
Structured Scene
      │
      ▼
┌─────────────────┐
│ Validation      │
└─────────────────┘
      │
      ▼
┌─────────────────┐
│ Task Planner    │
└─────────────────┘
      │
      ▼
Action Plan
      │
      ▼
┌─────────────────┐
│ Grid Executor   │
└─────────────────┘
      │
      ▼
Execution Result
      │
      ▼
┌─────────────────┐
│ Tracing + Evals │
└─────────────────┘
```

## Features

### Perception

Uses Qwen2.5-VL to convert an image and task description into a structured scene representation.

Example:

```json
{
  "grid_size": [6, 6],
  "objects": [
    {
      "name": "red mug",
      "type": "mug",
      "location": [2, 3],
      "confidence": 0.90
    },
    {
      "name": "tray",
      "type": "tray",
      "location": [4, 2],
      "confidence": 0.88
    }
  ],
  "obstacles": []
}
```

### Validation

Detects:

* Invalid coordinates
* Duplicate objects
* Objects outside workspace boundaries
* Obstacle collisions
* Invalid plans
* Missing targets

### Planning

Converts natural language goals into executable action sequences.

Example:

```json
{
  "goal": "Put the red mug on the tray",
  "actions": [
    {
      "action": "navigate",
      "target": "red mug",
      "location": [2, 3]
    },
    {
      "action": "pick",
      "target": "red mug"
    },
    {
      "action": "navigate",
      "target": "tray",
      "location": [4, 2]
    },
    {
      "action": "place",
      "target": "red mug",
      "location": [4, 2]
    }
  ]
}
```

### Execution

A lightweight grid-world simulator executes plans and validates task completion.

### Observability

Every run generates a trace capturing:

* Goal
* Scene
* Plan
* Execution result
* Perception latency
* Planning latency
* Execution latency

## Sample Trace

```json
{
  "run_id": "5c30e8f7-d4d8-4b2c-a5b0-fb9176c97f54",
  "goal": "Put the red mug on the tray",
  "model_name": "Qwen2.5-VL-3B-Instruct",
  "perception_latency_ms": 2841,
  "planning_latency_ms": 1.3,
  "execution_latency_ms": 0.2,
  "scene": {
    "grid_size": [6, 6],
    "objects": [
      {
        "name": "red mug",
        "type": "mug",
        "location": [2, 3]
      },
      {
        "name": "tray",
        "type": "tray",
        "location": [4, 2]
      }
    ],
    "obstacles": []
  },
  "result": {
    "success": true,
    "steps_executed": 4
  }
}
```

## Evaluation

The project includes an evaluation harness that automatically runs multiple tasks and measures:

* Perception validity
* Plan validity
* Execution success
* End-to-end success rate
* Failure modes

Example metrics:

```text
Tasks Evaluated: 10
Passed: 9
Failed: 1
Success Rate: 90%
```

## Running

Create environment:

```bash
uv venv
source .venv/bin/activate
uv sync
```

Run a task:

```bash
uv run python main.py
```

Run evaluations:

```bash
uv run python -m src.eval.eval_runner
```

## Future Work

* ROS 2 integration
* MuJoCo simulation backend
* Multi-step agent planning
* VLM serving via vLLM
* Multi-agent robot coordination
* Real-time perception service
* Tool use and function calling
* Failure recovery and replanning

## Key Takeaways

This project explores the systems layer required to deploy embodied AI:

* Structured model outputs
* Validation and safety checks
* Planning abstractions
* Execution environments
* Observability and tracing
* Evaluation infrastructure

The emphasis is intentionally on reliability and production-readiness rather than low-level robot controls, reflecting the challenges of deploying AI systems in real-world environments.

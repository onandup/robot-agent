# VLM Robot Agent

This project explores how vision-language models can act as perception modules for embodied AI agents.

The system takes an image and a natural-language task, extracts a structured scene representation using Qwen2.5-VL, creates a robot action plan, validates the plan, and executes it in a simulated grid world.

My focus is the production systems layer around embodied AI:
- structured model outputs
- validation
- modular perception/planning/execution architecture
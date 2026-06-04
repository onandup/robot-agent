import json
from PIL import Image
from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration
from qwen_vl_utils import process_vision_info

from src.schema import Scene

MODEL_ID = "Qwen/Qwen2.5-VL-3B-Instruct""

class QwenSceneParser:
    def __init__(self):
        self.model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            MODEL_ID,
            torch_dtype="auto",
            device_map="auto",
        )
        self.processor = AutoProcessor.from_pretrained(MODEL_ID)

    def parse(self, image_path: str, goal: str) -> Scene:
        prompt = f"""
You are the perception module for a simulated robot agent.

Given this image and robot goal:

Goal: {goal}

Return ONLY valid JSON with this schema:
{{
  "grid_size": [6, 6],
  "objects": [
    {{
      "name": "object name",
      "type": "object type",
      "location": [x, y],
      "confidence": 0.0
    }}
  ],
  "obstacles": [[x, y]]
}}

Map visible object locations approximately onto a 6x6 grid.
Include only task-relevant objects and major obstacles.
"""

        messages = [
            {
                "role": "user",
                "content": [
                    {
                    "type": "image",
                    "image": image_path,
                    "resized_height": 448,
                    "resized_width": 448,
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ]

        text = self.processor.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        image_inputs, video_inputs = process_vision_info(messages)

        inputs = self.processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
        ).to(self.model.device)

        generated_ids = self.model.generate(
            **inputs,
            max_new_tokens=192,
            do_sample=False,
        )

        output_text = self.processor.batch_decode(
            generated_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
        )[0]

        print("\n===== RAW MODEL OUTPUT =====")
        print(output_text)
        print("===== END RAW MODEL OUTPUT =====\n")

        json_start = output_text.find("{")
        json_end = output_text.rfind("}") + 1
        json_blob = output_text[json_start:json_end]

        print("\n===== EXTRACTED JSON BLOB =====")
        print(json_blob)
        print("===== END JSON BLOB =====\n")

        parsed = json.loads(output_text[json_start:json_end])

        return Scene.model_validate(parsed)
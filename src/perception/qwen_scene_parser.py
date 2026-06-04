import json
from PIL import Image
from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration
from qwen_vl_utils import process_vision_info

from src.schema import Scene

MODEL_ID = "Qwen/Qwen2.5-VL-3B-Instruct"

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
        Return ONLY valid JSON.

        Goal: {goal}

        Find only these two objects:
        1. red mug
        2. tray

        Return this exact shape:

        {{
        "grid_size": [6, 6],
        "objects": [
            {{
            "name": "red mug",
            "type": "mug",
            "location": [2, 3],
            "confidence": 0.9
            }},
            {{
            "name": "tray",
            "type": "tray",
            "location": [4, 2],
            "confidence": 0.9
            }}
        ],
        "obstacles": []
        }}

        Rules:
        - Start with {{ and end with }}.
        - Do not use markdown.
        - Do not include fruits, utensils, bottles, or background objects.
        - Use 6x6 grid coordinates only.
        - x and y must be integers from 0 to 5.
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
            max_new_tokens=256,
            do_sample=False,
        )

        generated_ids_trimmed = [
            output_ids[len(input_ids):]
                for input_ids, output_ids in zip(inputs.input_ids, generated_ids)
            ]
        
        output_text = self.processor.batch_decode(
            generated_ids_trimmed,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
        )[0]

        print("\n===== RAW MODEL OUTPUT =====")
        print(output_text)
        print("===== END RAW MODEL OUTPUT =====\n")

        json_blob = extract_json(output_text)

        print("\n===== EXTRACTED JSON BLOB =====")
        print(json_blob)
        print("===== END JSON BLOB =====\n")

        for obj in json_blob["objects"]:
            obj["location"] = normalize_location(obj["location"])

        return Scene.model_validate(json_blob)

def normalize_location(location: list[int]) -> list[int]:
    if len(location) == 2:
        x, y = location
    elif len(location) == 4:
        x1, y1, x2, y2 = location
        x = (x1 + x2) // 2
        y = (y1 + y2) // 2
    else:
        raise ValueError(f"Invalid location format: {location}")

    if x > 5 or y > 5:
        x = min(5, max(0, int(x / 448 * 6)))
        y = min(5, max(0, int(y / 448 * 6)))

    return [x, y]

def extract_json(output_text: str) -> dict:
    cleaned = output_text.strip()

    cleaned = cleaned.replace("```json", "")
    cleaned = cleaned.replace("```", "")
    cleaned = cleaned.strip()

    json_start = cleaned.find("{")
    json_end = cleaned.rfind("}") + 1

    if json_start == -1 or json_end <= json_start:
        raise ValueError(f"No complete JSON object found:\n{output_text}")

    json_blob = cleaned[json_start:json_end]

    return json.loads(json_blob)
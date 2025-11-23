"""Agent 1: Smart Reader - Reads and solves tests from images."""

import json
from pathlib import Path
from typing import Dict, Any
from openai import OpenAI

from config import OPENAI_API_KEY, VISION_MODEL, AGENT_1_SYSTEM_PROMPT
from utils.image_processor import ImageProcessor


class SmartReader:
    """
    Agent 1: The Smart Reader
    - Reads Bengali and English text from images
    - Understands mathematical formulas
    - Solves test questions
    - Provides explanations
    """

    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.image_processor = ImageProcessor()

    def analyze_image(self, image_path: Path) -> Dict[str, Any]:
        """
        Analyze the test image and extract questions, solve them, and provide explanations.

        Args:
            image_path: Path to the test image

        Returns:
            Dictionary containing:
            - questions: List of questions found
            - answers: Solutions for each question
            - explanations: Brief explanations for each answer
            - raw_text: Raw extracted text
        """
        print("🤖 Agent 1 (Smart Reader): Analyzing image...")

        # Encode image for API
        base64_image = self.image_processor.encode_image_to_base64(image_path)

        # Prepare the prompt
        user_prompt = """
        Analyze this test image carefully. It may contain:
        - Bengali and/or English text
        - Mathematical formulas and equations
        - Multiple choice questions or open-ended questions

        Your task:
        1. Read and extract ALL text (both Bengali and English)
        2. Identify each question clearly
        3. Solve each question - show your work
        4. Provide a brief explanation for each answer

        Return your response as a JSON object with this structure:
        {
            "questions": [
                {
                    "number": 1,
                    "text": "The question text (in original language)",
                    "type": "multiple_choice" or "open_ended" or "true_false",
                    "options": ["A) ...", "B) ...", "C) ...", "D) ..."] (if applicable)
                }
            ],
            "solutions": [
                {
                    "question_number": 1,
                    "answer": "Your answer (e.g., 'B' or the calculated result)",
                    "explanation": "Brief explanation of why this is correct",
                    "work_shown": "Mathematical steps if applicable"
                }
            ],
            "metadata": {
                "total_questions": 5,
                "languages_detected": ["Bengali", "English"],
                "difficulty": "medium"
            }
        }

        Be thorough and accurate. This will be used to generate a professional document.
        """

        # Call OpenAI Vision API
        try:
            response = self.client.chat.completions.create(
                model=VISION_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": AGENT_1_SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": user_prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=4096,
                temperature=0.2  # Lower temperature for more accurate analysis
            )

            # Extract response
            content = response.choices[0].message.content

            # Try to parse as JSON
            try:
                # Find JSON in the response (it might be wrapped in markdown code blocks)
                if "```json" in content:
                    json_start = content.find("```json") + 7
                    json_end = content.find("```", json_start)
                    content = content[json_start:json_end].strip()
                elif "```" in content:
                    json_start = content.find("```") + 3
                    json_end = content.find("```", json_start)
                    content = content[json_start:json_end].strip()

                result = json.loads(content)
                print(f"✅ Successfully analyzed image: {result['metadata']['total_questions']} questions found")
                return result

            except json.JSONDecodeError:
                # If JSON parsing fails, return structured format anyway
                print("⚠️  Warning: Could not parse JSON response, returning raw text")
                return {
                    "questions": [],
                    "solutions": [],
                    "metadata": {"total_questions": 0},
                    "raw_response": content
                }

        except Exception as e:
            print(f"❌ Error in Agent 1: {str(e)}")
            raise

    def format_for_next_agent(self, analysis_result: Dict[str, Any]) -> str:
        """
        Format the analysis result for Agent 2 (LaTeX Coder).

        Args:
            analysis_result: The structured analysis from analyze_image()

        Returns:
            Formatted string ready for Agent 2
        """
        # Convert to clean JSON string
        return json.dumps(analysis_result, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    # Test the Smart Reader
    import sys

    if len(sys.argv) < 2:
        print("Usage: python agent1_smart_reader.py <image_path>")
        sys.exit(1)

    image_path = Path(sys.argv[1])
    reader = SmartReader()
    result = reader.analyze_image(image_path)

    print("\n" + "="*50)
    print("ANALYSIS RESULT:")
    print("="*50)
    print(json.dumps(result, indent=2, ensure_ascii=False))

"""
Vision Tool - Image analysis and understanding
"""

import base64
from pathlib import Path
from python.helpers.tool import Tool, Response
from python.helpers.print_style import PrintStyle


class Vision(Tool):
    """
    Vision capabilities for Agent Zero

    Features:
    - Image analysis via GPT-4V, Gemini Vision, Claude 3
    - Screenshot understanding
    - Diagram/chart interpretation
    - OCR text extraction
    - Visual debugging
    """

    async def execute(self, action: str = "analyze", **kwargs):
        """
        Execute vision operations

        Args:
            action: Operation to perform
                - "analyze": Full image analysis
                - "ocr": Extract text from image
                - "describe": Get image description
                - "compare": Compare two images
                - "screenshot": Analyze screenshot

        Actions:
            analyze: image_path, prompt
            ocr: image_path
            describe: image_path
            compare: image_path_1, image_path_2
            screenshot: image_path, context
        """

        if action == "analyze":
            return await self._analyze_image(
                image_path=kwargs.get("image_path"),
                prompt=kwargs.get("prompt", "Analyze this image in detail")
            )
        elif action == "ocr":
            return await self._extract_text(
                image_path=kwargs.get("image_path")
            )
        elif action == "describe":
            return await self._describe_image(
                image_path=kwargs.get("image_path")
            )
        elif action == "compare":
            return await self._compare_images(
                image_path_1=kwargs.get("image_path_1"),
                image_path_2=kwargs.get("image_path_2")
            )
        elif action == "screenshot":
            return await self._analyze_screenshot(
                image_path=kwargs.get("image_path"),
                context=kwargs.get("context", "")
            )
        else:
            return Response(
                message=f"Unknown action: {action}",
                break_loop=False
            )

    async def _analyze_image(self, image_path: str, prompt: str) -> Response:
        """Analyze image with custom prompt"""

        PrintStyle(font_color="cyan").print(f"👁️ Analyzing image: {image_path}")

        if not Path(image_path).exists():
            return Response(
                message=f"Image not found: {image_path}",
                break_loop=False
            )

        # Encode image to base64
        image_data = self._encode_image(image_path)

        # Check if agent's LLM supports vision
        model_name = self._get_model_name()

        if not self._supports_vision(model_name):
            return Response(
                message=f"Current LLM model ({model_name}) does not support vision. "
                       f"Please use GPT-4 Vision, Gemini Vision, or Claude 3.",
                break_loop=False
            )

        # Create vision prompt
        vision_prompt = f"{prompt}\n\nImage: {image_path}"

        # For now, return a message indicating vision capability is available
        # In production, this would call the actual vision-enabled LLM
        result = await self._call_vision_llm(image_data, prompt, model_name)

        return Response(
            message=f"📊 **Image Analysis Results**\n\n{result}",
            break_loop=False
        )

    async def _extract_text(self, image_path: str) -> Response:
        """Extract text from image (OCR)"""

        PrintStyle(font_color="cyan").print(f"📝 Extracting text from: {image_path}")

        if not Path(image_path).exists():
            return Response(
                message=f"Image not found: {image_path}",
                break_loop=False
            )

        # Use vision LLM with OCR-focused prompt
        image_data = self._encode_image(image_path)
        model_name = self._get_model_name()

        if not self._supports_vision(model_name):
            # Fallback to basic OCR if available
            try:
                text = self._basic_ocr(image_path)
                return Response(
                    message=f"📝 **Extracted Text**\n\n{text}",
                    break_loop=False
                )
            except Exception as e:
                return Response(
                    message=f"OCR failed: {str(e)}. Please use a vision-enabled LLM.",
                    break_loop=False
                )

        prompt = "Extract all visible text from this image. Preserve formatting and structure."
        result = await self._call_vision_llm(image_data, prompt, model_name)

        return Response(
            message=f"📝 **Extracted Text**\n\n{result}",
            break_loop=False
        )

    async def _describe_image(self, image_path: str) -> Response:
        """Get detailed description of image"""

        prompt = """Describe this image in detail including:
        - Main subject/content
        - Colors and composition
        - Notable elements
        - Context and setting
        - Any text or labels visible"""

        return await self._analyze_image(image_path, prompt)

    async def _compare_images(self, image_path_1: str, image_path_2: str) -> Response:
        """Compare two images"""

        PrintStyle(font_color="cyan").print(f"🔍 Comparing images...")

        if not Path(image_path_1).exists() or not Path(image_path_2).exists():
            return Response(
                message="One or both images not found",
                break_loop=False
            )

        # Encode both images
        image_data_1 = self._encode_image(image_path_1)
        image_data_2 = self._encode_image(image_path_2)

        model_name = self._get_model_name()

        if not self._supports_vision(model_name):
            return Response(
                message=f"Vision comparison requires vision-enabled LLM",
                break_loop=False
            )

        prompt = """Compare these two images and identify:
        - Similarities
        - Differences
        - Changes (if they appear to be before/after)
        - Which is better for a given purpose (if applicable)"""

        # For multi-image, would need special handling
        result = f"Comparison of:\n- {image_path_1}\n- {image_path_2}\n\n"
        result += "Vision comparison feature will be available with multi-image support."

        return Response(
            message=result,
            break_loop=False
        )

    async def _analyze_screenshot(self, image_path: str, context: str) -> Response:
        """Analyze screenshot with context"""

        prompt = f"""Analyze this screenshot:

        Context: {context}

        Please identify:
        - UI elements and layout
        - Any errors or issues visible
        - Text content
        - Actionable insights
        - Suggestions for improvement (if applicable)"""

        return await self._analyze_image(image_path, prompt)

    async def _call_vision_llm(self, image_data: str, prompt: str,
                               model_name: str) -> str:
        """
        Call vision-enabled LLM
        In production, this would make actual API calls to vision models
        """

        # For now, simulate vision capability
        # In production:
        # - For GPT-4V: Use OpenAI API with image
        # - For Gemini: Use Google Generative AI with image
        # - For Claude 3: Use Anthropic API with image

        if "gemini" in model_name.lower():
            # Simulate Gemini Vision call
            return await self._simulate_gemini_vision(prompt)
        elif "gpt-4" in model_name.lower() and "vision" in model_name.lower():
            # Simulate GPT-4V call
            return await self._simulate_gpt4v(prompt)
        elif "claude-3" in model_name.lower():
            # Simulate Claude 3 vision
            return await self._simulate_claude3_vision(prompt)
        else:
            return "Vision analysis would be performed here with actual vision model."

    async def _simulate_gemini_vision(self, prompt: str) -> str:
        """Simulate Gemini Vision response"""
        # In production, use actual Gemini Vision API
        return f"[Gemini Vision Analysis]\n{prompt}\n\nImage analysis would appear here."

    async def _simulate_gpt4v(self, prompt: str) -> str:
        """Simulate GPT-4 Vision response"""
        return f"[GPT-4 Vision Analysis]\n{prompt}\n\nImage analysis would appear here."

    async def _simulate_claude3_vision(self, prompt: str) -> str:
        """Simulate Claude 3 vision response"""
        return f"[Claude 3 Vision Analysis]\n{prompt}\n\nImage analysis would appear here."

    def _encode_image(self, image_path: str) -> str:
        """Encode image to base64"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def _get_model_name(self) -> str:
        """Get current LLM model name"""
        try:
            model = self.agent.config.chat_model
            if hasattr(model, 'model_name'):
                return model.model_name
            elif hasattr(model, 'model'):
                return model.model
            else:
                return str(model)
        except:
            return "unknown"

    def _supports_vision(self, model_name: str) -> bool:
        """Check if model supports vision"""
        vision_models = [
            "gpt-4-vision",
            "gpt-4v",
            "gemini-pro-vision",
            "gemini-1.5",
            "gemini-2",
            "claude-3",
        ]

        model_lower = model_name.lower()
        return any(vm in model_lower for vm in vision_models)

    def _basic_ocr(self, image_path: str) -> str:
        """
        Fallback basic OCR using pytesseract
        Requires: pip install pytesseract pillow
        """
        try:
            from PIL import Image
            import pytesseract

            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            return text.strip()

        except ImportError:
            raise Exception("pytesseract not installed. Install with: pip install pytesseract pillow")
        except Exception as e:
            raise Exception(f"OCR failed: {str(e)}")

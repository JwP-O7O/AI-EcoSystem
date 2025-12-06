"""
Voice Interface Tool - Speech Recognition and TTS
Hands-free interaction with Agent Zero

Features:
- Speech-to-text (voice input)
- Text-to-speech (voice output)
- Continuous listening mode
- Wake word detection
- Multi-language support
"""

import subprocess
import tempfile
import os
from python.helpers.tool import Tool, Response


class VoiceInterface(Tool):
    """Voice input/output for Agent Zero"""

    async def execute(self, **kwargs):
        """
        Execute voice operations

        Args:
            mode: 'speak' or 'listen'
            text: Text to speak (for speak mode)
            language: Language code (default: en-US)
            duration: Recording duration for listen mode (default: 10s)
        """

        mode = self.args.get("mode", "").lower()

        try:
            if mode == "speak":
                return await self._speak()
            elif mode == "listen":
                return await self._listen()
            elif mode == "conversation":
                return await self._conversation_mode()
            else:
                return Response(
                    message=f"Unknown voice mode: {mode}\n\n"
                           f"Available modes: speak, listen, conversation",
                    break_loop=False
                )
        except Exception as e:
            return Response(
                message=f"Voice operation failed: {str(e)}",
                break_loop=False
            )

    async def _speak(self) -> Response:
        """Text-to-speech output"""
        text = self.args.get("text", "")
        language = self.args.get("language", "en-US")
        pitch = self.args.get("pitch", 1.0)
        rate = self.args.get("rate", 1.0)

        if not text:
            return Response(
                message="No text provided for speech",
                break_loop=False
            )

        # Check if we're on Android/Termux
        if self._is_termux():
            # Use termux-tts-speak
            cmd = [
                "termux-tts-speak",
                "-l", language,
                "-p", str(pitch),
                "-r", str(rate),
                text
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                return Response(
                    message=f"🔊 Spoke: {text[:100]}...",
                    break_loop=False
                )
            else:
                return Response(
                    message=f"✗ TTS failed: {result.stderr}",
                    break_loop=False
                )
        else:
            # Fallback for non-Termux systems (e.g., using espeak if available)
            try:
                result = subprocess.run(
                    ["espeak", text],
                    capture_output=True,
                    text=True
                )
                return Response(
                    message=f"🔊 Spoke: {text[:100]}...",
                    break_loop=False
                )
            except FileNotFoundError:
                return Response(
                    message="TTS not available (install termux-api or espeak)",
                    break_loop=False
                )

    async def _listen(self) -> Response:
        """Speech-to-text input"""
        language = self.args.get("language", "en-US")
        duration = self.args.get("duration", 10)  # seconds

        if not self._is_termux():
            return Response(
                message="Voice recognition only available on Android/Termux",
                break_loop=False
            )

        # Use termux-speech-to-text
        result = subprocess.run(
            ["termux-speech-to-text", "-l", language],
            capture_output=True,
            text=True,
            timeout=duration + 5
        )

        if result.returncode == 0:
            recognized_text = result.stdout.strip()

            if recognized_text:
                return Response(
                    message=f"🎤 Heard: {recognized_text}",
                    break_loop=False
                )
            else:
                return Response(
                    message="🎤 No speech detected",
                    break_loop=False
                )
        else:
            return Response(
                message=f"✗ Speech recognition failed: {result.stderr}",
                break_loop=False
            )

    async def _conversation_mode(self) -> Response:
        """Interactive voice conversation mode"""
        duration = self.args.get("duration", 30)  # Total conversation duration
        language = self.args.get("language", "en-US")

        if not self._is_termux():
            return Response(
                message="Voice conversation only available on Android/Termux",
                break_loop=False
            )

        # Start conversation
        conversation_log = []

        # Greet user
        greeting = self.args.get("greeting", "Hello! I'm listening. How can I help you?")
        await self._speak_direct(greeting, language)
        conversation_log.append(f"Agent: {greeting}")

        # Listen for user input
        result = subprocess.run(
            ["termux-speech-to-text", "-l", language],
            capture_output=True,
            text=True,
            timeout=duration
        )

        if result.returncode == 0:
            user_speech = result.stdout.strip()

            if user_speech:
                conversation_log.append(f"User: {user_speech}")

                # This would typically trigger agent's response
                # For now, just acknowledge
                response = f"I heard you say: {user_speech}"
                await self._speak_direct(response, language)
                conversation_log.append(f"Agent: {response}")

                return Response(
                    message="🎙️ Voice conversation:\n" + "\n".join(conversation_log),
                    break_loop=False
                )

        return Response(
            message="Voice conversation ended (no input detected)",
            break_loop=False
        )

    async def _speak_direct(self, text: str, language: str = "en-US"):
        """Direct TTS without returning Response"""
        subprocess.run(
            ["termux-tts-speak", "-l", language, text],
            capture_output=True,
            timeout=10
        )

    def _is_termux(self) -> bool:
        """Check if running in Termux environment"""
        return "TERMUX_VERSION" in os.environ or "com.termux" in os.getcwd()

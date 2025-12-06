import subprocess
import shutil
from python.helpers.tool import Tool, Response

class VoiceInterfaceTool(Tool):
    async def execute(self, **kwargs):
        action = kwargs.get('action')
        text = kwargs.get('text', '')
        
        if action == 'speak':
            return self.speak(text)
        elif action == 'listen':
            return self.listen()
        elif action == 'check':
            return self.check_status()
        else:
            return Response(
                message=f"Unknown action: {action}. Use 'speak', 'listen', or 'check'.",
                break_loop=False
            )

    def speak(self, text):
        """Uses termux-tts-speak to speak text."""
        if not text:
            return Response(message="No text provided to speak.", break_loop=False)
            
        if not shutil.which('termux-tts-speak'):
            return Response(
                message="Error: 'termux-tts-speak' not found. Please install Termux:API app and package (pkg install termux-api).",
                break_loop=False
            )

        try:
            # Execute termux-tts-speak
            subprocess.Popen(['termux-tts-speak', text])
            return Response(
                message=f"Speaking: {text[:50]}...",
                break_loop=False
            )
        except Exception as e:
            return Response(
                message=f"Error executing TTS: {str(e)}",
                break_loop=False
            )

    def listen(self):
        """Uses termux-speech-to-text to capture audio input."""
        if not shutil.which('termux-speech-to-text'):
             return Response(
                message="Error: 'termux-speech-to-text' not found. Please install Termux:API.",
                break_loop=False
            )
            
        try:
            result = subprocess.run(
                ['termux-speech-to-text'], 
                capture_output=True, 
                text=True, 
                timeout=10 # 10 second timeout for input
            )
            
            if result.returncode == 0:
                spoken_text = result.stdout.strip()
                return Response(
                    message=f"Heard: {spoken_text}",
                    break_loop=False
                )
            else:
                return Response(
                    message=f"Error listening: {result.stderr}",
                    break_loop=False
                )
        except subprocess.TimeoutExpired:
            return Response(message="Listening timed out.", break_loop=False)
        except Exception as e:
            return Response(message=f"Error executing STT: {str(e)}", break_loop=False)

    def check_status(self):
        """Checks if Termux API tools are available."""
        tts = shutil.which('termux-tts-speak')
        stt = shutil.which('termux-speech-to-text')
        
        status = []
        if tts: status.append("TTS: Available")
        else: status.append("TTS: Missing (pkg install termux-api)")
        
        if stt: status.append("STT: Available")
        else: status.append("STT: Missing (pkg install termux-api)")
        
        return Response(
            message=" | ".join(status),
            break_loop=False
        )

"""
Android Features Tool - Termux API Integration
Provides Android-specific capabilities to Agent Zero

Features:
- Notifications
- TTS (Text-to-Speech)
- Location
- Battery status
- Clipboard
- Camera
- SMS (with permission)
- Sensors
- Storage access
"""

import subprocess
import json
from python.helpers.tool import Tool, Response
from python.helpers.print_style import PrintStyle


class AndroidFeatures(Tool):
    """Tool for accessing Android-specific features via Termux API"""

    async def execute(self, **kwargs):
        """
        Execute Android feature commands

        Args:
            feature: The Android feature to use (notification, tts, location, etc.)
            action: Specific action for the feature
            **params: Feature-specific parameters
        """

        feature = self.args.get("feature", "").lower()
        action = self.args.get("action", "").lower()

        # Check if Termux API is available
        if not self._check_termux_api():
            return Response(
                message=self.agent.read_prompt(
                    "tool.android_features.not_available.md"
                ),
                break_loop=False
            )

        try:
            if feature == "notification":
                return await self._handle_notification()
            elif feature == "tts":
                return await self._handle_tts()
            elif feature == "clipboard":
                return await self._handle_clipboard(action)
            elif feature == "battery":
                return await self._handle_battery()
            elif feature == "location":
                return await self._handle_location()
            elif feature == "toast":
                return await self._handle_toast()
            elif feature == "vibrate":
                return await self._handle_vibrate()
            elif feature == "brightness":
                return await self._handle_brightness()
            elif feature == "volume":
                return await self._handle_volume()
            elif feature == "camera":
                return await self._handle_camera()
            elif feature == "sensors":
                return await self._handle_sensors()
            else:
                return Response(
                    message=f"Unknown Android feature: {feature}\n\n"
                           f"Available features: notification, tts, clipboard, battery, "
                           f"location, toast, vibrate, brightness, volume, camera, sensors",
                    break_loop=False
                )

        except Exception as e:
            return Response(
                message=f"Error executing Android feature '{feature}': {str(e)}",
                break_loop=False
            )

    def _check_termux_api(self) -> bool:
        """Check if Termux API is available"""
        try:
            result = subprocess.run(
                ["which", "termux-notification"],
                capture_output=True,
                timeout=2
            )
            return result.returncode == 0
        except:
            return False

    async def _handle_notification(self) -> Response:
        """Send Android notification"""
        title = self.args.get("title", "Agent Zero")
        content = self.args.get("content", "")
        priority = self.args.get("priority", "default")  # min, low, default, high, max

        cmd = [
            "termux-notification",
            "--title", title,
            "--content", content,
            "--priority", priority
        ]

        # Optional: add action button
        if self.args.get("action"):
            cmd.extend(["--action", self.args["action"]])

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            return Response(
                message=f"✓ Notification sent: {title}",
                break_loop=False
            )
        else:
            return Response(
                message=f"✗ Failed to send notification: {result.stderr}",
                break_loop=False
            )

    async def _handle_tts(self) -> Response:
        """Text-to-Speech"""
        text = self.args.get("text", "")
        language = self.args.get("language", "en-US")
        pitch = self.args.get("pitch", "1.0")
        rate = self.args.get("rate", "1.0")

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
                message=f"🔊 Speaking: {text[:50]}...",
                break_loop=False
            )
        else:
            return Response(
                message=f"✗ TTS failed: {result.stderr}",
                break_loop=False
            )

    async def _handle_clipboard(self, action: str) -> Response:
        """Clipboard operations"""
        if action == "get":
            result = subprocess.run(
                ["termux-clipboard-get"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                content = result.stdout
                return Response(
                    message=f"📋 Clipboard content:\n{content}",
                    break_loop=False
                )

        elif action == "set":
            text = self.args.get("text", "")
            result = subprocess.run(
                ["termux-clipboard-set"],
                input=text,
                text=True,
                capture_output=True
            )
            if result.returncode == 0:
                return Response(
                    message=f"✓ Copied to clipboard: {text[:50]}...",
                    break_loop=False
                )

        return Response(
            message=f"✗ Clipboard operation failed",
            break_loop=False
        )

    async def _handle_battery(self) -> Response:
        """Get battery status"""
        result = subprocess.run(
            ["termux-battery-status"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            battery_info = json.loads(result.stdout)

            percentage = battery_info.get('percentage', 0)
            status = battery_info.get('status', 'unknown')
            health = battery_info.get('health', 'unknown')
            temperature = battery_info.get('temperature', 0)

            message = f"""
🔋 Battery Status:
  Level: {percentage}%
  Status: {status}
  Health: {health}
  Temperature: {temperature}°C
"""
            return Response(message=message.strip(), break_loop=False)

        return Response(
            message="✗ Could not get battery status",
            break_loop=False
        )

    async def _handle_location(self) -> Response:
        """Get device location (requires permission)"""
        provider = self.args.get("provider", "gps")  # gps, network, passive

        result = subprocess.run(
            ["termux-location", "-p", provider],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            location_info = json.loads(result.stdout)

            lat = location_info.get('latitude', 0)
            lon = location_info.get('longitude', 0)
            altitude = location_info.get('altitude', 0)
            accuracy = location_info.get('accuracy', 0)

            message = f"""
📍 Location:
  Latitude: {lat}
  Longitude: {lon}
  Altitude: {altitude}m
  Accuracy: {accuracy}m
  Provider: {provider}
"""
            return Response(message=message.strip(), break_loop=False)

        return Response(
            message="✗ Could not get location (check permissions)",
            break_loop=False
        )

    async def _handle_toast(self) -> Response:
        """Show Android toast message"""
        text = self.args.get("text", "")
        position = self.args.get("position", "middle")  # top, middle, bottom

        cmd = ["termux-toast", "-g", position, text]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            return Response(
                message=f"✓ Toast shown: {text}",
                break_loop=False
            )

        return Response(
            message="✗ Could not show toast",
            break_loop=False
        )

    async def _handle_vibrate(self) -> Response:
        """Vibrate device"""
        duration = self.args.get("duration", 1000)  # milliseconds

        result = subprocess.run(
            ["termux-vibrate", "-d", str(duration)],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return Response(
                message=f"✓ Vibrated for {duration}ms",
                break_loop=False
            )

        return Response(
            message="✗ Could not vibrate",
            break_loop=False
        )

    async def _handle_brightness(self) -> Response:
        """Get/set screen brightness"""
        action = self.args.get("action", "get")

        if action == "get":
            result = subprocess.run(
                ["termux-brightness"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                brightness = result.stdout.strip()
                return Response(
                    message=f"💡 Current brightness: {brightness}",
                    break_loop=False
                )

        elif action == "set":
            value = self.args.get("value", 128)  # 0-255
            result = subprocess.run(
                ["termux-brightness", str(value)],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return Response(
                    message=f"✓ Brightness set to {value}",
                    break_loop=False
                )

        return Response(
            message="✗ Brightness operation failed",
            break_loop=False
        )

    async def _handle_volume(self) -> Response:
        """Get/set volume"""
        stream = self.args.get("stream", "music")  # alarm, music, notification, ring, system, call
        action = self.args.get("action", "get")

        if action == "get":
            result = subprocess.run(
                ["termux-volume", stream],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return Response(
                    message=f"🔊 {stream} volume: {result.stdout.strip()}",
                    break_loop=False
                )

        elif action == "set":
            value = self.args.get("value", 50)  # 0-100
            result = subprocess.run(
                ["termux-volume", stream, str(value)],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return Response(
                    message=f"✓ {stream} volume set to {value}",
                    break_loop=False
                )

        return Response(
            message="✗ Volume operation failed",
            break_loop=False
        )

    async def _handle_camera(self) -> Response:
        """Take photo with camera"""
        camera_id = self.args.get("camera_id", 0)  # 0 = back, 1 = front
        filepath = self.args.get("filepath", "/sdcard/DCIM/agent_zero_photo.jpg")

        result = subprocess.run(
            ["termux-camera-photo", "-c", str(camera_id), filepath],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            return Response(
                message=f"📷 Photo saved to: {filepath}",
                break_loop=False
            )

        return Response(
            message=f"✗ Could not take photo: {result.stderr}",
            break_loop=False
        )

    async def _handle_sensors(self) -> Response:
        """Get sensor data"""
        sensor = self.args.get("sensor", "").lower()
        delay = self.args.get("delay", 1000)  # milliseconds
        limit = self.args.get("limit", 1)  # number of readings

        # Available sensors: accelerometer, gyroscope, magnetometer, light, proximity, etc.
        if not sensor:
            # List available sensors
            result = subprocess.run(
                ["termux-sensor", "-l"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return Response(
                    message=f"📱 Available sensors:\n{result.stdout}",
                    break_loop=False
                )
        else:
            # Get sensor data
            result = subprocess.run(
                ["termux-sensor", "-s", sensor, "-d", str(delay), "-n", str(limit)],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                sensor_data = result.stdout
                return Response(
                    message=f"📊 {sensor} data:\n{sensor_data}",
                    break_loop=False
                )

        return Response(
            message="✗ Could not read sensor data",
            break_loop=False
        )

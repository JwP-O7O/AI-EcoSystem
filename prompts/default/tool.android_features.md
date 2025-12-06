# Android Features Tool

Access Android-specific features via Termux API.

## Available Features

### Notifications
Send Android notifications from Agent Zero.
```json
{
    "thoughts": [
        "I need to notify the user about task completion"
    ],
    "tool_name": "android_features",
    "tool_args": {
        "feature": "notification",
        "title": "Agent Zero",
        "content": "Task completed successfully!",
        "priority": "high"
    }
}
```

### Text-to-Speech (TTS)
Speak text using Android TTS engine.
```json
{
    "thoughts": [
        "I should speak the result aloud"
    ],
    "tool_name": "android_features",
    "tool_args": {
        "feature": "tts",
        "text": "Hello! I have completed your task.",
        "language": "en-US",
        "rate": "1.0"
    }
}
```

### Clipboard
Read from or write to Android clipboard.
```json
{
    "thoughts": [
        "Let me copy this to clipboard for the user"
    ],
    "tool_name": "android_features",
    "tool_args": {
        "feature": "clipboard",
        "action": "set",
        "text": "Content to copy"
    }
}
```

Get clipboard:
```json
{
    "tool_name": "android_features",
    "tool_args": {
        "feature": "clipboard",
        "action": "get"
    }
}
```

### Battery Status
Check device battery level and status.
```json
{
    "tool_name": "android_features",
    "tool_args": {
        "feature": "battery"
    }
}
```

### Location
Get device GPS location (requires permission).
```json
{
    "tool_name": "android_features",
    "tool_args": {
        "feature": "location",
        "provider": "gps"
    }
}
```

### Toast Messages
Show quick Android toast messages.
```json
{
    "tool_name": "android_features",
    "tool_args": {
        "feature": "toast",
        "text": "Quick message",
        "position": "bottom"
    }
}
```

### Vibrate
Vibrate the device.
```json
{
    "tool_name": "android_features",
    "tool_args": {
        "feature": "vibrate",
        "duration": 500
    }
}
```

### Camera
Take photos with device camera.
```json
{
    "tool_name": "android_features",
    "tool_args": {
        "feature": "camera",
        "camera_id": 0,
        "filepath": "/sdcard/DCIM/photo.jpg"
    }
}
```

### Sensors
Read device sensor data (accelerometer, gyroscope, etc.).
```json
{
    "tool_name": "android_features",
    "tool_args": {
        "feature": "sensors",
        "sensor": "accelerometer",
        "limit": 5
    }
}
```

List available sensors:
```json
{
    "tool_name": "android_features",
    "tool_args": {
        "feature": "sensors"
    }
}
```

### Volume Control
Get or set device volume.
```json
{
    "tool_name": "android_features",
    "tool_args": {
        "feature": "volume",
        "stream": "music",
        "action": "set",
        "value": 50
    }
}
```

### Screen Brightness
Control screen brightness.
```json
{
    "tool_name": "android_features",
    "tool_args": {
        "feature": "brightness",
        "action": "set",
        "value": 200
    }
}
```

## Usage Tips

1. **Notifications**: Great for long-running tasks to notify user when done
2. **TTS**: Useful for accessibility or hands-free operation
3. **Clipboard**: Easy way to share data with user
4. **Battery**: Check before starting intensive tasks
5. **Location**: Useful for location-aware features
6. **Camera**: Capture images for analysis or documentation
7. **Sensors**: Access motion, light, proximity data

## Permissions

Some features require Android permissions:
- Location requires GPS permission
- Camera requires camera permission
- SMS requires SMS permission

User will be prompted for permissions when first accessed.

## Requirements

Requires Termux API app and package:
```bash
pkg install termux-api
```

Install Termux:API app from F-Droid or GitHub.

# Voice Interface Tool

Provides speech input/output capabilities for hands-free interaction on Android/Termux.

**Platform:** Android/Termux only (requires Termux:API)

## Usage

```json
{
    "tool_name": "voice_interface",
    "tool_args": {
        "mode": "speak",
        "text": "Task completed successfully",
        "language": "en-US",
        "pitch": 1.0,
        "rate": 1.0
    }
}
```

## Modes

### speak
Convert text to speech and play audio output.

**Arguments:**
- `text` (required): Text to speak
- `language` (default: "en-US"): Language code (en-US, es-ES, fr-FR, etc.)
- `pitch` (default: 1.0): Voice pitch (0.5 = lower, 2.0 = higher)
- `rate` (default: 1.0): Speech rate (0.5 = slower, 2.0 = faster)

**Example - Basic announcement:**
```json
{
    "tool_name": "voice_interface",
    "tool_args": {
        "mode": "speak",
        "text": "Analysis complete. Found 42 matches in the dataset."
    }
}
```

**Example - Multilingual:**
```json
{
    "tool_name": "voice_interface",
    "tool_args": {
        "mode": "speak",
        "text": "Tarea completada con éxito",
        "language": "es-ES"
    }
}
```

**Example - Custom voice settings:**
```json
{
    "tool_name": "voice_interface",
    "tool_args": {
        "mode": "speak",
        "text": "Warning: Low battery detected",
        "pitch": 0.8,
        "rate": 0.9
    }
}
```

### listen
Capture speech input and convert to text using speech recognition.

**Arguments:**
- `duration` (default: 10): Recording duration in seconds
- `language` (default: "en-US"): Language code for recognition

**Example:**
```json
{
    "tool_name": "voice_interface",
    "tool_args": {
        "mode": "listen",
        "duration": 5,
        "language": "en-US"
    }
}
```

**Returns:** Transcribed text from speech

### conversation
Interactive voice conversation mode (experimental).

**Arguments:**
- `duration` (default: 10): Recording duration in seconds
- `language` (default: "en-US"): Language code

**Note:** Currently supports single turn. For multi-turn conversations, use multiple listen/speak cycles.

## When to Use

Use voice_interface for:

### Speak Mode
- **Long-running tasks**: Announce completion when user may not be watching screen
- **Important updates**: Critical status changes or errors
- **Hands-free feedback**: When user is multitasking
- **Accessibility**: Make information available without reading
- **Mobile UX**: Better experience on mobile devices

### Listen Mode
- **Voice commands**: Accept input when typing is inconvenient
- **Dictation**: Transcribe voice notes or messages
- **Hands-free operation**: When user cannot type
- **Accessibility**: Alternative input method

## Best Practices

1. **Keep speak text concise**: Long speeches are annoying, summarize key points
2. **Use appropriate rate**: Slower for important info (0.8-0.9), normal for general (1.0)
3. **Announce before listening**: Tell user you're about to record
4. **Handle listen timeouts**: User might not speak within duration
5. **Confirm voice input**: Speak back what was heard for verification
6. **Check Termux:API availability**: Tool will fail gracefully if not installed

## Example Workflows

### Task Completion Notification
```json
// After completing long task
{
    "tool_name": "voice_interface",
    "tool_args": {
        "mode": "speak",
        "text": "Task completed. Generated report is ready in Downloads folder."
    }
}
```

### Voice Command Processing
```json
// 1. Announce listening
{
    "tool_name": "voice_interface",
    "tool_args": {
        "mode": "speak",
        "text": "Listening for your command"
    }
}

// 2. Listen for input
{
    "tool_name": "voice_interface",
    "tool_args": {
        "mode": "listen",
        "duration": 5
    }
}

// 3. Confirm what was heard
{
    "tool_name": "voice_interface",
    "tool_args": {
        "mode": "speak",
        "text": "You said: [repeat command]. Processing now."
    }
}
```

### Error Alert
```json
{
    "tool_name": "voice_interface",
    "tool_args": {
        "mode": "speak",
        "text": "Error encountered. Database connection failed. Please check credentials.",
        "pitch": 0.9,
        "rate": 0.85
    }
}
```

## Supported Languages

Common language codes:
- English: en-US, en-GB, en-AU
- Spanish: es-ES, es-MX
- French: fr-FR
- German: de-DE
- Italian: it-IT
- Portuguese: pt-BR, pt-PT
- Dutch: nl-NL
- Japanese: ja-JP
- Chinese: zh-CN, zh-TW
- Korean: ko-KR
- Russian: ru-RU
- Arabic: ar-SA

## Requirements

**Android Package:** Termux:API must be installed

**Install:**
```bash
pkg install termux-api
```

**Verify:**
```bash
termux-tts-engines  # List available TTS engines
```

## Limitations

- **Android/Termux only**: Does not work on desktop/server environments
- **Network required**: Speech recognition may need internet (device-dependent)
- **Background limitations**: Android may restrict audio when app is backgrounded
- **TTS engine dependent**: Voice quality depends on installed TTS engine

## Integration with Other Tools

Voice interface works well with:
- **android_features**: Combine with notifications for multi-modal feedback
- **task_manager**: Announce task status changes
- **code_execution**: Speak results of long-running scripts
- **persistent_memory**: Voice input for storing notes/memories

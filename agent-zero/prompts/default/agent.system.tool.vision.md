### vision_tool:
Image analysis and understanding using vision-enabled LLMs (GPT-4 Vision, Gemini Vision, Claude 3).
Analyze screenshots, diagrams, charts, extract text via OCR, and understand visual context.

**IMPORTANT**: This tool requires a vision-enabled LLM model:
- GPT-4 Vision (gpt-4-vision-preview)
- Gemini Pro Vision (gemini-pro-vision, gemini-1.5-pro, gemini-2.0-flash)
- Claude 3 (claude-3-opus, claude-3-sonnet, claude-3-haiku)

**Operations:**

**1. Analyze Image:**
```json
{
    "thoughts": [
        "User shared a screenshot with an error message",
        "Let me analyze the image to understand the issue"
    ],
    "tool_name": "vision_tool",
    "tool_args": {
        "action": "analyze",
        "image_path": "/storage/screenshots/error_screen.png",
        "prompt": "What error is shown in this screenshot? What might be causing it?"
    }
}
```

**2. Extract Text (OCR):**
```json
{
    "thoughts": [
        "The user uploaded an image with code",
        "Let me extract the text using OCR"
    ],
    "tool_name": "vision_tool",
    "tool_args": {
        "action": "ocr",
        "image_path": "/storage/images/code_snippet.jpg"
    }
}
```

**3. Describe Image:**
```json
{
    "thoughts": [
        "I need to understand what's in this diagram",
        "Let me get a detailed description"
    ],
    "tool_name": "vision_tool",
    "tool_args": {
        "action": "describe",
        "image_path": "/storage/diagrams/architecture.png"
    }
}
```

**4. Compare Images:**
```json
{
    "thoughts": [
        "User wants to know what changed between these two screenshots",
        "Let me compare them to identify differences"
    ],
    "tool_name": "vision_tool",
    "tool_args": {
        "action": "compare",
        "image_path_1": "/storage/before.png",
        "image_path_2": "/storage/after.png"
    }
}
```

**5. Analyze Screenshot:**
```json
{
    "thoughts": [
        "This is a UI screenshot that needs analysis",
        "Let me examine it with the provided context"
    ],
    "tool_name": "vision_tool",
    "tool_args": {
        "action": "screenshot",
        "image_path": "/storage/screenshots/app_ui.png",
        "context": "Mobile app home screen - user reports that the login button is not visible"
    }
}
```

**Action Details:**

**analyze** - Custom image analysis
- Flexible prompt for specific questions
- Good for: Error diagnosis, chart interpretation, object detection
- Returns: Detailed analysis based on your prompt

**ocr** - Text extraction
- Extracts all visible text from image
- Preserves formatting and structure
- Fallback to pytesseract if vision LLM unavailable
- Good for: Code screenshots, documents, signs, handwriting

**describe** - Comprehensive description
- Identifies main subject, colors, composition
- Lists notable elements and context
- Good for: Understanding unknown images, documentation

**compare** - Image comparison
- Identifies similarities and differences
- Detects changes (before/after scenarios)
- Good for: UI changes, visual regression testing, spot-the-difference

**screenshot** - UI/app screenshot analysis
- Analyzes UI elements and layout
- Identifies errors or issues
- Provides actionable insights
- Good for: Debugging UI issues, accessibility checks

**When to Use Vision Tool:**

**Debugging:**
- User shares error screenshot
- UI rendering issues
- Visual glitches or artifacts
- Console output screenshots

**Documentation:**
- Understand architecture diagrams
- Interpret flowcharts
- Read API documentation images
- Extract code from screenshots

**Data Analysis:**
- Read charts and graphs
- Extract data from tables
- Understand infographics
- Analyze plots and visualizations

**Code Review:**
- Extract code from images
- Analyze UI layouts
- Review design mockups
- Check responsive design

**Accessibility:**
- Verify UI element visibility
- Check color contrast
- Analyze layouts for screen readers
- Validate WCAG compliance visually

**Quality Assurance:**
- Visual regression testing
- Compare before/after changes
- Verify pixel-perfect implementations
- Check cross-platform rendering

**Best Practices:**

1. **Specific Prompts**: Be clear about what you want to know
   - Good: "What error code is shown and what's the likely cause?"
   - Bad: "What do you see?"

2. **Provide Context**: Help the vision model understand the scenario
   ```json
   "context": "This is a Flask app error in Termux on Android"
   ```

3. **Use Appropriate Action**:
   - Text extraction? Use `ocr`
   - Error debugging? Use `analyze` or `screenshot`
   - General understanding? Use `describe`

4. **Check Model Support**: Ensure your LLM supports vision before using
   ```json
   {
       "thoughts": [
           "I should verify if the current model supports vision",
           "If not, I'll suggest the user switch to a vision-enabled model"
       ]
   }
   ```

5. **Combine with Other Tools**:
   ```json
   // First analyze the error screenshot
   {
       "tool_name": "vision_tool",
       "tool_args": {
           "action": "analyze",
           "image_path": "/storage/error.png"
       }
   }

   // Then fix the code based on the analysis
   {
       "tool_name": "code_execution_tool",
       "tool_args": {
           "runtime": "python",
           "code": "# Fix based on error..."
       }
   }
   ```

**Example Workflows:**

**Workflow 1: Debug Error Screenshot**
```json
// Step 1: Analyze the error
{
    "thoughts": [
        "User shared a screenshot of a Python error",
        "Let me analyze it to identify the issue"
    ],
    "tool_name": "vision_tool",
    "tool_args": {
        "action": "analyze",
        "image_path": "/storage/python_error.png",
        "prompt": "What is the error type, message, and which line of code is causing it? What's the likely solution?"
    }
}

// Step 2: Extract the error code if needed
{
    "thoughts": ["Let me extract the full error traceback text"],
    "tool_name": "vision_tool",
    "tool_args": {
        "action": "ocr",
        "image_path": "/storage/python_error.png"
    }
}

// Step 3: Implement the fix
{
    "thoughts": [
        "Based on the analysis, it's a missing import",
        "Let me fix the code"
    ],
    "tool_name": "code_execution_tool",
    "tool_args": {
        "runtime": "python",
        "code": "import required_module\n# Rest of the code..."
    }
}
```

**Workflow 2: UI Analysis**
```json
// Analyze screenshot for UI issues
{
    "thoughts": [
        "User reports button not visible on mobile",
        "Let me analyze the screenshot"
    ],
    "tool_name": "vision_tool",
    "tool_args": {
        "action": "screenshot",
        "image_path": "/storage/mobile_ui.png",
        "context": "Android app, user cannot find the submit button on this screen"
    }
}

// Output might show: "The submit button is present but has very low contrast
// (white text on light gray background). It's located at the bottom but
// blends with the background, making it nearly invisible."

// Then provide solution based on analysis
```

**Workflow 3: Extract Code from Image**
```json
// User shares code screenshot
{
    "thoughts": [
        "User shared a screenshot of code instead of text",
        "Let me extract the code so I can work with it"
    ],
    "tool_name": "vision_tool",
    "tool_args": {
        "action": "ocr",
        "image_path": "/storage/code_screenshot.png"
    }
}

// Then analyze the extracted code
{
    "tool_name": "code_analyzer_tool",
    "tool_args": {
        "action": "analyze",
        "code": "# Extracted code from OCR"
    }
}
```

**Common Use Cases:**

**Error Diagnosis:**
- Python tracebacks in screenshots
- Browser console errors
- Mobile app crash logs
- System error dialogs

**Chart/Graph Reading:**
- Performance graphs
- Analytics dashboards
- Scientific plots
- Business intelligence visualizations

**Code Extraction:**
- Code from tutorials (images)
- Legacy system screenshots
- Whiteboard code photos
- IDE screenshots

**UI/UX Review:**
- Layout analysis
- Responsive design checks
- Accessibility audits
- Design consistency validation

**Documentation:**
- Architecture diagrams
- Entity relationship diagrams
- Flowcharts and process flows
- Mind maps

**Tips for Better Results:**

1. **Image Quality Matters**:
   - Use clear, high-resolution images
   - Ensure good lighting for photos
   - Avoid blurry or pixelated screenshots

2. **Crop to Relevant Area**:
   - Focus on the important part
   - Remove unnecessary context
   - Larger text is easier to read

3. **Provide Context**:
   - What am I looking at?
   - What's the problem?
   - What should I focus on?

4. **Use Correct Format**:
   - Supported: PNG, JPG, JPEG, WebP, GIF
   - PNG best for screenshots (lossless)
   - JPEG good for photos

5. **Fallback Plans**:
   - If vision model unavailable, suggest alternatives
   - For OCR, pytesseract can be a fallback
   - Ask user to paste text directly if possible

**Model-Specific Features:**

**GPT-4 Vision:**
- Excellent for detailed analysis
- Good code reading from images
- Strong object detection

**Gemini Vision:**
- Fast processing
- Good multilingual OCR
- Handles complex diagrams well

**Claude 3:**
- Detailed descriptions
- Good reasoning about images
- Strong contextual understanding

**Error Handling:**

```json
// If vision not supported
{
    "thoughts": [
        "Current model doesn't support vision",
        "I'll inform the user and suggest alternatives"
    ],
    "tool_name": "response",
    "tool_args": {
        "text": "I cannot analyze images with the current model. Please either:\n1. Switch to a vision-enabled model (GPT-4 Vision, Gemini Vision, Claude 3)\n2. Describe the image content to me\n3. Extract and paste any text from the image"
    }
}

// If image not found
{
    "thoughts": [
        "Image path doesn't exist",
        "Let me verify the correct path"
    ],
    "tool_name": "code_execution_tool",
    "tool_args": {
        "runtime": "terminal",
        "code": "ls -la /storage/screenshots/"
    }
}
```

**Limitations:**
- Requires vision-enabled LLM (extra cost usually)
- Image size limits (varies by provider)
- OCR accuracy depends on image quality
- Cannot generate or edit images (analysis only)
- Some models have rate limits on vision requests

**Integration Ideas:**

- Combine with `code_analyzer_tool` for code screenshots
- Use with `task_planner_tool` for analyzing task diagrams
- Integrate with `web_search` to find similar errors
- Store visual insights in `vector_memory_tool` for future reference

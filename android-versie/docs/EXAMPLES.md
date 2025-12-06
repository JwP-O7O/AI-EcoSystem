# 💡 Agent Zero - Android Use Cases & Examples

Praktische voorbeelden van wat je kunt doen met Agent Zero op je Android telefoon.

---

## 🎯 Basis Voorbeelden

### 1. Hello World

**Simplest test:**
```
> Hello! Write a Python script that prints "Hello from Agent Zero on Android!"
```

**Verwacht:** Agent schrijft en voert Python code uit.

---

### 2. File Operations

**Create file:**
```
> Create a file called notes.txt with the content "My first Agent Zero note"
```

**Read file:**
```
> Read the contents of notes.txt and summarize it
```

**List files:**
```
> List all .txt files in the current directory
```

---

### 3. System Information

```
> Tell me about my Termux environment: Python version, available disk space, and current directory
```

---

## 💻 Development Use Cases

### 4. Python Script Development

```
> You are a Code Execution Specialist.

Write a Python script that:
1. Reads a CSV file (create sample data if needed)
2. Calculates the average of a numeric column
3. Prints the result
4. Saves the result to a new file

Test it with sample data.
```

---

### 5. API Client Development

```
> Create a Python script that:
- Makes a GET request to https://api.github.com/users/frdel
- Parses the JSON response
- Prints the user's name, followers, and public repos
- Handles errors gracefully
```

---

### 6. Data Processing

```
> Write Python code that:
1. Creates sample data (10 entries with name, age, city)
2. Converts it to a pandas DataFrame
3. Filters entries where age > 25
4. Saves to CSV
5. Prints summary statistics
```

---

## 🌐 Web & Research

### 7. Current Information

```
> Search online for the latest Python version and its release date. Then compare it to my current Python version in Termux.
```

---

### 8. Technology Research

```
> You are a Knowledge Research Specialist.

Research the best Python libraries for:
- Async HTTP requests
- Data validation
- CLI applications

Compare them and recommend one for each category with reasons.
```

---

### 9. Documentation Lookup

```
> Search for the official documentation of Flask's request handling and summarize the key points about accessing POST data.
```

---

## 🔧 Automation & Utilities

### 10. Batch File Operations

```
> Create a Python script that:
1. Creates a directory called "test_project"
2. Inside it, creates 3 files: main.py, utils.py, README.md
3. Adds basic Python template code to each .py file
4. Lists the created structure
```

---

### 11. Log Parser

```
> Write a Python script that:
- Reads a log file (create sample if needed)
- Counts occurrences of ERROR, WARNING, INFO
- Prints statistics
- Saves summary to results.txt
```

---

### 12. Environment Setup Helper

```
> Create a bash script that:
1. Checks if Python packages (requests, flask, pandas) are installed
2. Reports which are missing
3. Generates a requirements.txt for missing packages
```

---

## 📊 Data Analysis

### 13. Simple Analytics

```
> Generate sample sales data for 30 days (date, product, amount).
Analyze it to find:
- Total revenue
- Best selling day
- Average daily sales
- Create a simple text-based visualization
```

---

### 14. JSON Processing

```
> Create a Python script that:
1. Makes sample JSON data (5 users with id, name, email)
2. Validates email format
3. Filters valid entries
4. Saves to clean_data.json
5. Prints count of valid vs invalid
```

---

## 🎨 Creative Uses

### 15. Markdown Generator

```
> Create a Python script that generates a daily journal template in markdown format with:
- Today's date as title
- Sections for: Goals, Tasks, Notes, Reflections
- Save as journal_YYYY-MM-DD.md
```

---

### 16. Code Comment Generator

```
> Write a Python function that calculates Fibonacci numbers. Then add comprehensive docstrings and inline comments explaining each step.
```

---

## 🔄 Multi-Agent Workflows

### 17. Research → Design → Build

**Step 1 - Research:**
```
> You are a Knowledge Research Specialist.

Research the best approach for creating a simple REST API in Python. Compare Flask vs FastAPI. Recommend one with pros/cons.
```

**Step 2 - Architecture:**
```
> You are a Solution Architecture Specialist.

Based on [previous research], design a simple REST API for a todo app with:
- CRUD endpoints
- In-memory storage (no database)
- Input validation
- Error handling

Provide the architecture plan.
```

**Step 3 - Implementation:**
```
> You are a Code Execution Specialist.

Implement the todo API based on the architecture:
[paste architecture]

Create working code and test it.
```

---

### 18. Web Scraping Pipeline

**Step 1 - Scrape:**
```
> You are a Web Content Extraction Specialist.

Visit https://quotes.toscrape.com/ and extract:
- First 10 quotes
- Authors
- Tags

Structure the data as JSON.
```

**Step 2 - Process:**
```
> You are a Code Execution Specialist.

Take this scraped data:
[paste data]

Process it to:
- Count quotes per author
- List all unique tags
- Save clean data to quotes.json
```

---

## 🚀 Advanced Examples

### 19. Mini Task Manager

```
> Create a complete task management system:

1. Python script with functions to:
   - Add task (title, description, priority)
   - List tasks
   - Mark task complete
   - Delete task
   - Save/load from JSON file

2. Simple CLI interface

3. Test with sample tasks

Make it production-ready with error handling and documentation.
```

---

### 20. Personal Finance Tracker

```
> Build a simple expense tracker:

Features:
- Add expense (date, category, amount, description)
- List expenses
- Calculate total by category
- Monthly summary
- Data persistence (JSON)
- Input validation

Create working prototype and demonstrate with sample data.
```

---

## 📱 Android-Specific

### 21. Termux Info Script

```
> Create a Python script that gathers Termux environment info:
- Python version
- Installed packages (key ones)
- Current directory
- Available storage
- Termux version
- Generate nice formatted report
```

---

### 22. Battery-Friendly Automation

```
> Write a Python script that:
- Runs a task periodically (every 5 seconds for demo)
- Logs timestamp and a message
- Stops after 10 iterations
- Uses minimal CPU (sleep between tasks)
- Saves log to file

Demonstrate it's battery-friendly by showing the sleep mechanism.
```

---

## 🎯 Slash Commands Integration

### 23. Using /master

```
/master

Complete workflow:
1. Research best Python logging practices
2. Design a logging system for a web app
3. Implement example with Flask
4. Test and demonstrate
```

---

### 24. Using /code

```
/code

Write a Python script that:
- Takes command line arguments
- Validates input
- Performs calculation (user's choice)
- Returns formatted result

Include argparse, error handling, and help text.
```

---

### 25. Using /research

```
/research

Find the best lightweight database solutions for mobile/Termux Python apps. Compare SQLite, TinyDB, and JSON files. Consider:
- Performance
- Ease of use
- Storage efficiency
- Android compatibility
```

---

## 💡 Pro Tips for Better Results

### Be Specific
❌ "Make an API"
✅ "Create a Flask REST API with GET /users endpoint that returns JSON list of 3 sample users"

### Provide Context
```
> Context: I'm building a personal expense tracker.
Task: Write Python code to calculate monthly spending by category.
Expected: Function that takes list of expenses, returns dict of category totals.
```

### Iterative Refinement
```
Step 1: > Create basic version
Step 2: > Add error handling to previous code
Step 3: > Add logging
Step 4: > Add unit tests
```

### Use Roles
```
> You are a Code Execution Specialist.
[your task]
```

Makes responses more focused and expert.

---

## 🔗 Combining with Claude Code

**In Claude Code session:**
```
/code

Create a Termux automation script for my Android setup
```

**Then in Agent Zero:**
```
> Execute this script and verify it works:
[paste script from Claude Code]
```

---

## 🎓 Learning Projects

### Beginner: Calculator CLI
Build a calculator with Python that runs in Termux.

### Intermediate: Web Scraper + Database
Scrape quotes, store in SQLite, query and display.

### Advanced: Mini Web App
Flask app with API + HTML frontend, deploy on Termux.

---

## 📚 More Ideas

**Daily Automation:**
- Morning news summary
- Weather report
- Todo list generator
- Journal prompt creator

**Development Tools:**
- Code formatter
- Git helper scripts
- Project scaffolder
- Test data generator

**Data Science:**
- CSV analyzer
- Simple statistics calculator
- Data cleaner
- Chart generator (text-based)

**Utilities:**
- File organizer
- Backup script
- System monitor
- Network tester

---

## 🚀 Your Turn!

Try these examples and modify them for your needs!

**Share your creations:**
- Add them to this file
- Share in Agent Zero community
- Help others learn

---

**Happy building! 🎉**

*Versie: 1.0 - November 26, 2025*

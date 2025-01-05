# Typing Speed Tester

A modern, feature-rich typing speed test application built with Django. Test and improve your typing speed with real-time feedback and detailed mistake analysis.

*Built with [Windsurf](https://www.codeium.com/windsurf), the world's first agentic IDE.*

## Features

- **Real-time Typing Feedback**
  - Live WPM (Words Per Minute) counter
  - Character-by-character accuracy feedback
  - Color-coded visual feedback (green for correct, red for mistakes)
  - Instant cursor position tracking

- **Comprehensive Statistics**
  - Words Per Minute (WPM) calculation
  - Accuracy percentage
  - Time taken per test
  - Detailed mistake tracking

- **Mistake Analysis**
  - Track and display common typing mistakes
  - Word-level mistake analysis
  - Character-level mistake patterns
  - Most frequently mistyped words and characters

- **Customizable Tests**
  - Adjustable word count (10-25 words)
  - Option to retry the same text
  - Clean, distraction-free interface

## Technology Stack

- **Backend**: Django 4.2
- **Frontend**: 
  - HTML5, CSS3, JavaScript
  - Bootstrap 5
  - jQuery
- **Database**: SQLite3

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd typing_speed_tester
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

6. Visit `http://127.0.0.1:8000/` in your browser

## Usage

1. **Start a Test**
   - Select the number of words (10-25)
   - Click "Start Test"
   - Begin typing in the input field

2. **During the Test**
   - Watch your live WPM above the text
   - Green highlighting indicates correct typing
   - Red highlighting shows mistakes
   - The cursor shows your current position

3. **View Results**
   - See your final WPM, accuracy, and time
   - Review any mistakes made during the test
   - Option to retry the same text or start a new test

4. **Analyze Mistakes**
   - Visit the Mistakes page to see detailed statistics
   - View most common mistakes
   - Track improvement over time

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

*Created with ❤️ using [Windsurf](https://www.codeium.com/windsurf), the revolutionary agentic IDE that makes coding a breeze.*

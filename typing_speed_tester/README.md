# TypeFlow: Advanced Typing Speed Tester

A deeply interactive, modern typing speed suite built on Django. Hone your finger dexterity with highly analytical feedback loops, custom dictionaries, intelligent auditory telemetry, and biomechanic finger analysis. 


## 🚀 Key Features

### 🎧 Adaptive Auditory Telemetry & Dictation
- **Typewriter Acoustics:** Employs the native Web Audio API to yield instantaneous high-frequency soft ticks for successful keystrokes and dual-harmonic bells upon completion.
- **Immediate Error Feedback:** Generates harsh 150Hz sawtooth warning-buzzes the precise millisecond you create a typo.
- **Accessibility & Dictation:** A Web Speech API dictation engine that proactively reads words out loud. Explicitly features "blind recovery" spellouts (e.g., "capital S") when you type incorrectly so you never have to look down at the keyboard!

### 📊 Biomechanical & Advanced Analytics
- **QWERTY Finger Mapping:** Algorithmically maps your exact typo behavior against 10 distinct standard touch-typing finger assignments to detect biomechanical weaknesses in your reaches.
- **Global Dashboards:** High-level metrics tracking lifetime average speeds, best WPMs, true global accuracy, and aggregate active typing engagement logic.
- **Leaderboards:** Maps your success trajectories factoring in frequencies to isolate your Top 5 personal "Easiest" dictionary words.

### ⚙️ Deep Configuration Persistence & Customization
- **Modern Bootstrap 5 UI:** A gorgeously sleek dashboard equipped with toggles, badges, segregated telemetry layers, and distinct aesthetic boundaries.
- **Client-State Saving:** Your exact testing preferences (dictation on/off, ironclad modes, word counts) are mapped safely inside `localStorage` to effortlessly survive reloading.
- **Dynamic Database Slider Integration:** Backend Postgres aggregate queries natively evaluate your specific dynamic vocabulary minimum and maximum bounds.
- **"Startover on Mistake":** Toggle an aggressive Ironman enforcer that strictly punishes errors by instantly routing you back to absolute zero.
- **Word Dictionary Management:** Fully interactive curation system allowing dynamic addition and removal of testing lexicons.

## 🛠️ Technology Stack
- **Backend**: Python 3, Django 4.2
- **Frontend**: Bootstrap 5 Grid Layouts, HTML5 Web Speech and Web Audio APIs, jQuery, Custom JS State Management
- **Storage**: SQLite3 Relational DB, Browser `localStorage`

## ⚙️ Installation

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

6. Navigate to `http://127.0.0.1:8000/` in your browser to start typing!

## 🤝 Contributing
Contributions are absolutely welcome! Please feel free to submit a Pull Request to help us augment our analytics pipelines or UI interactions.

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

---
*Created with ❤️ using [Windsurf](https://www.codeium.com/windsurf), the revolutionary agentic IDE that makes coding a breeze.*

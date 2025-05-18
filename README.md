# Circle of Fifths Practice App

This is a practice app for learning and mastering the circle of fifths. The goal is to help musicians quickly recall which chords are related and which transitions are possible, similar to memorizing the multiplication table.

## Features

- **Major and Minor Circles:** Visualizes both major and minor chords in the circle of fifths.
- **Quiz Mode:** Test yourself on chord relationships, including clockwise, counterclockwise, and alternative (relative minor/major) movements.
- **Localization:** Supports multiple languages (e.g., English and Swedish).
- **Configurable Range:** Choose how many chords to include in your practice range.
- **Keyboard Controls:** Use keyboard shortcuts to answer questions and adjust settings.
- **Feedback:** Immediate feedback on your answers, with localized messages.
- **Interactive Circle:** Click on a slice of the circle of fifths to add or remove that chord from the quiz selection.

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/circleoffifths.git
    cd circleoffifths
    ```

2. **Set up a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the app:**
    ```bash
    python main.py
    ```

## Usage

- **Answer questions** by typing the chord name and pressing Enter.
- **Switch language** by changing the `lang` parameter in `main.py` or `game.py` (e.g., `"en"` for English, `"sv"` for Swedish).
- **Click on a slice** of the circle to add or remove that chord from the quiz.
- **Quit** with the `Esc` key.

## Localization

All user-facing text is localized. To add a new language, create a new JSON file in the `locales/` directory (e.g., `fr.json` for French) and translate the keys.

## Testing

Unit tests are located in the `tests/` directory.  
To run all tests:

```bash
python -m unittest discover -s tests
```

## Resources

- [How to Use the Circle of Fifths to Write Songs](https://neelmodi.com/how-to-use-the-circle-of-fifths-to-write-songs/)
- [YouTube: Circle of Fifths Explained](https://www.youtube.com/watch?v=7rMKOB1bQL4)
- [The Perfection of the Perfect Fifth](https://neelmodi.com/the-perfection-of-the-perfect-fifth/)

## License

MIT License

---

*Practice until you just know every time you think of a chord!*


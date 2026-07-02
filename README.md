# Perfect Pitch Ear Trainer 🎹

A Python-based interactive GUI application designed to train perfect pitch and interval recognition. 

I built this application to assist with my own piano and clarinet practice, specifically to speed up identifying complex jazz theory progressions by ear. It generates procedural audio using sine waves and features dynamic visual feedback. 

*Note: This was originally developed and executed in a local Linux environment on my Steam Deck, which influenced the local directory pathing and custom event loop architecture.*

## ⚙️ How It Works
Rather than relying purely on pre-recorded audio files, this application procedurally generates sine waves and constructs major and minor third chord inversions on the fly using `numpy` and `pygame`. 

### Core Features:
*   **Procedural Audio Generation:** Uses array manipulation (NumPy linspace and sine functions) to generate exact mathematical frequencies for notes across the 4th, 5th, and 6th octaves.
*   **Dynamic UI Rendering:** The Tkinter interface updates its background colors dynamically based on the specific pitch frequency and octave selected by the user.
*   **Chord Inversions:** Automatically calculates and plays major and minor 7th chord inversions to test ear training in complex harmonic contexts.
*   **Custom Event Loop:** Bypasses the standard Tkinter mainloop in favor of a custom Pygame event loop to ensure audio buffers and UI rendering stay perfectly synchronized without hanging the main thread.

## 🛠️ Technology Stack & Libraries
*   **Language:** Python 3.x
*   **GUI:** `tkinter`
*   **Audio & Math:** `pygame` (Mixer/Sndarray), `numpy`
*   **System Handling:** `os`, `random`, `time`

## 🚀 How to Run

1. Clone this repository to your local machine.
2. Ensure you have the required external dependencies installed:
   ```bash
   pip install numpy pygame

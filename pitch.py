# Perfect Pitch Trainer // June 17, 2024 // Perfect Pitch Trainer //
# Generates and displays a perfect pitch training game
# given the neccessary user input
import tkinter as tk
from tkinter import messagebox
import numpy as np
import pygame
import os
import random
import time

# Maximum dimensions of arrays and dictionaries
NOTE_FREQUENCIES = {
    'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23, 'G4': 392.00, 'A4': 440.00, 'B4': 493.88,
    'C5': 523.25, 'D5': 587.33, 'E5': 659.25, 'F5': 698.46, 'G5': 783.99, 'A5': 880.00, 'B5': 987.77,
    'C6': 1046.50, 'D6': 1174.66, 'E6': 1318.51, 'F6': 1396.91, 'G6': 1567.98, 'A6': 1760.00, 'B6': 1975.53
}

# Global varibles for storing game states and UI elements
gameActive = False
currentNote = ""
defaultColor = ""
noteButtons = {}

# Function Prototypes
# void generateSineWave(float, int);
# Generates a sine wave for a given frequency and duration
# void playChord(list);
# Generates each sine wave, normalizes to prevent clipping, and plays sound
# void playMajorThirdInversion(string);
# void playMinorThirdInversion(string);
# void fetchAndPlayRandomMp3(string, function);
# Reads directory where mp3 information is stored and outputs it to the mixer
# void changeBackgroundColorAndDisplay(string);
# Generates color of choice by checking string contents and updates GUI
# void handleUserClick(string);
# Handles the user interaction and checks against current gamestate
# void shuffleGridButtons();
# void startGameDisplayTones();
# Initializes variables to run the game loop and populates the grid
# void endGameClearMemory();

# Initializes standard modules
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)

# Variables
root = tk.Tk()
root.title("Perfect Pitch Trainer")
root.attributes('-fullscreen', False)
root.geometry("1280x800")
defaultColor = root.cget('bg')

frame = tk.Frame(root)
frame.pack(fill='both', expand=True)

buttonFrame = tk.Frame(frame)
buttonFrame.place(relx=0.5, rely=0.5, anchor='center')

def generateSineWave(frequency, duration):
    # Variables
    sampleRate = 44100
    t = np.linspace(0, duration, int(sampleRate * duration), endpoint=False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)

    return np.array(wave * 32767, dtype=np.int16)

def playChord(frequencies):
    # Variables
    duration = 1
    sampleRate = 44100
    t = np.linspace(0, duration, int(sampleRate * duration), endpoint=False)
    chord = np.zeros_like(t)

    for frequency in frequencies:
        sineWave = np.sin(2 * np.pi * frequency * t)
        chord += sineWave

    maxAmplitude = np.iinfo(np.int16).max
    chord = maxAmplitude * chord / np.max(np.abs(chord))
    chord = np.array(chord, dtype=np.int16)
    stereoChord = np.column_stack((chord, chord))

    soundBuffer = pygame.sndarray.make_sound(stereoChord)
    soundBuffer.play()

def playMajorThirdInversion(note):
    # Variables
    baseFrequency = NOTE_FREQUENCIES[note]
    majorThird = baseFrequency * (5/4)
    perfectFifth = baseFrequency * (3/2)
    majorSeventh = baseFrequency * (15/8)

    playChord([majorSeventh, baseFrequency, majorThird, perfectFifth])

def playMinorThirdInversion(note):
    # Variables
    baseFrequency = NOTE_FREQUENCIES[note]
    minorThird = baseFrequency * (6/5)
    perfectFifth = baseFrequency * (3/2)
    minorSeventh = baseFrequency * (7/4)

    playChord([minorSeventh, baseFrequency, minorThird, perfectFifth])

def fetchAndPlayRandomMp3(folder, callback=None):
    # Variables
    mp3Files = [f for f in os.listdir(folder) if f.endswith('.mp3')]
    randomMp3 = random.choice(mp3Files)

    pygame.mixer.music.load(os.path.join(folder, randomMp3))
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    if (callback):
        callback()

def changeBackgroundColorAndDisplay(note):
    # Variables
    targetColor = ""
    print(f"Changing color for note: {note}")

    if ('C' in note):
        if ('5' in note):
            targetColor = 'red2'
        else:
            targetColor = 'red'
    elif ('D' in note):
        targetColor = 'orange'
    elif ('E' in note):
        targetColor = 'yellow'
    elif ('F' in note):
        targetColor = 'green'
    elif ('G' in note):
        targetColor = 'blue'
    elif ('A' in note):
        targetColor = 'indigo'
    elif ('B' in note):
        targetColor = 'violet'
    elif (note == 'default'):
        targetColor = defaultColor

    root.configure(bg=targetColor)
    frame.configure(bg=targetColor)
    buttonFrame.configure(bg=targetColor)

def handleUserClick(note):
    # Variables
    global gameActive, currentNote
    isCorrectNote = False

    if (gameActive == False):
        randomOctave = random.choice(['4', '5', '6'])
        octaveNote = f'{note}{randomOctave}'
        changeBackgroundColorAndDisplay(octaveNote)
        playChord([NOTE_FREQUENCIES[octaveNote]])
    else:
        if (note + currentNote[-1] == currentNote):
            isCorrectNote = True

        if (isCorrectNote == True):
            changeBackgroundColorAndDisplay(currentNote)
            tk.messagebox.showinfo("Correct!", "You've selected the correct note!")
            baseFrequency = NOTE_FREQUENCIES[note + '4']
            playChord([baseFrequency])
            fetchAndPlayRandomMp3(os.path.join(os.path.dirname(__file__), 'Audio', note), callback=lambda: (startGameDisplayTones(), changeBackgroundColorAndDisplay('default')))
        else:
            tk.messagebox.showinfo("Try Again", "That was not the correct note. Try again!")

def shuffleGridButtons():
    # Variables
    notes = list(noteButtons.keys())

    for button in noteButtons.values():
        button.grid_remove()

    random.shuffle(notes)

    for i, note in enumerate(notes):
        noteButtons[note].grid(row=i//10, column=i%10)

def startGameDisplayTones():
    # Variables
    global currentNote, gameActive, defaultColor
    notes4thOctave = [note for note in NOTE_FREQUENCIES if '4' in note]
    notes5thOctave = [note for note in NOTE_FREQUENCIES if '5' in note]
    notes6thOctave = [note for note in NOTE_FREQUENCIES if '6' in note]
    selectedNotes = [
        random.choice(notes4thOctave),
        random.choice(notes5thOctave),
        random.choice(notes6thOctave)
    ]

    gameActive = True
    defaultColor = root.cget('bg')
    currentNote = random.choice(selectedNotes)

    root.configure(bg=defaultColor)
    shuffleGridButtons()
    playMajorThirdInversion(currentNote)
    pygame.time.set_timer(pygame.USEREVENT, 1500)

def endGameClearMemory():
    global gameActive
    gameActive = False

    pygame.mixer.quit()
    pygame.quit()
    endButton.config(state="disabled")
    root.after(1000, root.destroy)

# UI Elements
startButton = tk.Button(frame, text="Start", command=startGameDisplayTones)
startButton.pack()

endButton = tk.Button(frame, text="End", command=endGameClearMemory)
endButton.place(relx=0.5, rely=1.0, anchor='s')

for i, note in enumerate('CDEFGAB'):
    button = tk.Button(buttonFrame, text=note, command=lambda n=note: handleUserClick(n))
    button.grid(row=i//10, column=i%10)
    noteButtons[note] = button

def main():
    # Variables
    global gameActive
    loopRanOnce = True

    while True:
        try:
            for event in pygame.event.get():
                if (event.type == pygame.USEREVENT):
                    pygame.time.set_timer(pygame.USEREVENT, 0)
                    if (gameActive == True):
                        playMinorThirdInversion(currentNote)
        except Exception as e:
            print(f"An error occurred in the event loop: {e}")
            pygame.quit()
            break

        root.update_idletasks()
        root.update()

if __name__ == "__main__":
    main()

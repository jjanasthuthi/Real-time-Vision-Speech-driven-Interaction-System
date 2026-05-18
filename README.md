# Eye Controlled Mouse with Voice Commands 👁️🎤

A real-time hands-free computer interaction system that allows users to control the mouse cursor using eye movement and voice commands. The system uses MediaPipe FaceMesh for eye tracking and performs actions like cursor movement, clicking, scrolling, and control toggling.

## Motivation

Traditional mouse and keyboard interaction may not be convenient for everyone, especially for people with physical disabilities or users who need hands-free interaction. Existing eye-tracking systems can also be expensive.

This project aims to provide a simple and low-cost alternative using only a webcam and microphone.

---

## Features

 Cursor movement using eye movement  
 Blink detection for click and double click  
 Voice commands for system control  
 Scroll using eye movement  
 Pause/Resume control  
 Real-time webcam processing  
 Smooth cursor movement using filtering

---

## Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy
- PyAutoGUI
- SpeechRecognition
- Threading

---

## How It Works

### 1. Face and Eye Detection
The webcam captures video frames continuously and MediaPipe FaceMesh detects facial landmarks.

### 2. Calibration
The user looks straight at the screen for a few seconds. The system stores this as the center eye position.

### 3. Cursor Movement
Eye movement is compared with the calibrated position.

- Horizontal movement → cursor moves left/right
- Vertical movement → cursor moves up/down
- Smoothing is applied to reduce cursor shaking

### 4. Blink Detection
The distance between upper and lower eyelid landmarks is measured.

- Single blink → Click
- Quick repeated blink → Double click

### 5. Voice Commands
The system continuously listens for commands such as:

- Start
- Pause
- Click
- Double click
- Scroll up
- Scroll down
- Stop

---

## Project Flow

Webcam Input  
↓  
MediaPipe FaceMesh Detection  
↓  
Iris Landmark Extraction  
↓  
Eye Position Calculation  
↓  
Cursor Movement / Blink Detection / Voice Processing  
↓  
Mouse Actions

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/eye-controlled-mouse.git
```

Install required libraries:

```bash
pip install opencv-python mediapipe pyautogui numpy SpeechRecognition pyaudio
```

Run:

```bash
python filename.py
```

---

## Limitations

- Performance depends on lighting conditions
- Requires stable head position
- Blink detection may occasionally trigger unwanted clicks
- Webcam quality can affect tracking accuracy

---

## Future Improvements

- Add head pose correction
- Adaptive blink threshold
- Better gaze estimation
- Support for multiple users
- Improve tracking accuracy using advanced ML methods

---

## Applications

- Assistive technology for differently abled users
- Hands-free computer interaction
- Smart systems and accessibility tools
- Human-computer interaction research

---

## Author

J Janasthuthi

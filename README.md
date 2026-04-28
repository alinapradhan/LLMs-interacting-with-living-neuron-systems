# Demo-Only Hybrid AI + Living Brain Cell Simulation

This project is a **conceptual research demo** showing a closed cognitive loop between:

1. Simulated human-neuron-like activity,
2. Signal decoding,
3. AI reasoning,
4. Simulated neural stimulation output,
5. Feedback into the next synthetic neural frame.

> ⚠️ This is **visual simulation only**. It is **not** a medical system, implant, or neurostimulation device.

## Features

- Real-time neural signal simulator:
  - spike trains
  - EEG-like waveform
  - burst detection
  - oscillation bands (alpha, beta, theta, gamma)
  - network synchrony/plasticity metrics
- Mental state switching:
  - calm, focus, stress, curiosity, confusion, speech_intent, sleep, learning, emotional_excitement
- Decoder engine with interpreted intentions + confidence + reasoning
- AI thinking module with mode switching and reasoning trace
- Memory module tracking recent intentions, emotion trends, and learned preferences
- Neuron output encoder producing synthetic pulse trains and target regions
- Safety layer detecting panic loops, runaway cycles, and unstable output
- Live dashboard with controls:
  - Start / Pause / Reset
  - Change Brain State
  - Replay Session
  - Auto Simulation Mode

## Local Run

### 1) Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 2) Start app

```bash
python run_demo.py
```

### 3) Open dashboard

Visit:

```text
http://127.0.0.1:8000
```

## Project Structure

```text
app/
  neural_signal_simulator.py  # fake live neuron activity
  signal_decoder.py           # decode signals into intentions
  ai_thinking.py              # simulated LLM-style reasoning
  memory_module.py            # session memory and preference tracking
  output_encoder.py           # synthetic stimulation encoding
  safety_layer.py             # instability and loop safety checks
  closed_loop.py              # real-time cognitive loop orchestrator
  server.py                   # Flask API and static serving
static/
  index.html                  # dashboard UI
  styles.css                  # futuristic styling
  app.js                      # live controls + rendering
run_demo.py                   # main runner
```

## Notes

- The simulation runs continuously while started.
- Safety alerts auto-stop the loop.
- Replay shows recent timeline frames.

"""Closed cognitive loop orchestrator."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List
import threading
import time

from .ai_thinking import AIThinkingModule
from .memory_module import MemoryModule
from .neural_signal_simulator import NeuralSignalSimulator
from .output_encoder import NeuronOutputEncoder
from .safety_layer import SafetyLayer
from .signal_decoder import SignalDecoder


@dataclass
class LoopSnapshot:
    neural_frame: Dict = field(default_factory=dict)
    decoded: Dict = field(default_factory=dict)
    ai_output: Dict = field(default_factory=dict)
    encoded_output: Dict = field(default_factory=dict)
    memory: Dict = field(default_factory=dict)
    safety: Dict = field(default_factory=lambda: {"safe": True, "alerts": [], "action": "CONTINUE"})
    logs: List[str] = field(default_factory=list)
    running: bool = False
    tick: int = 0


class ClosedCognitiveLoop:
    """Continuously runs: signals -> decode -> AI think -> encode -> feedback."""

    def __init__(self) -> None:
        self.simulator = NeuralSignalSimulator()
        self.decoder = SignalDecoder()
        self.ai = AIThinkingModule()
        self.memory = MemoryModule()
        self.encoder = NeuronOutputEncoder()
        self.safety = SafetyLayer()

        self.snapshot = LoopSnapshot()
        self._lock = threading.Lock()
        self._thread: threading.Thread | None = None
        self._stop_event = threading.Event()
        self._feedback_bias = 0.0
        self.replay_frames: List[Dict] = []

    def set_brain_state(self, state: str) -> None:
        self.simulator.set_state(state)

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            with self._lock:
                self.snapshot.running = True
            return

        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def pause(self) -> None:
        with self._lock:
            self.snapshot.running = False

    def reset(self) -> None:
        self.pause()
        with self._lock:
            self.snapshot = LoopSnapshot()
            self.replay_frames.clear()
            self._feedback_bias = 0.0
        self.memory.reset()
        self.safety.reset()

    def replay(self) -> List[Dict]:
        return self.replay_frames[-60:]

    def get_snapshot(self) -> Dict:
        with self._lock:
            return {
                "neural_frame": self.snapshot.neural_frame,
                "decoded": self.snapshot.decoded,
                "ai_output": self.snapshot.ai_output,
                "encoded_output": self.snapshot.encoded_output,
                "memory": self.snapshot.memory,
                "safety": self.snapshot.safety,
                "logs": self.snapshot.logs[-18:],
                "running": self.snapshot.running,
                "tick": self.snapshot.tick,
                "available_states": self.simulator.available_states,
            }

    def _run(self) -> None:
        with self._lock:
            self.snapshot.running = True

        while not self._stop_event.is_set():
            with self._lock:
                is_running = self.snapshot.running
            if not is_running:
                time.sleep(0.08)
                continue

            frame = self.simulator.step(self._feedback_bias)
            decoded = self.decoder.decode(frame)
            memory_before = self.memory.snapshot()
            ai_output = self.ai.think(decoded, memory_before)
            encoded = self.encoder.encode(ai_output, decoded)
            safety = self.safety.evaluate(decoded, encoded)

            self.memory.record(decoded, ai_output)
            memory_after = self.memory.snapshot()

            self._feedback_bias = (encoded["modulation_intensity"] - 0.45) * 0.6
            log_line = (
                f"t={frame['timestamp']:.2f} | state={frame['mental_state']} "
                f"| intent={decoded['top_intention']} ({decoded['confidence']:.2f}) "
                f"| mode={ai_output['mode']}"
            )

            with self._lock:
                self.snapshot.neural_frame = frame
                self.snapshot.decoded = decoded
                self.snapshot.ai_output = ai_output
                self.snapshot.encoded_output = encoded
                self.snapshot.memory = memory_after
                self.snapshot.safety = safety
                self.snapshot.logs.append(log_line)
                self.snapshot.tick += 1
                self.replay_frames.append(
                    {
                        "tick": self.snapshot.tick,
                        "eeg": frame["eeg"],
                        "intent": decoded["top_intention"],
                        "response": ai_output["response"],
                    }
                )

                if not safety["safe"]:
                    self.snapshot.running = False
                    self.snapshot.logs.append("SAFETY STOP triggered: " + "; ".join(safety["alerts"]))

            time.sleep(0.22)

    def shutdown(self) -> None:
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)

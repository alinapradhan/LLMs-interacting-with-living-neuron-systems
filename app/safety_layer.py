"""Safety checks for synthetic closed-loop simulation."""

from __future__ import annotations

from collections import deque
from typing import Deque, Dict, List


class SafetyLayer:
    """Detect unstable loops, panic repetition, and contradictory outputs."""

    def __init__(self) -> None:
        self.last_intents: Deque[str] = deque(maxlen=8)
        self.last_intensities: Deque[float] = deque(maxlen=8)
        self.alerts: List[str] = []

    def evaluate(self, decoded: Dict, encoded: Dict) -> Dict:
        intent = decoded["top_intention"]
        intensity = encoded["modulation_intensity"]
        self.last_intents.append(intent)
        self.last_intensities.append(intensity)
        self.alerts = []

        panic_count = sum(1 for i in self.last_intents if i == "fear")
        if panic_count >= 5:
            self.alerts.append("Repeated panic/fear signals exceeded threshold.")

        avg_intensity = sum(self.last_intensities) / max(1, len(self.last_intensities))
        if avg_intensity > 0.9:
            self.alerts.append("Stimulation intensity too high for extended period.")

        if len(set(self.last_intents)) == 1 and len(self.last_intents) >= 6:
            self.alerts.append("Runaway feedback cycle detected (single-intent loop).")

        if intent == "fear" and encoded["signal_frequency_hz"] > 26:
            self.alerts.append("Contradictory output: fear intent with high-frequency stimulation.")

        unstable = len(self.alerts) > 0
        return {
            "safe": not unstable,
            "alerts": list(self.alerts),
            "action": "STOP_SIMULATION" if unstable else "CONTINUE",
        }

    def reset(self) -> None:
        self.last_intents.clear()
        self.last_intensities.clear()
        self.alerts = []

"""Neuron output encoder.

Encodes AI output into synthetic stimulation patterns.
Simulation only; not real neurostimulation.
"""

from __future__ import annotations

from typing import Dict, List
import random


class NeuronOutputEncoder:
    """Convert AI response into fake neural stimulation instructions."""

    def encode(self, ai_output: Dict, decoded: Dict) -> Dict:
        mode = ai_output["mode"]

        base_frequency = {
            "knowledge": 28,
            "explanation": 22,
            "planning": 30,
            "calming": 14,
            "contextual_reminder": 20,
            "general": 18,
        }.get(mode, 18)

        intensity = min(1.0, 0.35 + decoded["confidence"] * 0.55)
        packet_symbols: List[str] = [random.choice(["Δ", "Σ", "Φ", "Ψ", "Λ"]) for _ in range(6)]

        return {
            "pulse_train": [round(base_frequency * random.uniform(0.85, 1.15), 2) for _ in range(8)],
            "signal_frequency_hz": round(base_frequency * (0.85 + intensity * 0.3), 2),
            "neuron_packets": "".join(packet_symbols),
            "target_regions": ["Prefrontal Cortex (sim)", "Temporal Association (sim)", "Limbic Overlay (sim)"],
            "modulation_intensity": round(intensity, 3),
            "safety_note": "Visual simulation only. Not medical output.",
        }

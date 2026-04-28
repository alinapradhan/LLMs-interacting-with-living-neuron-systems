"""Signal decoder engine.

Maps synthetic neuron activity into interpreted intentions with confidence.
"""

from __future__ import annotations

from typing import Dict, List


class SignalDecoder:
    """Translate synthetic neural frames into human-readable intent outputs."""

    def decode(self, frame: Dict) -> Dict:
        bands = frame["oscillation_bands"]
        pattern = frame["network_pattern"]
        firing_rate = frame["firing_rate_hz"]

        scores: Dict[str, float] = {
            "curiosity": 0.35 + bands["gamma"] * 0.25 + pattern["plasticity"] * 0.2,
            "fear": 0.15 + max(0.0, -pattern["emotional_valence"]) * 0.5 + (0.2 if frame["burst"] else 0),
            "hunger": 0.1 + max(0.0, 0.8 - bands["alpha"]) * 0.3,
            "speaking_intent": 0.2 + bands["gamma"] * 0.2 + (0.2 if frame["mental_state"] == "speech_intent" else 0),
            "memory_recall": 0.2 + bands["theta"] * 0.3 + pattern["synchrony"] * 0.2,
            "attention": 0.2 + bands["beta"] * 0.35 + firing_rate * 0.02,
            "happiness": 0.2 + max(0.0, pattern["emotional_valence"]) * 0.6,
            "confusion": 0.15 + abs(bands["alpha"] - bands["beta"]) * 0.2 + (0.2 if frame["mental_state"] == "confusion" else 0),
            "decision_making": 0.25 + bands["beta"] * 0.25 + pattern["synchrony"] * 0.25,
            "question_intent": 0.2 + bands["gamma"] * 0.2 + (0.15 if frame["mental_state"] in {"curiosity", "confusion"} else 0),
        }

        normalized = {k: min(0.99, max(0.01, round(v / 1.6, 3))) for k, v in scores.items()}
        ranked: List[tuple[str, float]] = sorted(normalized.items(), key=lambda x: x[1], reverse=True)
        top_intent, confidence = ranked[0]

        reasons = [
            f"beta={bands['beta']} drove attention/decision score",
            f"gamma={bands['gamma']} shaped curiosity/question likelihood",
            f"valence={pattern['emotional_valence']} modulated fear/happiness",
            f"burst_event={'yes' if frame['burst'] else 'no'} altered fear weighting",
        ]

        return {
            "top_intention": top_intent,
            "confidence": confidence,
            "all_intentions": normalized,
            "decoder_reasoning": reasons,
        }

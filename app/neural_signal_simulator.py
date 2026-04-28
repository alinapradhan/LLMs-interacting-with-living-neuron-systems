"""Neural signal simulator for demo-only hybrid AI + neuron loop.

This module generates fake neural activity patterns in real time.
All output is synthetic and for visualization only.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List
import math
import random


@dataclass
class BrainStateProfile:
    """Controls signal behavior for one mental state."""

    baseline_hz: float
    burst_probability: float
    noise_scale: float
    alpha: float
    beta: float
    theta: float
    gamma: float
    excitability: float
    emotional_valence: float


class NeuralSignalSimulator:
    """Generate fake spike trains, EEG bands, bursts, and network metrics."""

    def __init__(self) -> None:
        self.t = 0.0
        self.dt = 0.08
        self.current_state = "calm"
        self._phase = random.random() * math.tau
        self._states: Dict[str, BrainStateProfile] = {
            "calm": BrainStateProfile(6, 0.05, 0.2, 1.0, 0.4, 0.8, 0.2, 0.4, 0.2),
            "focus": BrainStateProfile(10, 0.08, 0.18, 0.5, 1.2, 0.4, 0.6, 0.7, 0.1),
            "stress": BrainStateProfile(13, 0.2, 0.5, 0.3, 1.3, 0.2, 0.8, 0.85, -0.5),
            "curiosity": BrainStateProfile(9, 0.12, 0.25, 0.6, 0.9, 0.5, 0.9, 0.75, 0.4),
            "confusion": BrainStateProfile(8, 0.14, 0.4, 0.5, 0.8, 0.7, 0.5, 0.6, -0.1),
            "speech_intent": BrainStateProfile(12, 0.1, 0.22, 0.3, 1.1, 0.3, 1.2, 0.8, 0.15),
            "sleep": BrainStateProfile(4, 0.03, 0.12, 0.9, 0.2, 1.2, 0.1, 0.25, 0.0),
            "learning": BrainStateProfile(11, 0.16, 0.28, 0.5, 1.0, 0.6, 1.0, 0.82, 0.35),
            "emotional_excitement": BrainStateProfile(14, 0.21, 0.45, 0.2, 1.1, 0.2, 1.4, 0.92, 0.8),
        }

    @property
    def available_states(self) -> List[str]:
        return list(self._states.keys())

    def set_state(self, state: str) -> None:
        if state in self._states:
            self.current_state = state

    def _spike_train(self, baseline_hz: float, excitability: float) -> List[int]:
        window = 30
        spike_prob = min(0.95, (baseline_hz / 22.0) * (0.45 + excitability * 0.6))
        spikes = [1 if random.random() < spike_prob * random.uniform(0.4, 1.0) else 0 for _ in range(window)]
        return spikes

    def _eeg_waveform(self, profile: BrainStateProfile) -> float:
        self._phase += self.dt * (0.6 + profile.excitability)
        alpha_wave = profile.alpha * math.sin(self.t * 0.7 + self._phase)
        beta_wave = profile.beta * math.sin(self.t * 1.4 + self._phase * 0.5)
        theta_wave = profile.theta * math.sin(self.t * 0.4 + self._phase * 1.3)
        gamma_wave = profile.gamma * math.sin(self.t * 2.5 + self._phase * 0.2)
        noise = random.gauss(0, profile.noise_scale)
        return alpha_wave + beta_wave + theta_wave + gamma_wave + noise

    def step(self, feedback_bias: float = 0.0) -> Dict:
        """Generate a single synthetic neural frame."""
        profile = self._states[self.current_state]
        self.t += self.dt

        baseline_hz = max(1.0, profile.baseline_hz + (feedback_bias * 2.0))
        spikes = self._spike_train(baseline_hz, profile.excitability)
        eeg_value = self._eeg_waveform(profile)
        burst = random.random() < (profile.burst_probability + max(0.0, feedback_bias) * 0.05)

        # Simple network graph metrics for visual display.
        network_sync = min(1.0, max(0.0, 0.5 + eeg_value * 0.05 + profile.excitability * 0.35))
        plasticity = min(1.0, max(0.0, 0.4 + profile.gamma * 0.2 + (0.1 if self.current_state == "learning" else 0)))
        oscillation_bands = {
            "alpha": round(profile.alpha * random.uniform(0.8, 1.25), 3),
            "beta": round(profile.beta * random.uniform(0.8, 1.25), 3),
            "theta": round(profile.theta * random.uniform(0.8, 1.25), 3),
            "gamma": round(profile.gamma * random.uniform(0.8, 1.25), 3),
        }

        return {
            "timestamp": round(self.t, 2),
            "mental_state": self.current_state,
            "spikes": spikes,
            "eeg": round(eeg_value, 3),
            "firing_rate_hz": round(baseline_hz + random.uniform(-0.6, 0.6), 2),
            "burst": burst,
            "oscillation_bands": oscillation_bands,
            "network_pattern": {
                "synchrony": round(network_sync, 3),
                "plasticity": round(plasticity, 3),
                "emotional_valence": round(profile.emotional_valence, 3),
            },
        }

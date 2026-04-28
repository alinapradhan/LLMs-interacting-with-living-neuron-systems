"""Session memory tracking for the demo loop."""

from __future__ import annotations

from collections import Counter, deque
from typing import Deque, Dict, List


class MemoryModule:
    """Keeps short-term memory of interpreted thoughts and responses."""

    def __init__(self, max_items: int = 20) -> None:
        self.decoded_thoughts: Deque[Dict] = deque(maxlen=max_items)
        self.responses: Deque[str] = deque(maxlen=max_items)
        self.emotion_history: Deque[str] = deque(maxlen=max_items)
        self.preferences: Counter = Counter()

    def record(self, decoded: Dict, ai_output: Dict) -> None:
        self.decoded_thoughts.append(
            {
                "intent": decoded["top_intention"],
                "confidence": decoded["confidence"],
            }
        )
        self.responses.append(ai_output["response"])
        emotional_tag = ai_output["emotional_context"]
        self.emotion_history.append(emotional_tag)
        self.preferences[decoded["top_intention"]] += 1

    def snapshot(self) -> Dict:
        recent_chain = [
            f"{item['intent']} ({item['confidence']:.2f})"
            for item in list(self.decoded_thoughts)[-6:]
        ]
        return {
            "recent_decoded": list(self.decoded_thoughts),
            "recent_responses": list(self.responses)[-6:],
            "repeated_emotions": dict(Counter(self.emotion_history)),
            "learned_preferences": dict(self.preferences),
            "memory_chain": " -> ".join(recent_chain) if recent_chain else "No chain yet",
        }

    def reset(self) -> None:
        self.decoded_thoughts.clear()
        self.responses.clear()
        self.emotion_history.clear()
        self.preferences.clear()

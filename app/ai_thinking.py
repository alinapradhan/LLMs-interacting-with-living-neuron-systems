"""AI thinking module.

Simulates LLM-like reasoning paths based on decoded intentions.
"""

from __future__ import annotations

from typing import Dict


class AIThinkingModule:
    """Simulated thought engine with mode switching and reasoning trace."""

    def think(self, decoded: Dict, memory_snapshot: Dict) -> Dict:
        intent = decoded["top_intention"]
        confidence = decoded["confidence"]

        mode = "general"
        emotional_context = "neutral"
        response = "Maintaining baseline reflective mode."
        trace = [f"Detected intent '{intent}' with confidence {confidence:.2f}"]

        if intent in {"curiosity", "question_intent"}:
            mode = "knowledge"
            emotional_context = "engaged"
            response = "I sense curiosity. Let me provide a compact explanation with examples."
            trace.append("Activated knowledge answer pathway")
        elif intent == "confusion":
            mode = "explanation"
            emotional_context = "supportive"
            response = "Confusion detected. I'll break this into simple step-by-step guidance."
            trace.append("Switched to explanation mode for clarity")
        elif intent == "attention":
            mode = "planning"
            emotional_context = "focused"
            response = "Strong attention detected. Generating a practical action plan."
            trace.append("Planning mode triggered by sustained focus")
        elif intent == "fear":
            mode = "calming"
            emotional_context = "calm_reassurance"
            response = "Stress/fear signal detected. Slowing down and offering grounding prompts."
            trace.append("Applied calming language policy")
        elif intent == "memory_recall":
            mode = "contextual_reminder"
            emotional_context = "nostalgic"
            last_chain = memory_snapshot.get("memory_chain", "")
            response = f"Memory recall active. Previous chain: {last_chain}"
            trace.append("Injected short-term memory chain into response")

        trace.append(f"Response mode finalized as '{mode}'")

        return {
            "mode": mode,
            "emotional_context": emotional_context,
            "reasoning_trace": trace,
            "response": response,
        }

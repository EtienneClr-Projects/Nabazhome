from __future__ import annotations


class BoardService:
    """Thin abstraction over board-level actions. Currently used as a no-op stub."""

    def announce(self, message: str) -> str:
        return message

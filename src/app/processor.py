"""
Processor module for stock-backtest-strategies.

Validates incoming messages and executes multi-signal strategies to
generate final trade actions. This simulates rules-based or weighted logic.
"""

from typing import Any

from app.utils.setup_logger import setup_logger
from app.utils.types import ValidatedMessage
from app.utils.validate_data import validate_message_schema

logger = setup_logger(__name__)


def validate_input_message(message: dict[str, Any]) -> ValidatedMessage:
    """
    Validate the incoming raw message against the expected schema.

    Args:
        message (dict[str, Any]): The raw input message.

    Returns:
        ValidatedMessage: A validated message object.

    Raises:
        ValueError: If the message format is invalid.
    """
    logger.debug("🔍 Validating message schema...")
    if not validate_message_schema(message):
        logger.error("❌ Invalid message schema: %s", message)
        raise ValueError("Invalid message format")
    return message  # type: ignore[return-value]


def evaluate_strategy(message: ValidatedMessage) -> dict[str, Any]:
    """
    Evaluate a configurable strategy using available sub-signals.

    Args:
        message (ValidatedMessage): Validated signal-rich input.

    Returns:
        dict[str, Any]: Enriched message with final trade decision.
    """
    symbol = message.get("symbol", "UNKNOWN")
    logger.info("🧮 Evaluating strategy for %s", symbol)

    # Simplified rule-based logic (replace with config/weights later)
    votes = [
        message.get("alpha_signal"),
        message.get("momentum_signal"),
        message.get("sentiment_signal"),
        message.get("composite_signal"),
        message.get("beta_signal"),
        message.get("factor_signal"),
    ]

    vote_count = sum(1 for v in votes if v in ("BUY", "INCLUDE", "OVEREXPOSED", "REVERT_UP"))

    decision = "BUY" if vote_count >= 3 else "HOLD"
    result = {
        "final_strategy_decision": decision,
        "strategy_votes": vote_count,
    }

    logger.debug("✅ Final strategy decision for %s: %s", symbol, result)
    return {**message, **result}

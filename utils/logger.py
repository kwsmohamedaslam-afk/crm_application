import logging
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from models.log_transaction import LogTransaction

# Create a logger instance
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Optional: Add console handler if not already configured elsewhere
if not logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def log_event(db: Session, user_id: str, event: str) -> None:
    """Insert a log entry. Call this after any important action."""
    entry = LogTransaction(
        date_time=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        events=event,
        user_id=str(user_id),
    )
    db.add(entry)
    db.commit()
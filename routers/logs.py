from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import get_current_user
from models.log_transaction import LogTransaction
from models.user import UserMaster
from schemas.log_transaction import LogCreate, LogOut
from utils.logger import log_event

router = APIRouter(prefix="/api/logs", tags=["Logs"])


@router.post("/", response_model=LogOut, status_code=status.HTTP_201_CREATED, summary="Create a log entry")
def create_log(
    payload: LogCreate,
    db: Session = Depends(get_db),
    current_user: UserMaster = Depends(get_current_user),
):
    """Manually insert a log/transaction entry."""
    entry = LogTransaction(
        date_time=payload.date_time,
        events=payload.events,
        user_id=payload.user_id,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.get("/", response_model=List[LogOut], summary="List all log entries")
def list_logs(
    user_id: Optional[str] = Query(None, description="Filter by user_id"),
    limit: int = Query(100, ge=1, le=1000, description="Max records to return"),
    offset: int = Query(0, ge=0, description="Records to skip"),
    db: Session = Depends(get_db),
    current_user: UserMaster = Depends(get_current_user),
):
    """
    Retrieve log entries with optional filtering.
    - **user_id**: filter logs for a specific user
    - **limit / offset**: pagination controls
    """
    query = db.query(LogTransaction)
    if user_id:
        query = query.filter(LogTransaction.user_id == user_id)
    return query.order_by(LogTransaction.id.desc()).offset(offset).limit(limit).all()


@router.get("/{log_id}", response_model=LogOut, summary="Get a log entry by ID")
def get_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: UserMaster = Depends(get_current_user),
):
    """Retrieve a single log entry by its primary key."""
    entry = db.query(LogTransaction).filter(LogTransaction.id == log_id).first()
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log entry not found")
    return entry


@router.delete("/{log_id}", status_code=status.HTTP_200_OK, summary="Delete a log entry")
def delete_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: UserMaster = Depends(get_current_user),
):
    """Delete a specific log entry by ID."""
    entry = db.query(LogTransaction).filter(LogTransaction.id == log_id).first()
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log entry not found")

    db.delete(entry)
    db.commit()
    log_event(db, str(current_user.id), f"Deleted log entry id={log_id}")
    return {"message": f"Log entry {log_id} deleted successfully"}


@router.delete("/", status_code=status.HTTP_200_OK, summary="Clear all log entries")
def clear_logs(
    db: Session = Depends(get_db),
    current_user: UserMaster = Depends(get_current_user),
):
    """⚠️ Delete ALL log entries. Use with caution."""
    deleted = db.query(LogTransaction).delete()
    db.commit()
    return {"message": f"Deleted {deleted} log entries"}

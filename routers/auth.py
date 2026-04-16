from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import verify_password, create_access_token, get_current_user
from models.user import UserMaster
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import UserLogin, TokenOut, UserOut
from utils.logger import log_event

router = APIRouter(prefix="/api/auth", tags=["Auth"])


# @router.post("/login", response_model=TokenOut, summary="Login and get JWT token")
# def login(payload: UserLogin, db: Session = Depends(get_db)):

#     user = db.query(UserMaster).filter(UserMaster.username == payload.username).first()
#     if not user or not verify_password(payload.password, user.password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid username or password",
#         )

#     token = create_access_token({"sub": str(user.id)})
#     log_event(db, str(user.id), f"User '{user.username}' logged in")
#     return TokenOut(access_token=token, user=UserOut.model_validate(user))

@router.post("/login", response_model=TokenOut, summary="Login and get JWT token")
def login(payload: UserLogin, db: Session = Depends(get_db)):

    user = db.query(UserMaster).filter(UserMaster.username == payload.username).first()

    # ✅ Check if user exists
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    if not user.status:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is locked. Contact admin.",
        )

    if not verify_password(payload.password, user.password):
        user.failed_attempts += 1

        # 🚨 Lock account after 5 attempts
        if user.failed_attempts >= 5:
            user.status = False
            db.commit()

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Account locked after 5 failed attempts. Contact admin.",
            )

        db.commit()

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid password. Attempts left: {5 - user.failed_attempts}",
        )

    # ✅ Successful login → reset attempts
    user.failed_attempts = 0
    db.commit()

    token = create_access_token({"sub": str(user.id)})
    log_event(db, str(user.id), f"User '{user.username}' logged in")

    return TokenOut(access_token=token, user=UserOut.model_validate(user))


@router.put("/unlock-user/{user_id}")
def unlock_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserMaster).filter(UserMaster.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.failed_attempts = 0
    user.status = True
    db.commit()

    return {"message": "User unlocked successfully"}

@router.get("/me", response_model=UserOut, summary="Get current authenticated user")
def get_me(current_user: UserMaster = Depends(get_current_user)):
    """Returns the profile of the currently authenticated user."""
    return current_user

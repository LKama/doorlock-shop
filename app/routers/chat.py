from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.chat_message import ChatMessage

from app.utils.dependencies import get_current_user


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.get("/")
def get_messages(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return (
        db.query(ChatMessage)
        .filter(
            ChatMessage.user_id ==
            current_user.id
        )
        .order_by(
            ChatMessage.created_at.asc()
        )
        .all()
    )


@router.post("/send")
def send_message(
    message: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    msg = ChatMessage(
        user_id=current_user.id,
        sender="user",
        message=message
    )

    db.add(msg)

    db.commit()

    return {
        "message": "sent"
    }
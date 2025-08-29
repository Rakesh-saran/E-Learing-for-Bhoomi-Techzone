from fastapi import APIRouter, HTTPException
from database.schemas.notification import NotificationSchema
from database.repositories.notification_repository import NotificationRepository

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.post("/")
def add_notification(notification: NotificationSchema):
    result = NotificationRepository.create(notification.dict())
    notification_dict = notification.dict()
    notification_dict["id"] = str(result.inserted_id)
    return notification_dict

@router.get("/user/{user_id}")
def list_notifications(user_id: str):
    notifications = NotificationRepository.find_by_user(user_id)
    for n in notifications:
        n["id"] = str(n["_id"])
        n.pop("_id")
    return notifications

@router.put("/{notification_id}/read")
def mark_as_read(notification_id: str):
    result = NotificationRepository.mark_as_read(notification_id)
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"message": "Notification marked as read"}

@router.delete("/{notification_id}")
def remove_notification(notification_id: str):
    result = NotificationRepository.delete(notification_id)
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"message": "Notification deleted"}

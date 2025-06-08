from core import models


def send_notifications(alarm_data: dict, notification: models.AlarmNotification):
     for user_linked in alarm_data["alarm_users"]:
        if not user_linked["notify"]:
            continue
        # Only printing data to follow activity instructions 
        user_id = user_linked["user"]
        print(f"[Mock Notification]: Sending to User {user_id} Notification<{notification}>")

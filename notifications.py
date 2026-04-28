from config import get_settings


def send_push_notification(target: str, title: str, body: str) -> dict:
    settings = get_settings()
    provider = "firebase" if settings.firebase_api_key else "console"
    return {
        "provider": provider,
        "target": target,
        "title": title,
        "body": body,
        "status": "queued",
    }

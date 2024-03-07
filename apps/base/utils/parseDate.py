from datetime import datetime


def parseDate(date: str) -> datetime:
    return datetime.strptime(date, "%Y-%m-%d %H:%M:%S").date()
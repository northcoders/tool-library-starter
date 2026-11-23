# Dates are worked out from today, so the open loans are always current:
# the Pressure Washer and Rototiller are due back in the next few days,
# and the Socket Set is overdue.
from datetime import date, timedelta


def days_from_today(days):
    return (date.today() + timedelta(days=days)).isoformat()


loans = [
    {"id": 1, "tool_id": 3, "member_id": 2, "borrowed_date": days_from_today(-1), "due_date": days_from_today(2), "returned_date": None},
    {"id": 2, "tool_id": 15, "member_id": 4, "borrowed_date": days_from_today(-2), "due_date": days_from_today(1), "returned_date": None},
    {"id": 3, "tool_id": 1, "member_id": 1, "borrowed_date": days_from_today(-30), "due_date": days_from_today(-23), "returned_date": days_from_today(-24)},
    {"id": 4, "tool_id": 5, "member_id": 3, "borrowed_date": days_from_today(-35), "due_date": days_from_today(-28), "returned_date": days_from_today(-29)},
    {"id": 5, "tool_id": 2, "member_id": 5, "borrowed_date": days_from_today(-12), "due_date": days_from_today(-7), "returned_date": days_from_today(-7)},
    {"id": 6, "tool_id": 9, "member_id": 6, "borrowed_date": days_from_today(-16), "due_date": days_from_today(-2), "returned_date": None},
    {"id": 7, "tool_id": 4, "member_id": 2, "borrowed_date": days_from_today(-60), "due_date": days_from_today(-55), "returned_date": days_from_today(-56)},
    {"id": 8, "tool_id": 18, "member_id": 4, "borrowed_date": days_from_today(-90), "due_date": days_from_today(-85), "returned_date": days_from_today(-86)},
    {"id": 9, "tool_id": 11, "member_id": 1, "borrowed_date": days_from_today(-120), "due_date": days_from_today(-117), "returned_date": days_from_today(-117)},
    {"id": 10, "tool_id": 6, "member_id": 3, "borrowed_date": days_from_today(-150), "due_date": days_from_today(-143), "returned_date": days_from_today(-145)},
    {"id": 11, "tool_id": 17, "member_id": 5, "borrowed_date": days_from_today(-180), "due_date": days_from_today(-175), "returned_date": days_from_today(-175)},
    {"id": 12, "tool_id": 10, "member_id": 6, "borrowed_date": days_from_today(-200), "due_date": days_from_today(-197), "returned_date": days_from_today(-198)},
]

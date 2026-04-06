# utils.py
# Helper functions for the entire application

import datetime

def calc_level(total_xp: int) -> int:
    """Calculate user level based on total XP using the formula: 1 + (total_xp // 200)"""
    return 1 + (total_xp // 200)

def get_level_name(level: int) -> str:
    """Return the title for a given level."""
    if level < 3:
        return "Seedling"
    elif level < 6:
        return "Student"
    elif level < 10:
        return "Scholar"
    elif level < 15:
        return "Achiever"
    elif level < 20:
        return "Master"
    else:
        return "Legend"

def format_time_minutes(minutes: int) -> str:
    """Format total minutes into a more readable format, e.g., 2h 15m"""
    if minutes < 60:
        return f"{minutes}m"
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}h {mins}m" if mins else f"{hours}h"

def format_timer_display(seconds: int) -> str:
    """Format seconds into MM:SS format"""
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02d}:{secs:02d}"

# List of 20 motivational quotes to be displayed during study sessions
MOTIVATIONAL_QUOTES = [
    "Focus on the step in front of you.",
    "Small progress is still progress.",
    "The secret of getting ahead is getting started.",
    "Don't stop until you're proud.",
    "It always seems impossible until it's done.",
    "Dream big. Work hard. Stay focused.",
    "Don't wish for it, work for it.",
    "Success usually comes to those who are too busy to be looking for it.",
    "You don't have to be great to start, but you have to start to be great.",
    "Believe you can and you're halfway there.",
    "The only bad workout is the one that didn't happen.",
    "Push yourself, because no one else is going to do it for you.",
    "Hard work beats talent when talent doesn't work hard.",
    "Discipline is choosing between what you want now and what you want most.",
    "Do something today that your future self will thank you for.",
    "The harder you work for something, the greater you'll feel when you achieve it.",
    "Success is the sum of small efforts, repeated day in and day out.",
    "Nothing worth having comes easy.",
    "Stay focused, ignore the distractions, and you will accomplish your goals much faster.",
    "A year from now you may wish you had started today."
]

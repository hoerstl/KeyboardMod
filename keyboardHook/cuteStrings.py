import random

# Dictionary of cute strings categorized by use case
CUTE_STRINGS = {
    "general": {
        "titles": [
            "❤️ Heart-to-Heart Sync",
            "☕ Coffee & Cuddles Check-in",
            "🌟 Chat with My Favorite Human",
            "💌 Quick Love & Status Update",
            "✨ Daily Dose of You",
            "☕ Coffee Break with My Queen",
            "💕 Midday Sunshine Check-in",
            "📞 Priority Call: You",
            "✨ 30 Minutes of Your Smile",
            "🌸 Quick Hello to My World",
            "💖 Special Moment with You",
            "🌸 Just Because We're Together",
            "🥰 My Favorite Part of the Day",
            "💫 Us Time",
            "🥰 You + Me Time",
            "🌸 Sunshine on My Calendar",
            "💫 Favorite Appointment of the Day",
            "💖 Because I Love You"
        ],
        "descriptions": [
            "No rigid agenda required—just a lovely excuse to hear your voice.",
            "Checking in with the CEO of my heart.",
            "Taking a quick pause from the busy day to reconnect with you.",
            "Mandatory smile break brought to you by my wonderful wife.",
            "Checking in to see the prettiest smile in the world.",
            "Mandatory cuddle break via screen.",
            "Just wanted to hear your voice in the middle of the day.",
            "Any time spent with you is time well spent.",
            "Just a calendar reminder of how much I adore you.",
            "Reserved for the most amazing person in the world.",
            "Scheduled interruption for hugs and kisses.",
            "Reserved exclusively for my absolute favorite person.",
            "A reminder that you're always on my mind.",
            "Just because I wanted to block out some time for you."
        ]
    },
}

def getCuteTitleAndDescription(use_case="general"):
    """
    Returns a random cute (title, description) tuple for the given use case.
    Fallback to 'general' if the use case doesn't exist.
    """
    category = CUTE_STRINGS.get(use_case, CUTE_STRINGS["general"])
    title = random.choice(category["titles"])
    description = random.choice(category["descriptions"])
    return title, description

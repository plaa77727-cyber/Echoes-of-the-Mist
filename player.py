class Player:
    """Player class to track game state"""

    def __init__(self):
        self.courage = 50
        self.creativity = 50
        self.risk = 50
        self.chosen_path = []
        self.event_history = []

    def update_stat(self, stat_name, value):
        """Update a player stat"""
        current = getattr(self, stat_name, 0)
        setattr(self, stat_name, max(0, min(100, current + value)))

    def add_to_history(self, event_id, choice):
        """Add an event to player history"""
        self.event_history.append({
            'event_id': event_id,
            'choice': choice
        })

    def get_stats(self):
        """Return all stats as dictionary"""
        return {
            'courage': self.courage,
            'creativity': self.creativity,
            'risk': self.risk
        }
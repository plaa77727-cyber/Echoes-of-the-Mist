from events import EVENTS


class GameLogic:
    """Core game logic handler"""

    def __init__(self):
        self.events = EVENTS

    def get_event(self, event_id):
        """Retrieve an event by ID"""
        return self.events.get(event_id, None)

    def process_choice(self, event_id, choice_index):
        """Process a player choice and return next event"""
        event = self.get_event(event_id)
        if not event or choice_index >= len(event['choices']):
            return None

        choice = event['choices'][choice_index]
        return {
            'choice': choice,
            'next_event_id': choice.get('next_event', None)
        }

    def generate_ending(self, stats):
        """Generate ending based on final stats"""
        courage = stats['courage']
        creativity = stats['creativity']
        risk = stats['risk']

        # Determine dominant stat
        max_stat = max(courage, creativity, risk)

        if max_stat == courage:
            return {
                'title': 'The Courageous Echo',
                'text': 'Your journey was defined by bravery and determination. You faced the darkness and emerged transformed. Your echo reverberates with strength.'
            }
        elif max_stat == creativity:
            return {
                'title': 'The Creative Echo',
                'text': 'You crafted your own path through imagination and innovation. The world reshapes itself around your vision. Your echo inspires creation.'
            }
        else:
            return {
                'title': 'The Reckless Echo',
                'text': 'You pushed boundaries and embraced uncertainty. The path was unpredictable but ultimately transformative. Your echo thrums with wild possibility.'
            }

    def get_all_events(self):
        """Return all events (useful for debugging)"""
        return self.events
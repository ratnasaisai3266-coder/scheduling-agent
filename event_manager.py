class Event:
    def __init__(self, event_id, title, start_time, end_time):
        self.event_id = event_id
        self.title = title
        self.start_time = start_time
        self.end_time = end_time

events = []

def create_event(event_id, title, start_time, end_time):
    if check_conflict(start_time, end_time):
        raise Exception("Event conflicts with an existing event.")
    event = Event(event_id, title, start_time, end_time)
    events.append(event)

def read_event(event_id):
    for event in events:
        if event.event_id == event_id:
            return event
    raise Exception("Event not found.")

def update_event(event_id, title=None, start_time=None, end_time=None):
    event = read_event(event_id)
    if title:
        event.title = title
    if start_time or end_time:
        if check_conflict(start_time, end_time):
            raise Exception("Event conflicts with an existing event.")
        if start_time:
            event.start_time = start_time
        if end_time:
            event.end_time = end_time

def delete_event(event_id):
    global events
    events = [event for event in events if event.event_id != event_id]


def check_conflict(start_time, end_time):
    for event in events:
        if (start_time < event.end_time) and (end_time > event.start_time):
            return True
    return False

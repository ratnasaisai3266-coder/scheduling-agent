import click
from event_manager import EventManager
from calendar_integration import GoogleCalendarIntegration
from config import Config

class SchedulingAgent:
    def __init__(self):
        self.config = Config()
        self.event_manager = EventManager()
        self.calendar_integration = GoogleCalendarIntegration(self.config)
    
    def create_event(self, title, description, start_time, end_time, timezone='UTC'):
        """Create a new calendar event"""
        event = {
            'title': title,
            'description': description,
            'start_time': start_time,
            'end_time': end_time,
            'timezone': timezone
        }
        event_id = self.event_manager.create_event(event)
        self.calendar_integration.sync_to_google(event_id, event)
        return event_id
    
    def update_event(self, event_id, **kwargs):
        """Update an existing event"""
        self.event_manager.update_event(event_id, kwargs)
        event = self.event_manager.get_event(event_id)
        self.calendar_integration.sync_to_google(event_id, event)
    
    def delete_event(self, event_id):
        """Delete an event"""
        self.event_manager.delete_event(event_id)
        self.calendar_integration.delete_from_google(event_id)
    
    def list_events(self, limit=10):
        """List all events"""
        return self.event_manager.list_events(limit)
    
    def get_event(self, event_id):
        """Get a specific event"""
        return self.event_manager.get_event(event_id)

@click.group()
def cli():
    """Calendar Event Scheduling Agent"""
    pass

agent = SchedulingAgent()

@cli.command()
@click.option('--title', prompt='Event title', help='Title of the event')
@click.option('--description', prompt='Event description', help='Description of the event')
@click.option('--start', prompt='Start time (YYYY-MM-DD HH:MM)', help='Start time')
@click.option('--end', prompt='End time (YYYY-MM-DD HH:MM)', help='End time')
@click.option('--timezone', default='UTC', help='Timezone for the event')
def create(title, description, start, end, timezone):
    """Create a new calendar event"""
    try:
        event_id = agent.create_event(title, description, start, end, timezone)
        click.echo(f'✓ Event created successfully with ID: {event_id}')
    except Exception as e:
        click.echo(f'✗ Error creating event: {str(e)}')

@cli.command()
@cli.command()
@click.argument('event_id')
@click.option('--title', help='New event title')
@click.option('--description', help='New description')
@click.option('--start', help='New start time')
@click.option('--end', help='New end time')
def update(event_id, title, description, start, end):
    """Update an existing event"""
    try:
        updates = {}
        if title:
            updates['title'] = title
        if description:
            updates['description'] = description
        if start:
            updates['start_time'] = start
        if end:
            updates['end_time'] = end
        
        agent.update_event(event_id, **updates)
        click.echo(f'✓ Event {event_id} updated successfully')
    except Exception as e:
        click.echo(f'✗ Error updating event: {str(e)}')

@cli.command()
@click.argument('event_id')
def delete(event_id):
    """Delete an event"""
    try:
        agent.delete_event(event_id)
        click.echo(f'✓ Event {event_id} deleted successfully')
    except Exception as e:
        click.echo(f'✗ Error deleting event: {str(e)}')

@cli.command()
@click.option('--limit', default=10, help='Number of events to display')
def list(limit):
    """List all calendar events"""
    try:
        events = agent.list_events(limit)
        if not events:
            click.echo('No events found')
            return
        
        click.echo(f'\n📅 Events (showing {len(events)} of {limit}):')
        click.echo('-' * 80)
        for event in events:
            click.echo(f"ID: {event.get('id')}")
            click.echo(f"Title: {event.get('title')}")
            click.echo(f"Description: {event.get('description')}")
            click.echo(f"Start: {event.get('start_time')}")
            click.echo(f"End: {event.get('end_time')}")
            click.echo('-' * 80)
    except Exception as e:
        click.echo(f'✗ Error listing events: {str(e)}')

@cli.command()
@click.argument('event_id')
def get(event_id):
    """Get details of a specific event"""
    try:
        event = agent.get_event(event_id)
        if not event:
            click.echo(f'Event {event_id} not found')
            return
        
        click.echo(f'\n📅 Event Details:')
        click.echo('-' * 80)
        click.echo(f"ID: {event.get('id')}")
        click.echo(f"Title: {event.get('title')}")
        click.echo(f"Description: {event.get('description')}")
        click.echo(f"Start: {event.get('start_time')}")
        click.echo(f"End: {event.get('end_time')}")
        click.echo(f"Timezone: {event.get('timezone', 'UTC')}")
        click.echo('-' * 80)
    except Exception as e:
        click.echo(f'✗ Error getting event: {str(e)}')

if __name__ == '__main__':
    cli()
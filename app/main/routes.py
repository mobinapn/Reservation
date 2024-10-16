from flask import render_template
from app.main import bp



@bp.route('/')
def index():
    form = EventFilterForm(request.args)
    events = Event.query
    
    # Apply filters
    if form.place.data:
        events = events.filter(Event.place.contains(form.place.data))
    if form.start_date.data and form.end_date.data:
        events = events.filter(Event.begin_date >= form.start_date.data, Event.end_date <= form.end_date.data)
    if form.min_price.data:
        events = events.filter(Event.price >= form.min_price.data)
    if form.max_price.data:
        events = events.filter(Event.price <= form.max_price.data)
    if form.min_rate.data:
        events = events.filter(Event.rate >= form.min_rate.data)
    if form.max_rate.data:
        events = events.filter(Event.rate <= form.max_rate.data)
    if form.min_capacity.data:
        events = events.filter(Event.capacity >= form.min_capacity.data)
    if form.max_capacity.data:
        events = events.filter(Event.capacity <= form.max_capacity.data)
    
    events = events.all()
    return render_template('home.html', events=events, form=form)


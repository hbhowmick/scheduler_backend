from app import app, db
from flask import  request, jsonify
from app.models import Event


# set index route to return nothing, just so no error
@app.route('/')
def index():
    return ''


@app.route('/api/save', methods=['GET', 'POST'])
def save():
    try:
        # get headers first
        day = request.headers.get('day')
        month = request.headers.get('month')
        year = request.headers.get('year')
        title = request.headers.get('title')
        notes = request.headers.get('notes')

        # if not all exist, return error
        if not day and not month and not year and not title and not notes:
            return jsonify({'error': 'Invalid params'})

        # create an event
        event = Event(day=day, month=month, year=year, title=title, notes=notes)

        # add and commit to db
        db.session.add(event)
        db.session.commit()

        return jsonify({'success': 'Saved event'})

    except:
        return jsonify({'error': 'Invalid params, did not save'})

@app.route('/api/retrieve', methods=['GET', 'POST'])
def retrieve():
    try:
        day = request.headers.get('day')
        month = request.headers.get('month')
        year = request.headers.get('year')

        if not day and month and year:
            results = Event.query.filter_by(month=month, year=year).all()
        elif not day and not month and year:
            results = Event.query.filter_by(year=year).all()
        else:
            results = Event.query.filter_by(year=year, month=month, day=day).all()

        # check if no events
        if results == []:
            return jsonify({'success': 'No events today'})

        parties = []

        # loop through results and add each event to party
        for result in results:
            party = {
                'title': result.title,
                'day': result.day,
                'month': result.month,
                'year': result.year,
                'notes': result.notes,
                'event_id': result.event_id
            }

            parties.append(party)

        return jsonify(parties)

    except:
        return jsonify({'error': 'Incorrect headers'})


@app.route('/api/delete', methods=['GET', 'POST'])
def delete():
    try:
        event_id = request.headers.get('event_id')

        event = Event.query.filter_by(event_id=event_id).first()

        db.session.delete(event)
        db.session.commit()

        return jsonify({'success': 'Event deleted'})

    except:
        return jsonify({'error': 'Event not removed, try again'})

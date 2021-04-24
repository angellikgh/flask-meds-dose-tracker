from tracker import app


@app.route('/')
def index():
    return 'Hello Dose Tracker'

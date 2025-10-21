from server import create_app
from server.models import db

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db}

if __name__ == '__main__':
    # Only runs locally, not in production
    app.run(debug=False, port=5000)  # Change debug to False
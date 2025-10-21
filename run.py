	
from app import create_app
from app.server.models import db

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db}

if name == 'main':

# Only runs locally, not in production
app.run(debug=True, port=5000)
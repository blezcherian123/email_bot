from flask import Flask, render_template, request, flash
from agent import run_agent
import sys
from io import StringIO

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for flash messages

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            # Capture console output
            output = StringIO()
            sys.stdout = output
            
            run_agent()
            
            # Restore standard output
            sys.stdout = sys.__stdout__
            
            # Get the captured output
            processing_log = output.getvalue()
            
            # Split the log into lines and create formatted HTML
            log_lines = processing_log.split('\n')
            formatted_log = '<br>'.join(log_lines)
            
            flash(f'Email processing completed. Details:<br>{formatted_log}', 'success')
        except Exception as e:
            flash(f'Error occurred: {str(e)}', 'error')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
from bank_management import create_app
FLASK_APP = 'run.py'
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

# source venv/bin/activate : activates virtual environment
# deactivate : deactivates virtual environment

from app import app


if __name__=="__main__":
    app.run(port=3000,debug=True)

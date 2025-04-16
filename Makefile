# Activate the virtual environment
namespace:
	source myenv/bin/activate

# Stop the Gunicorn server
stop:
	pkill gunicorn

# Start the Gunicorn server
start:
	gunicorn -w 1 app:app --daemon --log-file 1.logfile.log --reload

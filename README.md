# gpxStravaFaker
changes the date and time of a strava gpx


# INSTALLATION
pip install -r requirements.txt

# USAGE
just run the script, it will ask you to input the filename to the gpx files.
then it will ask you to input a date and time in [YYYY-MM-DDThh:mm:ssZ] this format (example: 2020-12-12T16:30:03Z)

the avg speeds and activity length will remain the same, but the start time will change and all the others will follow.

# WARNING 
will not work on multi-day activities

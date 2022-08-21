# hrs-calendar
Horse Riding School appointment service, based on websockets served by django-channels (dockerized)

This will be my new personal project, which, if it works out fine, I plan to gift to my family (they run a horse riding school and prefer to stick to 'old-school' scheduling books, having to copy those manually). Django channels should provide transparency, so that every client coming to visit the app, will see up-to-date state of affairs and should be able to book his/her appointment using one of available slots.


### NOTE (20.08.2022):
Please bear in mind this project will serve me as a bit of a playground, since I do not have previous experience with Docker and intend to experiment a little with django-channels, hence I anticipate the development pace to be rather slow (for the next few days I will probably do a little digging and try out some tutorials on Docker before I start 'for good'). :)

### Updates:
I am running this project using Windows Subsystem for Linux (WSL2), so you may use different tools to start.

Prerequisites:
1. Essential knowledge:
* https://docs.microsoft.com/en-us/windows/wsl/setup/environment - Microsoft official guidelines to setup a WSL environment with docker, postgres db and so on
* https://dev.to/drack112/setup-a-django-project-with-docker-128f - an article I based my setup on
* please make sure your user has proper permissions for the files (especially the entrypoint.sh executable), as if it doesn't, the server won't start!

2. Install Python 3.10 (https://www.python.org/downloads/release/python-3100/) and make sure it is added to PATH
3. Install Docker Desktop for your OS (https://www.docker.com/get-started/) - if running on WSL, make sure you've read the guide from previous step.
4. Install VSCode (https://code.visualstudio.com/) - optional
5. Review .env++ file, populate it with your own credentials - remember to paste your django SECRET_KEY! Also, maybe you will have to create a PostgreSQL database if it does not exist yet. Once that's done, rename the file to .env
6. Run command "docker-compose up --build -V" from your debian distro terminal.

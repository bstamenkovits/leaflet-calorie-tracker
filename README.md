# Leaflet Calorie Tracker

This is a simple web-app hobby project, currently a work-in-progress.


## Deployment
This application is designed to be deployed/published using [Render](https://render.com/), a service for hosting a wide variety of web applications. This application is deployed as a "WebService" in Render, you only need to configure a couple of things on their website:
* Link a GitHub account, and point the WebService to this GitHub repo
* Set the build command as `bash build.sh`
* Set the run command as `bash run.sh`
* Configure the correct environment variables

## Installation - Local Development
### Prerequisites
* Python 3.11
* Node 20.11+

### Frontend
The frontend runs on Angular. To run this locally all you need to do is install all the frontend (NodeJS) related dependencies there. No need to create any environments, node manages this on its own. Start by opening a terminal in the root directory and follow the following steps:
1) Navigate to frontend `src` folder
```bash
cd frontend/src
```
2) Install dependencies
```bash
npm install
```

### Backend
The backend runs on FastAPI. To run this locally it is adviced to create a virtual environment and install all backend (Python) related dependencies there. Start by opening a terminal in the root directory and follow the following steps:

1) Navigate to backend folder
```bash
cd backend
```

2) Create a Python virtual environment
```bash
python -m venv .venv
```

3) Activate virtual environment
```bash
# windows
.venv/scripts/activate

# mac/linux
source .venv/bin/activate
```

4) Install dependencies
```bash
pip install -r requirements.txt
```




## Run - Local Development
This section describes how to run the application after all of the dependencies have been installed  (see previous section).

### Frontend
Any time any changes are made to the frontend, it's important to build/compile the Angular scripts into the relevant HTML, CSS, and JavaScript files that will be served to the user's browser. Open a new terminal in the root directory and follow the following steps:

1) Navigate to the frontend directory
```bash
cd frontend
```

2) Build the distributable `dist` directory (optionally add the `--watch` flag to automatically build whenver any changes to the source code are detected)
```bash
ng build --watch
```

### Backend
After the frontend has been built (see previous section), the backend application can be spun up. This backend FastAPI application will mount the relevant frontend files found in the Frontend `dist` directory, allowing the website to be accessed directly from the FastAPI instance.

#### Option 1: Run Normally
Open a new terminal in the root directory and follow the following steps:
1) Navigate to the backend folder
```bash
cd backend
```
2) Make sure the virtual environment is active
```bash
# windows
.venv/scripts/activate

# mac/linux
source .venv/bin/activate
```
3) Run the FastAPI application using Python
```bash
python src/app.py
```

#### Option 2: Use VSCode Debugger
Go to the "RUN AND DEBUG", select "FastAPI" from the dropdown menu and press the green play button.


## Documentation
For further documentation please see the [`docs`](./docs/) folder. The table below contains links to the various relevant documentation files.

| File | Description |
| -- | -- |
| [`auth.md`](./docs/auth.md) | Describes how authentication (using Google's OAuth2.0 client) is implemented in this web application |

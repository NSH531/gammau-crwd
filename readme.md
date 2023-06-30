Sure! Here's an updated README.md file with the specified app name:


# gammau-crwd - README

This repository contains a Django web application named "gammau-crwd". The application includes views for rendering different pages, handling form submissions, and executing scripts on remote hosts using the CrowdStrike FalconPy library.

## Prerequisites

Before running the web application, make sure you have the following prerequisites installed:

- Python 3.x: Visit the official Python website (https://www.python.org) and download the latest version of Python for your operating system. Follow the installation instructions to set up Python.

## Getting Started

To run the "gammau-crwd" Django web application, follow the steps below:

1. Clone or download this repository to your local machine.

2. Open a command prompt or terminal.

3. Navigate to the root directory of the cloned/downloaded repository using the `cd` command. For example:
   ```
   cd /path/to/gammau-crwd
   ```

4. Create a virtual environment to isolate the project dependencies. Run the following command:
   ```
   python -m venv env
   ```

5. Activate the virtual environment. The activation command depends on your operating system:
   - Windows:
     ```
     env\Scripts\activate.bat
     ```
   - macOS/Linux:
     ```
     source env/bin/activate
     ```

6. Install the project dependencies by running the following command:
7. 
   ```
   pip install -r requirements.txt
   ```

8. Configure the Django project's settings by renaming the `example.settings.py` file to `settings.py` located in the `app` directory.

9. Run database migrations to create the necessary database tables:
   ```shell
   python manage.py migrate
   ```

10. Start the Django development server:
   ```shell
   python manage.py runserver
   ```

11. Open a web browser and visit http://localhost:8000 to access the "gammau-crwd" web application.

## Functionality

The "gammau-crwd" Django web application provides the following functionality:

- Home Page: Renders the home page template (`app/index.html`).
- Contact Page: Renders the contact page template (`app/contact.html`).
- About Page: Renders the about page template (`app/about.html`).
- Credentials Page: Handles a form submission to retrieve an API key and secret. Generates an access token using the provided credentials and renders the `app/creds.html` template.
- Execute Script: Handles a form submission to execute a script on remote hosts. Retrieves the access token and other parameters, interacts with the CrowdStrike Falcon platform using the FalconPy library, and prints the result to the console.
- Main Page: Renders the main template (`app/main.html`).

## Configuration

The Django project's configuration is stored in the `settings.py` file located in the `app` directory. Update the configuration settings as needed for your environment.

## Dependencies

The project dependencies are listed in the `requirements.txt` file. The required packages will be installed when running `pip install -r requirements.txt`.

## Contributing

Contributions are welcome! If you find any issues or want to add new features, feel free to open a pull request.

## License

This project is licensed under the [MIT License](LICENSE).


Please note that the instructions provided assume you are using a command prompt or terminal. Make sure to replace `/path/to/gammau-crwd` with the actual path to the cloned or downloaded repository on your machine.

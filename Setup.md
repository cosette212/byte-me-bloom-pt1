Local Setup Guide
Step 1
Once the ZIP file containing the trained models has been downloaded, its contents must be placed inside the 'Predict' folder.

Step 2
After placing the files, open the main project folder named 'HACKATON2025' using a code editor (e.g., Visual Studio Code).

Step 3
Open the terminal and run the following command to activate the virtual environment, which includes all necessary packages and libraries for the web application to function properly: Step 1
Once the ZIP file containing the trained models has been downloaded, its contents must be placed inside the 'Predict' folder.

Step 2
After placing the files, open the main project folder named 'HACKATON2025' using a code editor (e.g., Visual Studio Code).

Step 3
Open the terminal and run the following command to activate the virtual environment, which includes all necessary packages and libraries for the web application to function properly:Step 1
Once the ZIP file containing the trained models has been downloaded, its contents must be placed inside the 'Predict' folder.

Step 2
After placing the files, open the main project folder named 'HACKATON2025' using a code editor (e.g., Visual Studio Code).

Step 3
Open the terminal and run the following command to activate the virtual environment, which includes all necessary packages and libraries for the web application to function properly:Step 1
Once the ZIP file containing the trained models has been downloaded, its contents must be placed inside the 'Predict' folder.

Step 2
After placing the files, open the main project folder named 'HACKATON2025' using a code editor (e.g., Visual Studio Code).

Step 3
Open the terminal and run the following command to activate the virtual environment, which includes all necessary packages and libraries for the web application to function properly:venv/Scripts/activate/ps1After executing this command, you should see the label '(venv)' in green on the left side of the terminal prompt. If this appears, proceed to the next step.

Step 4
If the folders are correctly placed and the virtual environment is activated, you can now start the local development server using the runserver command.

First, navigate to the 'hackaton2025' folder (note: this is different from 'HACKATON2025'; it is the direct project folder) by running:cd hackaton2025Then, start the server with the following command:python manage.py runserverStep 5
The command may take a few seconds to execute. You will see some warnings, but look for the following output:System check identified 1 issue (0 silenced).

You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
October 05, 2025 - 22:42:26
Django version 5.2.7, using settings 'hackaton2025.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.

WARNING: This is a development server. Do not use it in a production setting. Use a production WSGI or ASGI server instead.
For more information on production servers see: https://docs.djangoproject.com/en/5.2/howto/deployment/Within this output, locate the line:Starting development server at http://127.0.0.1:8000/Click Ctrl + Click on the URL http://127.0.0.1:8000/ to open the local server in your browser.

And that’s it — the setup is complete. les parece?? ustedes diganme

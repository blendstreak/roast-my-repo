# Roast My Repo

This project is a modern web application built using the Django framework in Python. It's designed to serve dynamic content, showcasing interactive elements or generated text. The application leverages SQLite for its database needs and integrates TailwindCSS for a utility-first approach to styling, providing a sleek and responsive user interface for displaying its content.
Get your repo roasted by AI and generate README for it. 
## Tech Stack

The core technologies and tools used in this project include:

*   **Backend Framework**: [Django](https://www.djangoproject.com/)
*   **Programming Language**: [Python 3.12](https://www.python.org/)
*   **Database**: [SQLite3](https://www.sqlite.org/index.html)
*   **Frontend Styling**: [Tailwind CSS](https://tailwindcss.com/)
*   **Frontend Build Tool**: [Tailwind CSS CLI](https://tailwindcss.com/docs/installation/cli)
*   **Package Managers**: `pip` (for Python dependencies), `npm` (for Node.js/frontend dependencies)

## Installation

Follow these steps to set up and run the project locally.

### Prerequisites

Ensure you have the following installed on your system:

*   [Python 3.12+](https://www.python.org/downloads/)
*   [Node.js and npm](https://nodejs.org/en/download/)

### Steps

1.  **Clone the Repository**
    If you haven't already, clone the project repository to your local machine:

    ```bash
    git clone https://github.com/blendstreak/roast-my-repo
    cd roast-my-repo
    ```

2.  **Set up Python Virtual Environment**
    It's highly recommended to use a virtual environment to manage Python dependencies to avoid conflicts with other projects.

    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Python Dependencies**
    Install all required Python packages listed in `requirements.txt`.

    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Node.js Dependencies (For development, just for tailwindcss)**
    Install frontend-related packages, including the Tailwind CSS CLI.
    

    ```bash
    npm install
    ```

6.  **Compile Tailwind CSS**
    Generate the production-ready CSS file from your Tailwind input.

    ```bash
    npx tailwindcss -i ./static/css/input.css -o ./static/css/styles.css --minify
    ```

    *For development with live reloading, you can use the `--watch` flag:*
    ```bash
    npx tailwindcss -i ./static/css/input.css -o ./static/css/styles.css --watch
    ```

7.  **Apply Database Migrations**
    Set up the database schema for the project.

    ```bash
    python manage.py migrate
    ```

8.  **Run the Development Server**
    Start the Django development server to access the application.

    ```bash
    python manage.py runserver
    ```

    The application should now be accessible in your web browser at `http://127.0.0.1:8000/`.

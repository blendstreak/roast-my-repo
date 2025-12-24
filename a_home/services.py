import requests
import os
from google import genai
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
if not GEMINI_API_KEY:
    raise ValueError("No API Key found! Check your .env file.")

client = genai.Client()

def format_file_tree(files):
    if not files:
        return ""

    paths = [f['path'] for f in files]
    paths.sort()
    return "\n".join(paths[:50])

def get_dependency_file(owner, repo, files):
    target_files = ['requirements.txt', 'package.json', 'Pipfile', 'pyproject.toml']
    found_file = None

    for file_obj in files:
        if file_obj['path'] in target_files:
            found_file = file_obj['path']
            break
    if not found_file:
        return "No dependency file found."

    raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/{found_file}"
    response = requests.get(raw_url, headers=headers)

    if response.status_code != 200:
        raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/master/{found_file}"
        response = requests.get(raw_url, headers=headers)

    if response.status_code == 200:
        return f"File: {found_file}\nContent\n{response.text[:1000]}"

    return "Could not fetch dependency content."

def generate_roast_and_readme(file_tree, dependencies):
    prompt = f"""
    You are a rude, cynical senior software engineer.

    I am giving you the file structure and dependencies of a Github repository.

    TASK 1: Roast the user based on their tech stack, Be brief (max 2 senteces) and mercilessly funny.
    TASK2: Suggest a professional Title for the README.

    DATA:
    ---
    File Structure:
    {file_tree}

    Dependencies:
    {dependencies}

    OUTPUT FORMAT:
    Please output your response strictly in this format:
    ROAST: [Your roast here]
    README_TITLE: [Your title here]
    """

    try:

        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        print(response.text)
        return response.text
    except Exception as e:
        print(f"API ERROR: {e}")
        return "ROAST: The AI is judging you silently (API Error). \nREADME_TITLE: Error"

def generate_full_readme(file_tree, dependencies):
    prompt = f"""
    You are an expert Technical Writer.

    I am giving you the file structure and dependencies of a software project.

    Task: Write a professional, complete README.md file for this project.

    REQUIREMENTS:
    1. Use a clear H1 Title.
    2. Write a 1-paragraph overview of what the project likely does.
    3. Create a "Tech Stack" section based on the dependencies.
    4. Write "Installation" instructions (guess the commands based on the language, e.g., pip install vs npm install).
    5. Output ONLY the raw Markdown code. Do not wrap it in ```
    markdown``` code blocks.

    DATA:
    File Structure:
    {file_tree}

    Dependencies:
    {dependencies}
    """
    try:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return response.text

    except Exception as e:
        return f"#Error\nCould not generate README: {e}"


def parse_ai_response(raw_text):
    
    result = {'roast': 'Roast generation failed', 'title': 'Project Title'}

    try:
        parts = raw_text.split("README_TITLE:")
        
        if len(parts) == 2:
            result['roast'] = parts[0].replace("ROAST:", "").strip()
            result['title'] = parts[1].strip()
        else:
            result['roast'] = raw_text.replace("ROAST:", "").strip()

    except Exception as e:
        print(f"Parsing Error: {e}")

    return result



def get_repo_details(url):
    parsed = urlparse(url)
    path_parts = parsed.path.strip("/").split("/")
    
    if len(path_parts) < 2:
        return None, None

    owner = path_parts[0]
    repo = path_parts[1]
    return owner, repo

def fetch_file_tree(owner,repo):
    api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        return data.get('tree', [])
    elif response.status_code == 404:
        api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/master?recursive=1"
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            return response.json().get('tree', [])

    return None

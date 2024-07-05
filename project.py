import os
import json
from typing import Dict, List, Union

EXCLUDED_DIRS = {'node_modules', 'venv', '.git', '__pycache__', 'migrations', 'build'}
IMPORTANT_FILE_TYPES = {'.py', '.js', '.jsx', '.ts', '.tsx', '.json', '.yml', '.yaml', '.md', '.html', '.css'}
KEY_FILES_DJANGO = {'models.py', 'views.py', 'urls.py', 'settings.py', 'serializers.py', 'forms.py', 'admin.py'}
KEY_FILES_REACT = {'.jsx', '.js'}

def analyze_project(root_dir: str) -> Dict[str, Union[List[Dict[str, str]], Dict[str, str]]]:
    project_structure = {"files": [], "directories": [], "analysis": {}}

    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]

        rel_path = os.path.relpath(dirpath, root_dir)
        if rel_path != '.':
            project_structure["directories"].append({
                "path": rel_path,
                "name": os.path.basename(dirpath)
            })

        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            rel_file_path = os.path.relpath(file_path, root_dir)

            file_info = analyze_file(file_path, rel_file_path)
            project_structure["files"].append(file_info)

    project_structure["analysis"] = analyze_project_structure(project_structure)
    return project_structure

def analyze_file(file_path: str, rel_file_path: str) -> Dict[str, str]:
    file_info = {
        "name": os.path.basename(file_path),
        "path": rel_file_path,
        "size": os.path.getsize(file_path),
        "type": get_file_type(file_path)
    }

    file_extension = os.path.splitext(file_path)[1]

    if file_info["type"] == "text" and (file_info["name"] in KEY_FILES_DJANGO or file_extension in KEY_FILES_REACT):
        file_info["content"] = get_full_file_content(file_path)
        file_info["line_count"] = len(file_info["content"].splitlines())
    elif file_info["type"] == "text" and file_extension in IMPORTANT_FILE_TYPES:
        file_info["content_preview"] = get_file_content_preview(file_path)
        file_info["line_count"] = file_info["content_preview"].count('\n') + 1

    return file_info

def get_file_type(filename: str) -> str:
    ext = os.path.splitext(filename)[1].lower()
    if ext in IMPORTANT_FILE_TYPES:
        return "text"
    elif ext in ['.jpg', '.png', '.gif', '.svg', '.ico']:
        return "image"
    else:
        return "other"

def get_full_file_content(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def get_file_content_preview(file_path: str, max_lines: int = 10) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return '\n'.join(f.readlines()[:max_lines])
    except Exception as e:
        return f"Error reading file: {str(e)}"

def analyze_project_structure(project_structure: Dict) -> Dict[str, str]:
    analysis = {}

    # Check for Django
    if any(f["name"] == "manage.py" for f in project_structure["files"]):
        analysis["framework"] = "Django"
        analysis["django_apps"] = [d["name"] for d in project_structure["directories"] if "apps.py" in [f["name"] for f in project_structure["files"] if f["path"].startswith(d["path"])]]

    # Check for React
    if any(f["name"] == "package.json" and "react" in f.get("content_preview", "") for f in project_structure["files"]):
        analysis["frontend"] = "React"

    return analysis

def main():
    project_root = input("Enter the root directory of your project: ")
    output_file = input("Enter the output JSON file name: ")

    project_structure = analyze_project(project_root)

    with open(output_file, 'w') as f:
        json.dump(project_structure, f, indent=2)

    print(f"Project structure analysis saved to {output_file}")

if __name__ == "__main__":
    main()

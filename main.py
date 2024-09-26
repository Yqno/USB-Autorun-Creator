import os

def to_lowercase(text: str) -> str:
    """Convert a string to lowercase."""
    return text.lower()

def get_input() -> tuple[str, str]:
    """Prompt the user for directory path and filename."""
    base_path = input("Enter the full path of the directory where your file is saved: ").strip()
    target_filename = input("Enter the name of the file you want to make an autorun file: ").strip()
    return base_path, target_filename

def validate_file_path(base_path: str, target_filename: str) -> str:
    """Construct the full path of the target file and check if it exists."""
    target_path = os.path.join(base_path, target_filename)
    if not os.path.isfile(target_path):
        raise FileNotFoundError(f"The file '{target_filename}' does not exist at the specified path '{base_path}'.")
    return target_path

def generate_autorun_content(filename: str) -> str:
    """Generate the content for the autorun.inf file based on file extension."""
    ext = to_lowercase(filename)

    # Define file type mappings
    file_type_actions = {
        ".exe": lambda f: f"[autorun]\nOpen={f}\nUseAutoPlay=1",
        ".zip": lambda f: f"[autorun]\nShellExecute=explorer.exe {f}\nUseAutoPlay=1",
        ".bat": lambda f: f"[autorun]\nShellExecute={f}\nUseAutoPlay=1",
        ".py": lambda f: f"[autorun]\nShellExecute=pythonw.exe {f}\nUseAutoPlay=1",
        ".jar": lambda f: f"[autorun]\nShellExecute=javaw.exe -jar {f}\nUseAutoPlay=1",
        ".ps1": lambda f: f"[autorun]\nShellExecute=powershell.exe -ExecutionPolicy Bypass -File {f}\nUseAutoPlay=1"
    }
    
    # Image file extensions
    image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".gif")
    if ext.endswith(image_extensions):
        return f"[autorun]\nShellExecute={filename}\nUseAutoPlay=1"

    # Check for exact match, including hidden files
    if ext in file_type_actions:
        return file_type_actions[ext](filename)

    # Check if the filename starts with a dot for hidden files
    if ext.startswith("."):
        # Here, just use ShellExecute directly for hidden files without creating an entry
        return f"[autorun]\nOpen={filename}\nUseAutoPlay=1"

    raise ValueError("Unsupported file type. Please use an executable, ZIP file, image, Python script, Java JAR, CMD batch file, or PowerShell script.")

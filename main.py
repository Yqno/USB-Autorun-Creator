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
        (".jpg", ".jpeg", ".png", ".bmp", ".gif"): lambda f: f"[autorun]\nShellExecute={f}\nUseAutoPlay=1",
        ".py": lambda f: f"[autorun]\nShellExecute=pythonw.exe {f}\nUseAutoPlay=1",
        ".jar": lambda f: f"[autorun]\nShellExecute=javaw.exe -jar {f}\nUseAutoPlay=1",
        ".bat": lambda f: f"[autorun]\nShellExecute={f}\nUseAutoPlay=1",
        ".ps1": lambda f: f"[autorun]\nShellExecute=powershell.exe -ExecutionPolicy Bypass -File {f}\nUseAutoPlay=1"
    }

    # Check for exact match
    for key, action in file_type_actions.items():
        if isinstance(key, tuple):
            if ext.endswith(key):
                return action(filename)
        elif ext.endswith(key):
            return action(filename)
    
    raise ValueError("Unsupported file type. Please use an executable, ZIP file, image, Python script, Java JAR, CMD batch file, or PowerShell script.")

def create_autorun_file(base_path: str, content: str) -> None:
    """Create or overwrite the autorun.inf file in the specified directory."""
    autorun_path = os.path.join(base_path, "autorun.inf")
    
    if os.path.exists(autorun_path):
        overwrite = input("Warning: 'autorun.inf' already exists. Do you want to overwrite it? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("Operation canceled.")
            return

    try:
        with open(autorun_path, 'w') as file:
            file.write(content)
        print(f"'autorun.inf' file created successfully at {base_path}.")
    except Exception as e:
        print(f"Error: Could not create 'autorun.inf' file. {str(e)}")

def main():
    """Main function to handle user inputs and create the autorun.inf file."""
    base_path, target_filename = get_input()
    
    try:
        validate_file_path(base_path, target_filename)
        autorun_content = generate_autorun_content(target_filename)
        create_autorun_file(base_path, autorun_content)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

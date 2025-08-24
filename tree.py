import os

IGNORE_FOLDERS = {"renenv", "__pycache__", ".git", ".idea", ".vscode"}

def print_tree(start_path, prefix="", file=None):
    try:
        files = sorted(os.listdir(start_path))
    except PermissionError:
        return
    for idx, f in enumerate(files):
        path = os.path.join(start_path, f)
        if os.path.isdir(path) and f in IGNORE_FOLDERS:
            continue  # skip ignored folders
        connector = "└── " if idx == len(files) - 1 else "├── "
        line = prefix + connector + f
        print(line)
        if file:
            file.write(line + "\n")
        if os.path.isdir(path):
            extension = "    " if idx == len(files) - 1 else "│   "
            print_tree(path, prefix + extension, file)

if __name__ == "__main__":
    root = os.getcwd()
    output_file = "folder_structure.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        title = os.path.basename(root) + "/"
        print(title)
        f.write(title + "\n")
        print_tree(root, file=f)
    print(f"\n✅ Folder structure saved to {output_file}")

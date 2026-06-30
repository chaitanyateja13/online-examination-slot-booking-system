import os

def print_tree(directory, prefix="", file=None):
    exclude_dirs = {'venv', '__pycache__', '.git', 'migrations', '.env'}
    if not os.path.isdir(directory):
        return
        
    entries = sorted(os.listdir(directory))
    entries = [e for e in entries if e not in exclude_dirs and not e.endswith('.pyc') and e not in ('structure.txt', 'structure_utf8.txt', 'clean_tree.txt', 'project_structure.txt')]
    
    for i, entry in enumerate(entries):
        path = os.path.join(directory, entry)
        is_last = (i == len(entries) - 1)
        
        connector = "└── " if is_last else "├── "
        file.write(f"{prefix}{connector}{entry}\n")
        
        if os.path.isdir(path):
            extension = "    " if is_last else "│   "
            print_tree(path, prefix + extension, file=file)

with open('project_structure.txt', 'w', encoding='utf-8') as f:
    f.write("exam_system/\n")
    print_tree('.', file=f)

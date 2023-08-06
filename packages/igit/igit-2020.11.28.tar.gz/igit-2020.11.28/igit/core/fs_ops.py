from pathlib import Path

# TODO - refactor into object

# input - base path, exclude directories, exclude files
# output - list of all files that are not excluded or in excluded directories


def in_stem(fs_element, excluded_dirs):
    for parent in fs_element.parents:
        if parent in excluded_dirs:
            return True
    return False


def get_files(base_path, excluded_dirs=None, excluded_files=None, files_only=True):
    files = []
    for file in base_path.rglob('*'):
        file_rel_path = file.relative_to(base_path)
        if not in_stem(file_rel_path, excluded_dirs) \
                and file_rel_path not in excluded_files \
                and file.is_file() if files_only else True:
            files.append(file_rel_path)
    return files

if __name__ == "__main__":

    dir_path = '/Users/kobarhan/workspace/igit_test'
    repo_path = Path(dir_path)

    ex_dirs = [Path(ex_dir) for ex_dir in ['.git']]
    ex_files = [Path(ex_file) for ex_file in ['data3.txt']]

    files_objects = get_files(repo_path, ex_dirs, ex_files)
    print(files_objects)

    files_objects = [str(file) for file in files_objects]
    print(files_objects)

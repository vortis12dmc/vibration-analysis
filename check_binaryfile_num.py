import os

def count_bin_files_in_subdirs(directory):
    """
    Count the number of .bin files in each subdirectory of the given directory,
    including nested subdirectories.
    """
    for root, dirs, files in os.walk(directory):
        for subdir in dirs:
            subdir_path = os.path.join(root, subdir)
            bin_count = sum(1 for file in os.listdir(subdir_path) if file.endswith('.bin'))
            relative_subdir_path = os.path.relpath(subdir_path, directory)
            print(f"{relative_subdir_path} {bin_count}")

# Replace '/path/to/trains' with the actual path to the 'trains' directory
train_dir = '/2023/v23e3021/Program/ohtakeLab/analyTrainData/trains'
count_bin_files_in_subdirs(train_dir)


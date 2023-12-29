import os
import re
from collections import defaultdict

def time_difference(time1, time2):
    h1, m1, s1 = int(time1[:2]), int(time1[2:4]), int(time1[4:])
    h2, m2, s2 = int(time2[:2]), int(time2[2:4]), int(time2[4:])
    return (h2 - h1) * 3600 + (m2 - m1) * 60 + (s2 - s1)

def list_directories_with_issues(base_directory):
    directories_with_multiple_sets = defaultdict(list)
    directories_with_time_diff_issues = defaultdict(list)

    for root, dirs, files in os.walk(base_directory):
        bin_files = [f for f in files if f.endswith('.bin') and re.match(r"\d{8}_\d{6}_\d_[xyz].bin", f)]

        xyz_count = defaultdict(int)
        for file in bin_files:
            timestamp = re.match(r"(\d{8}_\d{6}_\d)_[xyz].bin", file).group(1)
            xyz_count[timestamp] += 1

        for timestamp, count in xyz_count.items():
            if count >= 3:
                directories_with_multiple_sets[root].append(timestamp)

        times = sorted(xyz_count.keys())
        for i in range(len(times) - 1):
            time_diff = time_difference(times[i].split('_')[1], times[i + 1].split('_')[1])
            if time_diff != 15:
                directories_with_time_diff_issues[root].append((times[i], times[i + 1], time_diff))

    return directories_with_multiple_sets, directories_with_time_diff_issues

base_dir = "../concatTrains"
directories_with_multiple_sets, directories_with_time_diff_issues = list_directories_with_issues(base_dir)

print("\nDirectories with Multiple Sets of x, y, z Files:")
for dir, sets in directories_with_multiple_sets.items():
    print(f"{dir}: {sets}")

print("\nDirectories with Time Difference Issues:")
for dir, issues in directories_with_time_diff_issues.items():
    for issue in issues:
        print(f"{dir}: Times {issue[0]}, {issue[1]} with difference of {issue[2]} seconds")


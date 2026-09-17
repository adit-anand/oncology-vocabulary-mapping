import os
import shutil

# Directory containing Chia annotations
ANNOTATIONS_DIR = "/Users/ara2205/natarajan-lab/eligibility-criteria/ohdsi-2026/data/annotations/chia-files"
TRAIN_DIR = "/Users/ara2205/natarajan-lab/eligibility-criteria/ohdsi-2026/data/annotations/train"
TEST_DIR = "/Users/ara2205/natarajan-lab/eligibility-criteria/ohdsi-2026/data/annotations/test"
# Remove and recreate any existing train/test directories
shutil.rmtree(TRAIN_DIR)
shutil.rmtree(TEST_DIR)
os.mkdir(TRAIN_DIR)
os.mkdir(TEST_DIR)
# Get list of Chia annotation filenames 
file_list = os.listdir(ANNOTATIONS_DIR)
# Get a list of the NCT IDs
nct_ids = set()
for filename in file_list:
    # First 11 characters of the file name contain the NCT ID
    nct_id = filename[0:11]
    nct_ids.add(nct_id)
# Convert set to list
nct_ids = list(nct_ids)
# Designate NCT IDs for training and testing data
train_nct_ids = nct_ids[0:int(len(nct_ids)*0.8)]
test_nct_ids = nct_ids[int(len(nct_ids)*0.8):len(nct_ids)]
# Copy training data files
for nct_id in train_nct_ids:
    # Filter down files relevant to the current trial
    trial_files = [filename for filename in file_list if nct_id in filename]
    # Copy files to the train directory
    for filename in trial_files:
        absolute_filepath = f"{ANNOTATIONS_DIR}/{filename}"
        shutil.copy2(absolute_filepath, TRAIN_DIR)
# Copy testing data files
for nct_id in test_nct_ids:
    # Filter down files relevant to the current trial
    trial_files = [filename for filename in file_list if nct_id in filename]
    # Copy files to the test directory
    for filename in trial_files:
        absolute_filepath = f"{ANNOTATIONS_DIR}/{filename}"
        shutil.copy2(absolute_filepath, TEST_DIR)
import datasets
from datasets import load_dataset, DatasetDict
import os



def split_dataset(dataset_name, subsets, domain_name, split_ratio=0.8, random_seed=42):
    # Loop through each subset and process it
    dataset = load_dataset(dataset_name)
    for subset in subsets:
        print(f"Processing subset: {subset}...")
        sub_dataset = dataset[subset]
        # Split train set into train and test
        train_test_split = sub_dataset.train_test_split(test_size=1 - split_ratio, seed=random_seed)
        # Create a new dataset dictionary with train-test splits
        processed_dataset = DatasetDict({
            "train": train_test_split["train"],
            "test": train_test_split["test"]
        })
        # Define save path
        subset_output_dir = os.path.join(output_dir, domain_name, subset)
        os.makedirs(subset_output_dir, exist_ok=True)
        # Save train and test splits locally
        processed_dataset.save_to_disk(subset_output_dir)
        print(f"Saved {subset} dataset splits to {subset_output_dir}")


if __name__ == "__main__":

    case_name = 'teapotlid/PrivaCI-Bench_cases'
    case_subsets = ['AI_ACT', 'GDPR', 'HIPAA','ACLU']
    output_dir = "checklist_splits" 
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    split_dataset(case_name, case_subsets, domain_name = 'cases')
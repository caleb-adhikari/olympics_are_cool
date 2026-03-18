from datasets import load_dataset

# Load the dataset from the repository, turn it into a pandas dataframe and return it
def load_data():
    dataset = load_dataset("Haider67795/veriseti_20220203_olimpiyatlar",
                           data_files="veriseti_20220203_olimpiyatlar.csv")
    return dataset['train'].to_pandas()

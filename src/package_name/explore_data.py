from package_name.load_data import load_data
def explore():
    """
    Load the Olympics dataset and print basic information
    to understand its structure and quality.
    
    Returns:
        df (pd.DataFrame): The loaded dataset
    """
    
    # Load dataset into a pandas DataFrame
    df = load_data()
    
    # Print number of rows and columns
    print("Shape:", df.shape)
    
    # Print column names
    print("\nColumns:", df.columns)
    
    # Show data types of each column
    print("\nData types:\n", df.dtypes)
    
    # Count missing values in each column
    print("\nMissing values:\n", df.isna().sum())
    
    # Display first few rows of the dataset
    print("\nFirst few rows:\n", df.head())

    return df


# Run the function when the script is executed directly
if __name__ == "__main__":
    explore()
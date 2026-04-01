
import pytest
import pandas as pd
import numpy as np

@pytest.fixture
def sample_csv(tmp_path):
    """Create a temporary CSV file for testing."""
    df = pd.DataFrame({
        'col1': [1, 2, 3],
        'col2': ['a', 'b', 'c']
    })

    file_path = tmp_path / "test_data.csv"
    df.to_csv(file_path, index=False)

    return file_path, df

# add file path here when we have our data from online:

#def test_load_data_reads_csv(sample_csv):
    file_path, original_df = sample_csv

    loaded_df = load_data(file_path)

    # Check it's not empty
    assert not loaded_df.empty

    # Check shape matches
    assert loaded_df.shape == original_df.shape

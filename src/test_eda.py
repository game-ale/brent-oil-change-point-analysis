
import unittest
import pandas as pd
import numpy as np
from eda_analysis import preprocess_data

class TestEDA(unittest.TestCase):
    
    def test_preprocess_data(self):
        # Create dummy data
        data = {
            'Date': ['20-May-87', '21-May-87', 'Invalid-Date'],
            'Price': [18.63, 18.45, 18.55]
        }
        df = pd.DataFrame(data)
        
        # Run preprocessing
        processed_df = preprocess_data(df)
        
        # Checks
        self.assertEqual(len(processed_df), 2)  # Should drop invalid date
        self.assertIn('Log_Returns', processed_df.columns)
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(processed_df.index))
        # Check calculation: ln(18.45 / 18.63) approx -0.0097
        expected_return = np.log(18.45 / 18.63)
        self.assertAlmostEqual(processed_df['Log_Returns'].iloc[1], expected_return, places=4)

if __name__ == '__main__':
    unittest.main()

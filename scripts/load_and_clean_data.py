"""
Data Processing Script for Retail Inventory Analysis

This script loads raw inventory data, performs basic cleaning and transformations,
and saves the processed data for analysis.

Usage:
    python load_and_clean_data.py
"""

import pandas as pd
import os
from datetime import datetime


def load_raw_data(file_path):
    """
    Load raw CSV data from the specified file path.
    
    Args:
        file_path (str): Path to the raw CSV file
        
    Returns:
        pd.DataFrame: Loaded data
    """
    print(f"Loading data from {file_path}...")
    data = pd.read_csv(file_path)
    print(f"Loaded {len(data)} rows and {len(data.columns)} columns")
    return data


def clean_data(data):
    """
    Perform basic data cleaning and validation.
    
    Args:
        data (pd.DataFrame): Raw data
        
    Returns:
        pd.DataFrame: Cleaned data
    """
    print("\nCleaning data...")
    
    # Convert date column to datetime
    data['date'] = pd.to_datetime(data['date'])
    print(f"  - Converted 'date' to datetime format")
    
    # Check for missing values
    missing_values = data.isnull().sum()
    if missing_values.sum() > 0:
        print(f"  - Found missing values:\n{missing_values[missing_values > 0]}")
        print("  - Dropping rows with missing values")
        data = data.dropna()
    else:
        print("  - No missing values found")
    
    # Ensure numeric columns are correct type
    numeric_columns = ['units_sold', 'units_in_stock', 'price']
    for col in numeric_columns:
        data[col] = pd.to_numeric(data[col], errors='coerce')
    print(f"  - Converted numeric columns to proper types")
    
    # Validate stock levels (should not be negative)
    if (data['units_in_stock'] < 0).any() or (data['units_sold'] < 0).any():
        print("  - Warning: Found negative values in stock or sales data")
    
    print(f"  - Cleaned data shape: {data.shape}")
    return data


def add_feature_columns(data):
    """
    Create additional feature columns for analysis.
    
    Args:
        data (pd.DataFrame): Cleaned data
        
    Returns:
        pd.DataFrame: Data with new feature columns
    """
    print("\nCreating feature columns...")
    
    # Revenue = units_sold * price
    data['revenue'] = data['units_sold'] * data['price']
    
    # Stock after sales (approximate)
    data['stock_after_sales'] = data['units_in_stock'] - data['units_sold']
    
    # Extract year, month, day for time-based analysis
    data['year'] = data['date'].dt.year
    data['month'] = data['date'].dt.month
    data['day'] = data['date'].dt.day
    data['day_of_week'] = data['date'].dt.day_name()
    
    print("  - Added: revenue, stock_after_sales, year, month, day, day_of_week")
    return data


def save_processed_data(data, output_path):
    """
    Save processed data to CSV.
    
    Args:
        data (pd.DataFrame): Processed data
        output_path (str): Path to save the processed data
    """
    data.to_csv(output_path, index=False)
    print(f"\nData saved to {output_path}")
    print(f"Final dataset: {len(data)} rows × {len(data.columns)} columns")


def main():
    """
    Main execution function.
    """
    # Define file paths
    raw_data_path = os.path.join(
        os.path.dirname(__file__),
        '..',
        'data',
        'raw',
        'sample_inventory_data.csv'
    )
    
    processed_data_path = os.path.join(
        os.path.dirname(__file__),
        '..',
        'data',
        'processed',
        'processed_inventory_data.csv'
    )
    
    # Execute data pipeline
    try:
        raw_data = load_raw_data(raw_data_path)
        cleaned_data = clean_data(raw_data)
        enhanced_data = add_feature_columns(cleaned_data)
        save_processed_data(enhanced_data, processed_data_path)
        print("\n✓ Data processing completed successfully!")
        
    except FileNotFoundError:
        print(f"Error: Could not find {raw_data_path}")
        print("Make sure the raw data file exists in data/raw/")
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        raise


if __name__ == '__main__':
    main()

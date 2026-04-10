"""
Inventory Analysis Script

This script performs analysis on processed inventory data to identify:
- Slow-moving items (low sales velocity)
- Fast-selling products (high sales velocity)
- Demand variability across stores and time periods

Usage:
    python analyze_inventory.py
"""

import pandas as pd
import os


def load_processed_data(file_path):
    """
    Load processed data from CSV.
    
    Args:
        file_path (str): Path to processed data
        
    Returns:
        pd.DataFrame: Processed inventory data
    """
    print(f"Loading processed data from {file_path}...")
    data = pd.read_csv(file_path)
    data['date'] = pd.to_datetime(data['date'])
    print(f"Loaded {len(data)} rows")
    return data


def analyze_slow_moving_items(data, threshold=5):
    """
    Identify slow-moving items (average units sold below threshold).
    
    Args:
        data (pd.DataFrame): Processed data
        threshold (int): Sales threshold for slow-moving classification
        
    Returns:
        pd.DataFrame: Slow-moving items analysis
    """
    print("\n" + "="*60)
    print("ANALYSIS 1: SLOW-MOVING ITEMS")
    print("="*60)
    
    slow_movers = data.groupby('product_name').agg({
        'units_sold': ['mean', 'sum', 'count'],
        'price': 'first',
        'revenue': 'sum'
    }).round(2)
    
    slow_movers.columns = ['avg_units_sold', 'total_units_sold', 
                           'sale_count', 'price', 'total_revenue']
    slow_movers = slow_movers.sort_values('avg_units_sold')
    
    print("\nAll Products Ranked by Average Sales Volume:")
    print(slow_movers)
    
    # Filter for items below threshold
    truly_slow = slow_movers[slow_movers['avg_units_sold'] < threshold]
    print(f"\nProducts with avg sales < {threshold} units/day:")
    print(truly_slow)
    
    return slow_movers


def analyze_fast_selling_items(data, threshold=12):
    """
    Identify fast-selling items (average units sold above threshold).
    
    Args:
        data (pd.DataFrame): Processed data
        threshold (int): Sales threshold for fast-selling classification
        
    Returns:
        pd.DataFrame: Fast-selling items analysis
    """
    print("\n" + "="*60)
    print("ANALYSIS 2: FAST-SELLING ITEMS")
    print("="*60)
    
    fast_sellers = data.groupby('product_name').agg({
        'units_sold': ['mean', 'sum', 'count'],
        'price': 'first',
        'revenue': 'sum'
    }).round(2)
    
    fast_sellers.columns = ['avg_units_sold', 'total_units_sold', 
                            'sale_count', 'price', 'total_revenue']
    fast_sellers = fast_sellers.sort_values('avg_units_sold', ascending=False)
    
    print("\nAll Products Ranked by Average Sales Volume:")
    print(fast_sellers)
    
    # Filter for items above threshold
    truly_fast = fast_sellers[fast_sellers['avg_units_sold'] >= threshold]
    print(f"\nProducts with avg sales >= {threshold} units/day:")
    print(truly_fast)
    
    return fast_sellers


def analyze_demand_variability(data):
    """
    Analyze demand variability across stores and time periods.
    
    Args:
        data (pd.DataFrame): Processed data
        
    Returns:
        dict: Dictionary with variability analyses
    """
    print("\n" + "="*60)
    print("ANALYSIS 3: DEMAND VARIABILITY")
    print("="*60)
    
    results = {}
    
    # Variability by store
    print("\nDemand Variability by Store:")
    store_analysis = data.groupby('store_id').agg({
        'units_sold': ['mean', 'std', 'min', 'max']
    }).round(2)
    store_analysis.columns = ['avg_sales', 'std_dev', 'min_sales', 'max_sales']
    store_analysis['coefficient_of_variation'] = (
        store_analysis['std_dev'] / store_analysis['avg_sales']
    ).round(3)
    print(store_analysis)
    results['by_store'] = store_analysis
    
    # Variability by product
    print("\nDemand Variability by Product:")
    product_analysis = data.groupby('product_name').agg({
        'units_sold': ['mean', 'std', 'min', 'max']
    }).round(2)
    product_analysis.columns = ['avg_sales', 'std_dev', 'min_sales', 'max_sales']
    product_analysis['coefficient_of_variation'] = (
        product_analysis['std_dev'] / product_analysis['avg_sales']
    ).round(3)
    print(product_analysis)
    results['by_product'] = product_analysis
    
    # Variability by time period (day of week)
    print("\nDemand Variability by Day of Week:")
    time_analysis = data.groupby('day_of_week').agg({
        'units_sold': ['mean', 'std', 'count']
    }).round(2)
    time_analysis.columns = ['avg_sales', 'std_dev', 'count']
    print(time_analysis)
    results['by_time'] = time_analysis
    
    return results


def generate_summary_statistics(data):
    """
    Generate overall summary statistics.
    
    Args:
        data (pd.DataFrame): Processed data
        
    Returns:
        dict: Summary statistics
    """
    print("\n" + "="*60)
    print("SUMMARY STATISTICS")
    print("="*60)
    
    summary = {
        'total_records': len(data),
        'date_range': f"{data['date'].min().date()} to {data['date'].max().date()}",
        'unique_products': data['product_name'].nunique(),
        'unique_stores': data['store_id'].nunique(),
        'total_units_sold': data['units_sold'].sum(),
        'avg_units_per_transaction': data['units_sold'].mean().round(2),
        'total_revenue': data['revenue'].sum().round(2),
        'avg_stock_level': data['units_in_stock'].mean().round(2),
        'low_stock_alerts': (data['stock_after_sales'] < 5).sum()
    }
    
    for key, value in summary.items():
        print(f"{key}: {value}")
    
    return summary


def save_results(slow_movers, fast_sellers, variability, summary, output_dir):
    """
    Save analysis results to CSV files.
    
    Args:
        slow_movers (pd.DataFrame): Slow-moving items
        fast_sellers (pd.DataFrame): Fast-selling items
        variability (dict): Variability analyses
        summary (dict): Summary statistics
        output_dir (str): Output directory path
    """
    print("\n" + "="*60)
    print("SAVING RESULTS")
    print("="*60)
    
    # Save slow movers
    slow_path = os.path.join(output_dir, 'slow_moving_items.csv')
    slow_movers.to_csv(slow_path)
    print(f"✓ Saved: {slow_path}")
    
    # Save fast sellers
    fast_path = os.path.join(output_dir, 'fast_selling_items.csv')
    fast_sellers.to_csv(fast_path)
    print(f"✓ Saved: {fast_path}")
    
    # Save variability analyses
    store_var_path = os.path.join(output_dir, 'demand_variability_by_store.csv')
    variability['by_store'].to_csv(store_var_path)
    print(f"✓ Saved: {store_var_path}")
    
    product_var_path = os.path.join(output_dir, 'demand_variability_by_product.csv')
    variability['by_product'].to_csv(product_var_path)
    print(f"✓ Saved: {product_var_path}")
    
    # Save summary statistics as text
    summary_path = os.path.join(output_dir, 'summary_statistics.txt')
    with open(summary_path, 'w') as f:
        f.write("RETAIL INVENTORY ANALYSIS - SUMMARY STATISTICS\n")
        f.write("=" * 50 + "\n\n")
        for key, value in summary.items():
            f.write(f"{key}: {value}\n")
    print(f"✓ Saved: {summary_path}")


def main():
    """
    Main execution function.
    """
    # Define file paths
    processed_data_path = os.path.join(
        os.path.dirname(__file__),
        '..',
        'data',
        'processed',
        'processed_inventory_data.csv'
    )
    
    output_dir = os.path.join(
        os.path.dirname(__file__),
        '..',
        'outputs'
    )
    
    try:
        # Load data
        data = load_processed_data(processed_data_path)
        
        # Run analyses
        slow_movers = analyze_slow_moving_items(data)
        fast_sellers = analyze_fast_selling_items(data)
        variability = analyze_demand_variability(data)
        summary = generate_summary_statistics(data)
        
        # Save results
        save_results(slow_movers, fast_sellers, variability, summary, output_dir)
        
        print("\n✓ Analysis completed successfully!")
        
    except FileNotFoundError:
        print(f"Error: Could not find {processed_data_path}")
        print("Run load_and_clean_data.py first to generate processed data.")
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        raise


if __name__ == '__main__':
    main()

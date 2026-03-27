import pandas as pd
from typing import Optional, List


def filter_by_date_range(
    df: pd.DataFrame,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    date_col: str = "Date",
) -> pd.DataFrame:
    """
    Filter a DataFrame to rows within a given date range (inclusive).

    Args:
        df: Source DataFrame.
        start_date: Start date string, e.g. '2023-01-01'. None = no lower bound.
        end_date: End date string, e.g. '2023-06-30'. None = no upper bound.
        date_col: Name of the date column.

    Returns:
        Filtered DataFrame.
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])

    if start_date:
        df = df[df[date_col] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df[date_col] <= pd.to_datetime(end_date)]

    return df


def filter_by_region(df: pd.DataFrame, regions: List[str]) -> pd.DataFrame:
    """
    Keep only rows matching the given regions.

    Args:
        df: Source DataFrame with a 'Region' column.
        regions: List of region names to keep.

    Returns:
        Filtered DataFrame.
    """
    if not regions:
        return df
    return df[df["Region"].isin(regions)]


def filter_by_product(df: pd.DataFrame, products: List[str]) -> pd.DataFrame:
    """
    Keep only rows matching the given products.

    Args:
        df: Source DataFrame with a 'Product' column.
        products: List of product names to keep.

    Returns:
        Filtered DataFrame.
    """
    if not products:
        return df
    return df[df["Product"].isin(products)]


def compute_kpis(df: pd.DataFrame) -> dict:
    """
    Compute high-level KPIs from the filtered DataFrame.

    Returns a dict with:
        - total_revenue
        - total_units
        - avg_order_value
        - top_region
        - top_product
    """
    if df.empty:
        return {
            "total_revenue": 0.0,
            "total_units": 0,
            "avg_order_value": 0.0,
            "top_region": "N/A",
            "top_product": "N/A",
        }

    return {
        "total_revenue": round(df["Revenue"].sum(), 2),
        "total_units": int(df["Units_Sold"].sum()),
        "avg_order_value": round(df["Revenue"].mean(), 2),
        "top_region": df.groupby("Region")["Revenue"].sum().idxmax(),
        "top_product": df.groupby("Product")["Revenue"].sum().idxmax(),
    }


if __name__ == "__main__":
    from data_gen import generate_mock_data

    df = generate_mock_data(200)

    # Apply filters
    df_filtered = filter_by_date_range(df, start_date="2023-02-01", end_date="2023-04-30")
    df_filtered = filter_by_region(df_filtered, ["North", "East"])

    kpis = compute_kpis(df_filtered)
    print("=== KPI Summary (North & East, Feb–Apr 2023) ===")
    for k, v in kpis.items():
        print(f"  {k:20s}: {v}")

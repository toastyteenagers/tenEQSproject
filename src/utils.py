import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def calculate_eoq(df, ordering_cost, holding_cost, time_period='daily'):
    """
    Calculate Economic Order Quantity (EOQ) based on sales data.

    :param df: Pandas DataFrame containing sales transactions.
    :param ordering_cost: Cost per order.
    :param holding_cost: Holding cost per unit per year.
    :param time_period: 'daily', 'monthly', or 'yearly' sales data.
    :return: EOQ value.
    """

    # Convert timestamp to date to count unique daily sales occurrences
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    daily_sales = df.groupby('date').size()

    # Aggregate demand based on time period
    if time_period == 'daily':
        annual_demand = daily_sales.mean() * 365
    elif time_period == 'monthly':
        annual_demand = daily_sales.mean() * 12 * 30  # Approximate monthly sales
    else:  # Assume yearly by default
        annual_demand = daily_sales.sum()

    # Compute EOQ
    eoq = np.sqrt((2 * annual_demand * ordering_cost) / holding_cost)
    return float(eoq)

def pad_and_fill_missing_values(row, target_length=7, fill_value="0.00"):
    filled_row = [col if col.strip() != "" else fill_value for col in row]
    padded_row = filled_row + [fill_value] * (target_length - len(filled_row))
    return padded_row



def read_csv(file_path: str) -> pd.DataFrame:
    data = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            row = line.strip().split(",")
            row = pad_and_fill_missing_values(row)
            data.append(row)

    # first row is the columns
    data = data[1:]

    df = pd.DataFrame(data, columns=["product_name", "our_price", "category", "current_stock", "restock_threshold", "last_restock", "product_brand"])
    # coerce prices to strictly numerics.
    df["our_price"] = df["our_price"].replace({"[$]": ""}, regex=True)
    df["our_price"] = pd.to_numeric(df["our_price"], errors="coerce").fillna(0.00)

    # make categories all lowercase.
    df["category"] = df["category"].str.lower()

    # coerce current stock and restock threshold to numeric
    df["current_stock"] = pd.to_numeric(df["current_stock"], errors="coerce").fillna(0.00)
    df["restock_threshold"] = pd.to_numeric(df["restock_threshold"], errors="coerce").fillna(0.00)

    # convert restock dates to iso 8601
    df["last_restock"] = df["last_restock"].apply(convert_to_iso8601)

    # santize string fields
    df["product_name"] = df["product_name"].apply(sanitize_text)
    df["product_brand"] = df["product_brand"].apply(sanitize_text)

    return df


def convert_to_iso8601(date_str: str):
    try:
        return pd.to_datetime(date_str).strftime("%Y-%m-%d")
    except Exception:
        return pd.to_datetime("1970-01-01").strftime("%Y-%m-%d")


def calculate_eoq(df, demand_col, ordering_cost, holding_cost, time_period='daily'):
    """
    Calculate Economic Order Quantity (EOQ) based on sales data.

    :param df: Pandas DataFrame containing sales data over time.
    :param demand_col: Column name representing sales demand.
    :param ordering_cost: Cost per order.
    :param holding_cost: Holding cost per unit per year.
    :param time_period: 'daily', 'monthly', or 'yearly' sales data.
    :return: EOQ value.
    """

    # Aggregate demand based on time period
    if time_period == 'daily':
        annual_demand = df[demand_col].sum() * 365
    elif time_period == 'monthly':
        annual_demand = df[demand_col].sum() * 12
    else:  # Assume yearly by default
        annual_demand = df[demand_col].sum()

    # Compute EOQ
    eoq = np.sqrt((2 * annual_demand * ordering_cost) / holding_cost)
    return eoq

def sanitize_text(text):
        if pd.isna(text):
            return "0.00"  # fill missing  fields with "0.00"
        text = str(text)
        # escape characters
        sanitized_text = re.sub(r"[\n\r\t\\]", "", text)
        return sanitized_text
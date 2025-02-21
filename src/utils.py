import re
import pandas as pd



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


def sanitize_text(text):
        if pd.isna(text):
            return "0.00"  # fill missing  fields with "0.00"
        text = str(text)
        # escape characters
        sanitized_text = re.sub(r"[\n\r\t\\]", "", text)
        return sanitized_text
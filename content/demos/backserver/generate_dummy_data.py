"""
Generate 10 million transaction records for AG Grid server-side testing.
Uses batch processing, parallel generation, and progress tracking.

Usage:
    python generate_dummy_data.py
"""

import polars as pl
from faker import Faker
import numpy as np
from datetime import datetime, timedelta
import random
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
import os

NUM_ROWS = 10_000_000
BATCH_SIZE = 5_000
NUM_WORKERS = os.cpu_count() or 4
OUTPUT_FILE = "dummy_data.parquet"

# Lookup data
SELLERS = None
PRODUCTS = None
CATEGORIES = [
    "Electronics", "Clothing", "Food & Beverage", "Home & Garden",
    "Sports & Outdoors", "Automotive", "Health & Beauty", "Books & Media",
    "Toys & Games", "Office Supplies"
]
COUNTRIES = ["USA", "UK", "Canada", "Germany", "France", "Japan", "Australia", "Brazil", "India", "China"]
REGIONS = {
    "USA": ["Northeast", "Southeast", "Midwest", "Southwest", "West"],
    "UK": ["England", "Scotland", "Wales", "Northern Ireland"],
    "Canada": ["Ontario", "Quebec", "British Columbia", "Alberta"],
    "Germany": ["Bavaria", "North Rhine-Westphalia", "Baden-Württemberg", "Hesse"],
    "France": ["Île-de-France", "Provence-Alpes-Côte d'Azur", "Auvergne-Rhône-Alpes"],
    "Japan": ["Kanto", "Kansai", "Chubu", "Kyushu"],
    "Australia": ["New South Wales", "Victoria", "Queensland", "Western Australia"],
    "Brazil": ["São Paulo", "Rio de Janeiro", "Minas Gerais", "Bahia"],
    "India": ["Maharashtra", "Karnataka", "Delhi", "Tamil Nadu"],
    "China": ["Beijing", "Shanghai", "Guangdong", "Zhejiang"],
}
PAYMENT_METHODS = ["Credit Card", "Debit Card", "PayPal", "Bank Transfer", "Cash"]
STATUSES = ["Completed", "Pending", "Cancelled", "Refunded"]
START_DATE = datetime.now() - timedelta(days=730)


def init_worker():
    """Initialize worker with seed for reproducibility."""
    global SELLERS, PRODUCTS
    fake = Faker()
    Faker.seed(42)
    SELLERS = [fake.company() for _ in range(500)]
    PRODUCTS = [fake.catch_phrase() for _ in range(1000)]


def generate_batch(args):
    """Generate a batch of transaction data."""
    batch_num, batch_size, seed = args

    # Create local faker instance with unique seed per batch
    fake = Faker()
    Faker.seed(seed)
    np.random.seed(seed)
    random.seed(seed)

    # Generate lookup data if not initialized
    sellers = [fake.company() for _ in range(500)]
    products = [fake.catch_phrase() for _ in range(1000)]

    start_id = batch_num * batch_size

    transaction_ids = [f"TXN{start_id + i:010d}" for i in range(batch_size)]
    seller_list = np.random.choice(sellers, batch_size).tolist()
    product_list = np.random.choice(products, batch_size).tolist()
    category_list = np.random.choice(CATEGORIES, batch_size).tolist()

    customer_names = [fake.name() for _ in range(batch_size)]
    customer_emails = [fake.email() for _ in range(batch_size)]

    country_list = np.random.choice(COUNTRIES, batch_size).tolist()
    region_list = [np.random.choice(REGIONS.get(country, ["N/A"])) for country in country_list]
    city_list = [fake.city() for _ in range(batch_size)]

    quantities = np.random.randint(1, 50, batch_size)
    unit_prices = np.round(np.random.uniform(5.0, 500.0, batch_size), 2)
    discount_percents = np.random.choice([0, 5, 10, 15, 20, 25], batch_size, p=[0.4, 0.2, 0.15, 0.15, 0.07, 0.03])

    subtotals = quantities * unit_prices
    discount_amounts = subtotals * (discount_percents / 100)
    total_values = np.round(subtotals - discount_amounts, 2)

    transaction_dates = [START_DATE + timedelta(days=random.randint(0, 730)) for _ in range(batch_size)]
    payment_methods = np.random.choice(PAYMENT_METHODS, batch_size).tolist()
    status_list = np.random.choice(STATUSES, batch_size, p=[0.85, 0.08, 0.05, 0.02]).tolist()
    shipping_costs = np.round(np.random.uniform(0, 50, batch_size), 2)

    ratings = np.random.choice([1, 2, 3, 4, 5, None], batch_size, p=[0.02, 0.05, 0.15, 0.45, 0.28, 0.05])
    customer_ratings = [None if r is None else int(r) for r in ratings]

    is_repeat_customers = np.random.choice([True, False], batch_size, p=[0.6, 0.4]).tolist()
    is_gifts = np.random.choice([True, False], batch_size, p=[0.15, 0.85]).tolist()

    return pl.DataFrame({
        "transaction_id": transaction_ids,
        "seller": seller_list,
        "product": product_list,
        "category": category_list,
        "customer_name": customer_names,
        "customer_email": customer_emails,
        "country": country_list,
        "region": region_list,
        "city": city_list,
        "quantity": quantities.tolist(),
        "unit_price": unit_prices.tolist(),
        "discount_percent": discount_percents.tolist(),
        "total_value": total_values.tolist(),
        "transaction_date": transaction_dates,
        "payment_method": payment_methods,
        "status": status_list,
        "shipping_cost": shipping_costs.tolist(),
        "customer_rating": customer_ratings,
        "is_repeat_customer": is_repeat_customers,
        "is_gift": is_gifts,
    })


def main():
    print(f"Generating {NUM_ROWS:,} transaction records...")
    print(f"Batch size: {BATCH_SIZE:,}")
    print(f"Workers: {NUM_WORKERS}")

    num_batches = (NUM_ROWS + BATCH_SIZE - 1) // BATCH_SIZE

    # Prepare batch arguments with different seeds
    batch_args = [(i, min(BATCH_SIZE, NUM_ROWS - i * BATCH_SIZE), 42 + i) for i in range(num_batches)]

    batches = []

    # Generate batches in parallel with progress bar
    with ProcessPoolExecutor(max_workers=NUM_WORKERS, initializer=init_worker) as executor:
        futures = {executor.submit(generate_batch, args): args[0] for args in batch_args}

        with tqdm(total=num_batches, desc="Generating batches", unit="batch") as pbar:
            for future in as_completed(futures):
                batch_num = futures[future]
                try:
                    batch_df = future.result()
                    batches.append((batch_num, batch_df))
                    pbar.update(1)
                except Exception as e:
                    print(f"\nError generating batch {batch_num}: {e}")
                    raise

    # Sort batches by batch number to maintain order
    batches.sort(key=lambda x: x[0])
    batch_dfs = [df for _, df in batches]

    print("Concatenating batches...")
    df = pl.concat(batch_dfs)

    print(f"Writing to {OUTPUT_FILE}...")
    df.write_parquet(OUTPUT_FILE, compression="snappy")

    file_size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)

    print(f"\n{'='*60}")
    print(f"Data generation complete!")
    print(f"{'='*60}")
    print(f"File: {OUTPUT_FILE}")
    print(f"Total rows: {df.height:,}")
    print(f"Total columns: {df.width}")
    print(f"File size: {file_size_mb:.2f} MB")

    print(f"\nColumns:")
    for col in df.columns:
        print(f"  - {col}: {df[col].dtype}")

    print(f"\nSample data (first 5 rows):")
    print(df.head(5))

    print(f"\nSummary statistics:")
    print(f"  Total transaction value: ${df['total_value'].sum():,.2f}")
    print(f"  Average transaction value: ${df['total_value'].mean():.2f}")
    print(f"  Unique sellers: {df['seller'].n_unique()}")
    print(f"  Unique products: {df['product'].n_unique()}")
    print(f"  Unique countries: {df['country'].n_unique()}")
    print(f"  Date range: {df['transaction_date'].min()} to {df['transaction_date'].max()}")

    print(f"\nStatus distribution:")
    print(df.group_by('status').agg(pl.len()).sort('status'))

    print(f"\nCategory distribution:")
    print(df.group_by('category').agg(pl.len()).sort('len', descending=True))


if __name__ == "__main__":
    main()

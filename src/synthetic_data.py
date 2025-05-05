import pandas as pd
from faker import Faker
import random

fake = Faker()

# Define parameters
n_records = 1000
categories = ['Food', 'Transport', 'Rent', 'Entertainment',
              'Utilities', 'Health', 'Shopping', 'Other'
              ]
payment_methods = ['Card', 'Cash', 'Bank Transfer', 'Mobile Payment']


def generate_expense():
    category = random.choice(categories)
    base_amount = {
        'Food': (5, 30),
        'Transport': (2, 50),
        'Rent': (400, 1200),
        'Entertainment': (10, 100),
        'Utilities': (50, 200),
        'Health': (20, 150),
        'Shopping': (10, 200),
        'Other': (5, 100)
    }

    amount_range = base_amount[category]

    return {
        'date': fake.date_between(start_date='-6M', end_date='today'),
        'category': category,
        'amount': round(random.uniform(*amount_range), 2),
        'payment_method': random.choice(payment_methods),
        'description': fake.sentence(nb_words=4)
    }


if __name__ == "__main__":
    # Generate synthetic data
    data = [generate_expense() for _ in range(n_records)]
    df = pd.DataFrame(data)

    # Sort by date
    df = df.sort_values(by='date')

    # Save to CSV or show
    df.to_csv('data/synthetic_expenses.csv', index=False)
    print(df.head())

    # This is just for testing purposes
    print("Synthetic data generated and saved to 'synthetic_expenses.csv'")
    print(f"Total records generated: {len(df)}")
    print("Sample data:")
    print(df.sample(5))
    # You can also load the data back to check
    loaded_df = pd.read_csv('data/synthetic_expenses.csv')
    print("Loaded data sample:")
    print(loaded_df.sample(5))
    print(f"Total records loaded: {len(loaded_df)}")

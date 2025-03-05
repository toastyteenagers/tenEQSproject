import sys
import utils
import kagglehub
from kagglehub import KaggleDatasetAdapter

if len(sys.argv) < 2:  # argv[0] is the script name
    print("Usage: python analysis.py [filename for csv]")
    sys.exit(1)

file_path = sys.argv[1]
print("Reading csv file at:", file_path)

df = utils.read_csv(file_path)
print(df.head(n=len(df.columns)))

print(df.describe())

# load in external coffee sales data
sales = kagglehub.dataset_load(
    KaggleDatasetAdapter.PANDAS,
    'ihelon/coffee-sales',
    'index_1.csv'
)

with open("report.md","a") as report:

    # sample parameters for EOQ
    ordering_cost = 50   # Cost per order
    holding_cost = 2      # Holding cost per unit per day

    print("Findings from csv:", file = report)
    eoq_value = utils.calculate_eoq(df, 'current_stock',ordering_cost, holding_cost)

    findings = f"Calculated EOQ: {eoq_value:.2f} (Optimal Order Cost) for ordering cost: {ordering_cost} and holding cost: {holding_cost}"
    print(findings, file=report)


    print("External findings:", file = report)
    product_counts = sales['coffee_name'].value_counts()

    most_ordered = product_counts.idxmax()
    most_ordered_count = product_counts.loc[most_ordered]
    least_ordered = product_counts.idxmin()
    least_ordered_count = product_counts.loc[least_ordered]

    print(f"Total sales: {len(sales)}", file = report)
    print(f"Most ordered product: {most_ordered}, amount of sales: {most_ordered_count}", file = report)
    print(f"Least ordered product: {least_ordered}, amount of sales: {least_ordered_count}", file = report)




sys.exit(0)

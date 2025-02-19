import pandas as pd
import glob
import matplotlib.pyplot as plt

# Define the path where your CSV files are stored (modify this as needed)
csv_files = glob.glob("job_results_from_1.csv")
# Dictionary to store counts per state
state_counts = {}

state_counts = {}

# Process each CSV file
for file in csv_files:
    with open(file, 'r') as f:
        lines = f.readlines()
    
    # Extract only valid rows, skipping 'Job ID' headers
    data = []
    for line in lines:
        line = line.strip()
        if line.startswith("Job ID") or len(line.split(",")) != 2:
            continue
        data.append(line.split(","))

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=["State", "Count"])
    df["Count"] = df["Count"].astype(int)  # Convert Count column to integer

    # Aggregate values per state
    for _, row in df.iterrows():
        state = row["State"]
        count = row["Count"]

        if state not in state_counts:
            state_counts[state] = []
        
        state_counts[state].append(count)

# Compute the median for each state
median_counts = {state: pd.Series(counts).median() for state, counts in state_counts.items()}

# Convert to DataFrame for better visualization
median_df = pd.DataFrame(list(median_counts.items()), columns=["State", "Median Count"])

# Sort by State
median_df.sort_values(by="State", inplace=True)


# Plot the data
plt.figure(figsize=(12, 6))
plt.bar(median_df["State"], median_df["Median Count"], color='blue')
plt.xlabel("State")
plt.ylabel("Median Count")
plt.title("Median Count per State")
plt.xticks(rotation=90)
plt.show()

# Optionally, save to a CSV file
# median_df.to_csv("median_counts.csv", index=False)

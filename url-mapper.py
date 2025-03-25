import pandas as pd
from fuzzywuzzy import fuzz, process

# Load CSV files containing URLs
def load_urls(csv_path):
    df = pd.read_csv(csv_path)
    return df['url'].tolist()

# Match URLs from old-urls to new-urls using FuzzyWuzzy with token_set_ratio
def match_urls(old_urls, new_urls):
    matched_results = []
    
    for url in old_urls:
        # Find the best match in new-urls for each URL in old-urls using token_set_ratio
        best_match = process.extractOne(url, new_urls, scorer=fuzz.token_set_ratio)
        matched_results.append({
            'Old_URL': url,
            'Best_Match_New_URL': best_match[0],
            'Match_Score': best_match[1]  # Still returning match score for information
        })
    
    return matched_results

# Save matched results to a CSV
def save_matches_to_csv(matched_results, output_path):
    df_results = pd.DataFrame(matched_results)
    df_results.to_csv(output_path, index=False)

# Main function to run the script
def main(old_urls_csv, new_urls_csv, output_csv):
    print("Loading URLs...")
    old_urls = load_urls(old_urls_csv)
    new_urls = load_urls(new_urls_csv)
    
    print("Matching URLs using fuzz.token_set_ratio...")
    matched_results = match_urls(old_urls, new_urls)
    
    print("Saving matched results...")
    save_matches_to_csv(matched_results, output_csv)
    
    print(f"Matching complete! Results saved to {output_csv}")

# Example usage
if __name__ == "__main__":
    old_urls_csv = "old-urls.csv"  # Path to old-urls CSV file
    new_urls_csv = "new-urls.csv"  # Path to new-urls CSV file
    output_csv = "matched_urls.csv"  # Output file for matched results
    
    main(old_urls_csv, new_urls_csv, output_csv)

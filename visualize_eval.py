import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np # Import numpy for bar positioning
import matplotlib as mpl # Import matplotlib for rcParams
import matplotlib.font_manager as fm # Import font_manager
import shutil # For removing cache directory

# --- List Available Fonts (for debugging) ---
print("--- Matplotlib Font List ---")
try:
    # Get a list of font family names known to Matplotlib
    font_families = sorted(set(f.name for f in fm.fontManager.ttflist))
    print("Available font families:")
    for family in font_families:
        print(f"  - {family}")
    # Specifically check for Nanum variants
    nanum_found = [f for f in font_families if 'Nanum' in f]
    if nanum_found:
        print("\nFound Nanum variants:", nanum_found)
    else:
        print("\nNo Nanum variants found in Matplotlib's list.")
except Exception as e:
    print(f"Error listing fonts: {e}")
print("--- End Font List ---\n")
# --- End Debugging ---

# --- Rebuild Font Cache (if necessary) ---
try:
    # Check if NanumGothic is already known
    fm.findfont("NanumGothic", fallback_to_default=False)
except ValueError:
    print("NanumGothic not found in current cache. Rebuilding font cache...")
    # Get cache directory
    cache_dir = mpl.get_cachedir()
    # Remove the existing cache directory if it exists
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)
        print(f"Removed font cache directory: {cache_dir}")
    # Matplotlib should rebuild automatically on next findfont/font load
    # Or explicitly trigger rebuild (can sometimes be slow)
    # fm._rebuild()
    print("Font cache will be rebuilt on first plot attempt.")
# --- End Cache Rebuild ---

# --- Font Configuration for Korean Characters ---
try:
    # Try common Korean fonts
    # You might need to install them: sudo apt-get install fonts-nanum*
    mpl.rcParams['font.family'] = 'NanumGothic'
    mpl.rcParams['axes.unicode_minus'] = False # Ensure minus signs render correctly
    print("Successfully set font to NanumGothic.") # Confirmation
except Exception as e:
    print(f"Warning: Could not set 'NanumGothic' font ({e}). Korean characters might not display correctly.")
    print("Consider installing a Korean font like NanumGothic: sudo apt-get install fonts-nanum* (Debian/Ubuntu)")
    # Fallback to a generic sans-serif, which might or might not work depending on system config
    try:
        mpl.rcParams['font.family'] = 'sans-serif'
        mpl.rcParams['axes.unicode_minus'] = False
    except Exception as fallback_e:
         print(f"Could not set fallback font: {fallback_e}")
# --- End Font Configuration ---

def visualize_comparison(csv_files, output_image_path):
    """
    Reads evaluation data from multiple CSV files, combines them,
    and generates a grouped bar chart comparing the total scores
    assigned by different evaluators.

    Args:
        csv_files (list): A list of paths to the input CSV files.
        output_image_path (str): Path to save the output bar chart image.
    """
    all_dfs = []
    evaluator_names = []

    report_col_name = '보고서'
    score_col_name = '총점'

    for csv_file_path in csv_files:
        try:
            # Read the CSV file
            df = pd.read_csv(csv_file_path)

            # --- Data Validation ---
            if report_col_name not in df.columns:
                print(f"Error: Report column '{report_col_name}' not found in {csv_file_path}")
                continue # Skip this file
            if score_col_name not in df.columns:
                print(f"Error: Score column '{score_col_name}' not found in {csv_file_path}")
                continue # Skip this file

            # --- Data Preparation ---
            # Extract evaluator name from filename (e.g., "claude_results.csv" -> "Claude")
            try:
                evaluator = os.path.splitext(os.path.basename(csv_file_path))[0].split('_')[0].title()
            except IndexError:
                evaluator = f"Evaluator_{len(evaluator_names) + 1}" # Fallback name
                print(f"Warning: Could not determine evaluator name from {csv_file_path}. Using '{evaluator}'.")
            evaluator_names.append(evaluator)

            # Ensure the score column is numeric
            df[score_col_name] = pd.to_numeric(df[score_col_name], errors='coerce')
            df.dropna(subset=[score_col_name], inplace=True) # Drop rows where score conversion failed

            # Rename columns for consistency
            df.rename(columns={report_col_name: 'Report', score_col_name: 'Score'}, inplace=True)

            # Add evaluator column
            df['Evaluator'] = evaluator

            # Keep only necessary columns
            all_dfs.append(df[['Report', 'Score', 'Evaluator']])

        except FileNotFoundError:
            print(f"Error: CSV file not found at {csv_file_path}")
        except pd.errors.EmptyDataError:
            print(f"Error: CSV file is empty at {csv_file_path}")
        except Exception as e:
            print(f"An error occurred processing {csv_file_path}: {e}")

    if not all_dfs:
        print("Error: No valid data loaded from any CSV file. Cannot generate chart.")
        return

    # --- Combine and Pivot Data ---
    try:
        combined_df = pd.concat(all_dfs, ignore_index=True)
        pivoted_df = combined_df.pivot(index='Report', columns='Evaluator', values='Score')

        # Sort by the average score across evaluators (optional, for consistent ordering)
        pivoted_df['Mean_Score'] = pivoted_df.mean(axis=1)
        pivoted_df.sort_values(by='Mean_Score', ascending=False, inplace=True)
        pivoted_df.drop(columns=['Mean_Score'], inplace=True)

        # --- Plotting ---
        plt.style.use('ggplot')
        ax = pivoted_df.plot(kind='bar', figsize=(18, 9), width=0.8) # Adjust figsize and width

        # Add labels and title
        ax.set_ylabel('Total Score (Max 5.0)', fontsize=12) # Assuming max score is 5 based on context
        ax.set_xlabel('Report (Model & Status)', fontsize=12)
        ax.set_title('Comparison of Evaluation Scores by Evaluator', fontsize=16, fontweight='bold')

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right', fontsize=10)

        # Add score values on top of bars
        for container in ax.containers:
            ax.bar_label(container, fmt='%.1f', label_type='edge', fontsize=8, padding=3)

        # Add a grid for the y-axis
        ax.yaxis.grid(True, linestyle='--', alpha=0.7)
        ax.set_ylim(0, max(5.5, pivoted_df.max().max() * 1.1)) # Set y-axis limits dynamically

        # Add legend
        ax.legend(title='Evaluator')

        # Adjust layout
        plt.tight_layout()

        # Save the plot
        plt.savefig(output_image_path, dpi=300)
        print(f"Comparison chart saved successfully to {output_image_path}")

        # Display the plot
        plt.show()

    except KeyError as e:
        print(f"Error during pivoting or plotting: Missing key {e}. Check if reports are consistent across files.")
    except Exception as e:
        print(f"An error occurred during chart generation: {e}")

# --- Script Execution ---
# List of CSV files to compare
csv_input_files = [
    'demo/eval/claude_results.csv',
    'demo/eval/gemini_results.csv'
]
# Output file path
output_chart_file = 'evaluation_comparison_chart.png'

# Generate the comparison chart
visualize_comparison(csv_input_files, output_chart_file)

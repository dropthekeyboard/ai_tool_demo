import pandas as pd
import matplotlib.pyplot as plt
import os

def visualize_evaluation_csv(csv_file_path, output_image_path):
    """
    Reads evaluation data from a CSV file and generates a bar chart
    comparing the total scores of different reports.

    Args:
        csv_file_path (str): Path to the input CSV file.
        output_image_path (str): Path to save the output bar chart image.
    """
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file_path)

        # --- Data Preparation ---
        # Ensure the score column is numeric
        score_column = 'Total Score (Weighted, Max 5.0)'
        if score_column not in df.columns:
            # Try finding a similar column name robustly
            potential_cols = [col for col in df.columns if 'Total Score' in col and 'Max 5.0' in col]
            if not potential_cols:
                 print(f"Error: Could not find the score column '{score_column}' or similar in {csv_file_path}")
                 return
            score_column = potential_cols[0] # Use the first match
            print(f"Warning: Using score column '{score_column}'")


        df[score_column] = pd.to_numeric(df[score_column], errors='coerce')
        # Drop rows where score conversion failed (if any)
        df.dropna(subset=[score_column], inplace=True)

        # Create shorter labels for the plot from the file path
        def create_short_label(path):
            try:
                basename = os.path.basename(path)
                model_part = os.path.splitext(basename)[0]
                # Attempt to determine if augmented
                is_augmented = "augmented" in path
                status = "(Aug)" if is_augmented else "(Orig)"
                # Basic name formatting (can be improved)
                label = model_part.replace('_', ' ').replace('-', ' ').title()
                return f"{label} {status}"
            except:
                return path # Fallback to full path if error

        df['Short Label'] = df['Report File Path'].apply(create_short_label)

        # Sort by score for better visualization (optional)
        df.sort_values(by=score_column, ascending=False, inplace=True)

        # --- Plotting ---
        plt.style.use('ggplot') # Use a visually appealing style
        fig, ax = plt.subplots(figsize=(12, 7)) # Adjust figure size as needed

        # Create the bar chart
        bars = ax.bar(df['Short Label'], df[score_column], color=plt.cm.viridis(df[score_column] / 5.0)) # Color by score

        # Add labels and title
        ax.set_ylabel('Total Score (Weighted, Max 5.0)', fontsize=12)
        ax.set_xlabel('Report (Model & Status)', fontsize=12)
        ax.set_title('Simulated Evaluation Scores of Tariff Reports', fontsize=16, fontweight='bold')

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right', fontsize=10) # Adjust rotation and alignment

        # Add score values on top of bars
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.05, f'{yval:.1f}', va='bottom', ha='center', fontsize=9) # Adjust vertical offset

        # Add a grid for the y-axis
        ax.yaxis.grid(True, linestyle='--', alpha=0.7)
        ax.set_ylim(0, 5.5) # Set y-axis limits slightly above max score

        # Adjust layout to prevent labels from being cut off
        plt.tight_layout()

        # Save the plot to a file
        plt.savefig(output_image_path, dpi=300) # Save with high resolution
        print(f"Chart saved successfully to {output_image_path}")

        # Display the plot
        plt.show()

    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_file_path}")
    except pd.errors.EmptyDataError:
         print(f"Error: CSV file is empty at {csv_file_path}")
    except KeyError as e:
        print(f"Error: Column not found in CSV - {e}. Please check the CSV headers.")
    except Exception as e:
        print(f"An error occurred during visualization: {e}")

# --- Script Execution ---
csv_input_file = 'evaluation_results.csv'
output_chart_file = 'evaluation_scores_chart.png'

visualize_evaluation_csv(csv_input_file, output_chart_file)

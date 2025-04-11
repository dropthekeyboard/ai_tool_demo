#!/usr/bin/env python3
"""
Evaluation Visualization Tool

This script visualizes evaluation data from CSV files in the eval directory.
It creates bar charts, radar charts, and comparison visualizations.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.ticker import MaxNLocator
import matplotlib.font_manager as fm
import matplotlib as mpl

# Set style
plt.style.use('ggplot')
sns.set_palette("Set2")

# Configure fonts for Korean text support
def setup_korean_fonts():
    # Try to find a font that supports Korean characters
    # Common fonts that support Korean: NanumGothic, Malgun Gothic, AppleGothic
    potential_fonts = ['NanumGothic', 'Malgun Gothic', 'AppleGothic', 
                      'NanumBarunGothic', 'Gulim', 'Batang', 'Dotum']
    
    font_found = False
    for font_name in potential_fonts:
        # Check if the font is available in the system
        font_list = [f.name for f in fm.fontManager.ttflist]
        if font_name in font_list:
            plt.rcParams['font.family'] = font_name
            print(f"Using {font_name} font for Korean text")
            font_found = True
            break
    
    if not font_found:
        # If no Korean font found, use a fallback method
        print("No Korean font found, using fallback method")
        # Use a generic sans-serif font and handle warnings
        plt.rcParams['font.family'] = 'sans-serif'
        # Transliterate Korean category names to English to avoid rendering issues
        return False
    
    return font_found

# Transliterate Korean category names to English
def transliterate_categories(categories):
    translation = {
        '포괄성 (0-5)': 'Comprehensiveness (0-5)',
        '분석깊이 (0-5)': 'Analysis Depth (0-5)',
        '데이터활용 (0-5)': 'Data Utilization (0-5)',
        '구조논리 (0-5)': 'Structure/Logic (0-5)',
        '표현품질 (0-5)': 'Presentation (0-5)',
        '총점': 'Total Score',
        '등급': 'Grade',
        '기본': 'Basic',
        '증강': 'Enhanced'
    }
    
    if isinstance(categories, list):
        return [translation.get(cat, cat) for cat in categories]
    else:
        return translation.get(categories, categories)

def load_csv_files(directory):
    """Load all CSV files in the directory into a dictionary of dataframes."""
    csv_data = {}
    for filename in os.listdir(directory):
        if filename.endswith('.csv') and 'results' in filename:
            name = filename.split('_')[0]  # Extract evaluator name (claude or gemini)
            filepath = os.path.join(directory, filename)
            csv_data[name] = pd.read_csv(filepath)
    return csv_data

def create_bar_charts(data_dict, output_dir, has_korean_font):
    """Create bar charts for each evaluator's scores."""
    for evaluator, df in data_dict.items():
        # Create figure for total scores
        plt.figure(figsize=(12, 6))
        
        # Extract model names (removing the parts in parentheses for cleaner labels)
        models = [row.split(' (')[0] for row in df['보고서']]
        model_types = ['기본' if '기본' in row else '증강' for row in df['보고서']]
        
        # Always transliterate model types for consistency
        model_types = ['Basic' if m == '기본' else 'Enhanced' for m in model_types]
        
        # Create a new DataFrame with clean model names and types
        plot_df = pd.DataFrame({
            'Model': models,
            'Type': model_types,
            'Score': df['총점']
        })
        
        # Create grouped bar chart
        basic_mask = plot_df['Type'] == 'Basic'
        enhanced_mask = plot_df['Type'] == 'Enhanced'
        
        # Get unique models
        unique_models = plot_df['Model'].unique()
        x = np.arange(len(unique_models))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Plot bars for basic models
        basic_scores = []
        enhanced_scores = []
        
        for model in unique_models:
            # Get scores for basic version of this model
            basic_model_df = plot_df[(plot_df['Model'] == model) & basic_mask]
            if not basic_model_df.empty:
                basic_scores.append(basic_model_df['Score'].values[0])
            else:
                basic_scores.append(0)
                
            # Get scores for enhanced version of this model
            enhanced_model_df = plot_df[(plot_df['Model'] == model) & enhanced_mask]
            if not enhanced_model_df.empty:
                enhanced_scores.append(enhanced_model_df['Score'].values[0])
            else:
                enhanced_scores.append(0)
        
        # Always use English labels for consistency
        label_basic = 'Basic'
        label_enhanced = 'Enhanced'
        
        rects1 = ax.bar(x - width/2, basic_scores, width, label=label_basic)
        rects2 = ax.bar(x + width/2, enhanced_scores, width, label=label_enhanced)
        
        # Customize plot
        ax.set_xlabel('Model')
        ax.set_ylabel('Total Score')
        ax.set_title(f'{evaluator.capitalize()} Evaluation - Basic vs Enhanced Models')
        ax.set_xticks(x)
        ax.set_xticklabels(unique_models, rotation=45, ha='right')
        ax.legend()
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        
        # Add value labels above bars
        for rect in rects1 + rects2:
            height = rect.get_height()
            if height > 0:  # Only add labels for bars with values
                ax.annotate(f'{height:.1f}',
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'{evaluator}_total_scores.png'))
        plt.close()
        
        # Create radar charts for each model
        for i, row in df.iterrows():
            model_name = row['보고서']
            categories = ['포괄성 (0-5)', '분석깊이 (0-5)', '데이터활용 (0-5)', '구조논리 (0-5)', '표현품질 (0-5)']
            scores = [float(row[cat]) for cat in categories]
            
            # Always use English category names for consistency
            clean_categories = transliterate_categories([cat.split(' ')[0] for cat in categories])
            
            # Create radar chart
            fig = plt.figure(figsize=(8, 8))
            ax = fig.add_subplot(111, polar=True)
            
            # Number of categories
            N = len(categories)
            
            # Angle of each axis
            angles = [n / float(N) * 2 * np.pi for n in range(N)]
            angles += angles[:1]  # Close the loop
            
            # Scores need to be circular
            scores = np.array(scores)
            scores = np.append(scores, scores[0])
            
            # Draw the plot
            ax.plot(angles, scores, linewidth=2, linestyle='solid')
            ax.fill(angles, scores, alpha=0.1)
            
            # Draw category labels
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(clean_categories)
            
            # Draw y-labels (scores)
            ax.set_yticks([1, 2, 3, 4, 5])
            ax.set_yticklabels(['1', '2', '3', '4', '5'])
            ax.set_ylim(0, 5)
            
            # Get model type (basic or enhanced) for the title
            model_type = 'Basic' if '기본' in model_name else 'Enhanced'
            model_name_clean = model_name.split(' (')[0]
            
            plt.title(f"{evaluator.capitalize()} Evaluation - {model_name_clean} ({model_type})")
            plt.tight_layout()
            
            # Clean filename - replace Korean characters with transliterated versions
            if '기본' in model_name:
                model_type_clean = 'Basic'
            else:
                model_type_clean = 'Enhanced'
                
            clean_filename = f"{model_name_clean}_{model_type_clean}"
            clean_filename = clean_filename.replace(" ", "_").replace(".", "")
            
            plt.savefig(os.path.join(output_dir, f'{evaluator}_{clean_filename}_radar.png'))
            plt.close()

def create_evaluator_comparison(data_dict, output_dir, has_korean_font):
    """Create comparison charts between different evaluators."""
    if len(data_dict) < 2:
        print("Need at least two evaluators to create comparison")
        return
    
    # Prepare data for comparison
    evaluators = list(data_dict.keys())
    
    # Get common models between evaluators
    common_models = set(data_dict[evaluators[0]]['보고서'])
    for evaluator in evaluators[1:]:
        common_models = common_models.intersection(set(data_dict[evaluator]['보고서']))
    
    if not common_models:
        print("No common models found between evaluators")
        return
    
    # Convert to list and sort
    common_models = sorted(list(common_models))
    
    # Create comparison dataframe
    comparison_data = {}
    for model in common_models:
        # Clean model name for display - replace Korean with English
        model_name_clean = model.split(' (')[0]
        model_type = 'Basic' if '기본' in model else 'Enhanced'
        model_key = f"{model_name_clean} ({model_type})"
        
        comparison_data[model_key] = {}
        for evaluator in evaluators:
            df = data_dict[evaluator]
            row = df[df['보고서'] == model].iloc[0]
            comparison_data[model_key][evaluator] = row['총점']
    
    comparison_df = pd.DataFrame(comparison_data).T
    
    # Create bar chart comparison
    plt.figure(figsize=(14, 8))
    comparison_df.plot(kind='bar', figsize=(14, 8))
    plt.xlabel('Model')
    plt.ylabel('Total Score')
    plt.title('Comparison of Evaluator Scores')
    plt.legend(title='Evaluator')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'evaluator_comparison.png'))
    plt.close()
    
    # Create heatmap for score differences
    plt.figure(figsize=(12, 8))
    difference_df = comparison_df.copy()
    for evaluator in evaluators[1:]:
        difference_df[f'{evaluator} - {evaluators[0]}'] = difference_df[evaluator] - difference_df[evaluators[0]]
    
    difference_cols = [col for col in difference_df.columns if ' - ' in col]
    if difference_cols:
        sns.heatmap(difference_df[difference_cols], annot=True, cmap='RdBu_r', center=0)
        plt.title('Score Differences Between Evaluators')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'evaluator_differences.png'))
        plt.close()

def main():
    # Define directories
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_dir, 'visualizations')
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Setup Korean fonts
    has_korean_font = setup_korean_fonts()
    
    # Load CSV data
    csv_data = load_csv_files(current_dir)
    
    if not csv_data:
        print("No CSV files found with 'results' in the filename")
        return
    
    # Create visualizations
    create_bar_charts(csv_data, output_dir, has_korean_font)
    create_evaluator_comparison(csv_data, output_dir, has_korean_font)
    
    print(f"Visualizations created in {output_dir}")

if __name__ == "__main__":
    main() 
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from wordcloud import WordCloud
from PIL import Image, ImageTk
import io

# Function to plot the top 10 industries based on frequency
def plot_top_industries():
    top_10_highest = industry_counts_sorted.head(10)
    plt.figure(figsize=(10, 6))
    top_10_highest.plot(kind='bar', color='skyblue')
    plt.title('Top 10 Biggest Industries based on Distribution of Companies')
    plt.xlabel('Industry')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# Function to plot the bottom 10 industries based on frequency
def plot_bottom_industries():
    top_10_lowest = industry_counts_sorted.tail(10)
    plt.figure(figsize=(10, 6))
    top_10_lowest.plot(kind='bar', color='lightcoral')
    plt.title('Top 10 Smallest Industries based on Distribution of Companies')
    plt.xlabel('Industry')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# Function to plot the pie chart for top industries
def plot_pie_chart():
    # Creating an empty dictionary to store count of company IDs for each industry of interest
    industry_data_count = {}

    # Define the industries of interest
    industries_of_interest = top_10_highest.index.tolist()

    # Filtering the DataFrame to include only rows where the industry is one of the industries of interest
    df_industries_of_interest = df[df['industry'].isin(industries_of_interest)]

    # Iterating over the industries of interest
    for industry_name in industries_of_interest:
        # Filtering the DataFrame to include only rows with the current industry
        industry_df = df_industries_of_interest[df_industries_of_interest['industry'] == industry_name]
        # Storing the count of company IDs for the current industry in the dictionary
        industry_data_count[industry_name] = len(industry_df)

    # Storing counts of companies separately for each industry
    staffing = industry_data_count.get('Staffing and Recruiting', 0)
    IT = industry_data_count.get('IT Services and IT Consulting', 0)
    hospitals = industry_data_count.get('Hospitals and Health Care', 0)
    software = industry_data_count.get('Software Development', 0)
    finance = industry_data_count.get('Financial Services', 0)
    total_rows = df.shape[0]

    # Pie chart
    labels = ['Staffing and Recruiting', 'IT Services and IT Consulting', 'Hospitals and Health Care', 'Software Development', 'Financial Services', 'Others']
    sizes = [staffing, IT, hospitals, software, finance, total_rows - staffing - IT - hospitals - software - finance]
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6']
    explode = (0, 0.2, 0, 0.2, 0, 0)  # explode the 1st slice

    plt.figure(figsize=(10, 7))  # Adjust the figsize for a bigger graph
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=lambda p: '{:.1f}%\n({:.0f})'.format(p, p * sum(sizes) / 100), startangle=100)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.title('Percentage and Number of Companies Belonging to the Top 5 Biggest Industry')

    plt.show()

# Function to generate word cloud from a dictionary of word frequencies
def generate_wordcloud(word_freq, title, ignore_words=None):
    # Ignore specified words
    if ignore_words:
        word_freq = {word: freq for word, freq in word_freq.items() if word.lower() not in ignore_words}
    
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)
    return wordcloud.to_image()

# Function to plot the donut chart for top skills
def plot_donut_chart():
    # Read the skills.csv file into a DataFrame
    skills_file = 'C:/Users/noele/Documents/E3 Final Project/JobPostings/mappings/skills.csv'
    dfS = pd.read_csv(skills_file)

    # job_skills CSV file
    job_skills = 'C:/Users/noele/Documents/E3 Final Project/JobPostings/jobs/job_skills.csv'

    # Reading the CSV file into a DataFrame
    dfJS = pd.read_csv(job_skills)

    # job_skills CSV file
    skills = 'C:/Users/noele/Documents/E3 Final Project/JobPostings/mappings/skills.csv'

    # Reading the CSV file into a DataFrame
    dfS = pd.read_csv(skills)

    # Extracting unique values from the 'skill_abr' column and storing them in a list
    unique_skills = dfJS['skill_abr'].unique().tolist()

    # Creating an empty dictionary to store job_ids for each unique skill
    skill_job_mapping = {}

    # Iterating through unique skills
    for skill in unique_skills:
        # Selecting rows where 'skill_abr' matches the current skill
        skill_rows = dfJS[dfJS['skill_abr'] == skill]
        # Extracting unique job_ids for this skill
        unique_job_ids = skill_rows['job_id'].unique()
        # Storing the unique job_ids in the dictionary with the skill as key
        skill_job_mapping[skill] = unique_job_ids

    # Creating an empty dictionary to store the count of job IDs for each skill
    skill_job_count = {}

    # Iterating through each skill abbreviation
    for skill in unique_skills:
        # Counting the occurrences of job IDs for the current skill abbreviation
        count_per_skill = len(dfJS[dfJS['skill_abr'] == skill])
        # Storing the count in the dictionary with the skill abbreviation as key
        skill_job_count[skill] = count_per_skill

    # Sorting the skill_job_count dictionary by values (counts), from largest to smallest
    sorted_skills = sorted(skill_job_count.items(), key=lambda x: x[1], reverse=True)

    # Extracting the top 10 skills and their counts
    top_10_skills = sorted_skills[:10]
    top_10_labels = [skill for skill, count in top_10_skills]
    top_10_counts = [count for skill, count in top_10_skills]

    # Define colors
    colors = ['#98FF98', '#FFC0CB', '#BCF5A9', '#FF69B4', '#BCECAC', '#FFB6C1', '#32CD32', '#FF1493', '#FFE4B5', '#FA8072', '#50C878']

    # Merge the top 10 skills DataFrame with the skills DataFrame to get the skill names
    top_10_skills_df = pd.DataFrame({'skill_abr': top_10_labels[:-1], 'count': top_10_counts[:-1]})
    top_10_skills_merged = pd.merge(top_10_skills_df, dfS, on='skill_abr', how='left')

    # Extracting the top 10 skill names and their counts
    top_10_labels = top_10_skills_merged['skill_name'].tolist()
    top_10_counts = top_10_skills_merged['count'].tolist()

    # Calculating the count of "Others"
    others_count = top_10_counts

    # Plotting the donut chart with the specified colors
    plt.figure(figsize=(10, 8))
    patches, texts, autotexts = plt.pie(top_10_counts, labels=top_10_labels, autopct='%1.1f%%', startangle=90, pctdistance=0.85, colors=colors)
    centre_circle = plt.Circle((0, 0), 0.6, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    # Add numeric value below the percentage
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontsize(10)
        autotext.set_horizontalalignment('center')
        autotext.set_verticalalignment('top')

    # Equal aspect ratio ensures that pie is drawn as a circle
    plt.axis('equal')
    plt.title('Distribution of Job Posting')
    plt.show()

# Read the CSV file into a DataFrame
company_industries = 'C:/Users/noele/Documents/E3 Final Project/JobPostings/companies/company_industries.csv'
df = pd.read_csv(company_industries)

# Compute the frequency of each industry
industry_counts = df['industry'].value_counts()
industry_counts_sorted = industry_counts.sort_values(ascending=False)

top_10_highest = industry_counts_sorted.head(10)

# Creating an empty dictionary to store company IDs for each industry of interest
industry_data = {}

# Define the industries of interest
industries_of_interest = ['IT Services and IT Consulting', 'Software Development']

# Filtering the DataFrame to include only rows where the industry is one of the industries of interest
df_industries_of_interest = df[df['industry'].isin(industries_of_interest)]

# Iterating over the industries of interest
for industry_name in industries_of_interest:
    # Filtering the DataFrame to include only rows with the current industry
    industry_df = df_industries_of_interest[df_industries_of_interest['industry'] == industry_name]
    # Storing the list of company IDs for the current industry in the dictionary
    industry_data[industry_name] = industry_df['company_id'].tolist()

# company_industries CSV file
company_industries = 'C:/Users/noele/Documents/E3 Final Project/JobPostings/companies/company_specialities.csv'

# Reading the CSV file into a DataFrame
dfCI = pd.read_csv(company_industries)

# Creating empty dictionaries to store specialties for each industry category
industry_specialties = {'IT Services and IT Consulting': {}, 'Software Development': {}}

# Iterate over the company IDs in the industry_data dictionary
for industry, company_ids in industry_data.items():
    # Iterate over each company ID for the current industry
    for company_id in company_ids:
        # Find the corresponding row in dfCI DataFrame for the current company ID
        company_row = dfCI[dfCI['company_id'] == company_id]
        # Check if the row exists (match found)
        if not company_row.empty:
            # Extract the specialty value from the matched row
            specialty = company_row['speciality'].iloc[0]
            # Assign the specialty to the appropriate industry category
            industry_specialties[industry].setdefault(company_id, []).append(specialty)

# Creating lists to store unique specialties and their frequencies for 'IT Services and IT Consulting'
it_services_specialties_list = []
it_services_specialties_freq = {}

# Extracting specialties and their frequencies for 'IT Services and IT Consulting'
for company_specialties in industry_specialties['IT Services and IT Consulting'].values():
    it_services_specialties_list.extend(company_specialties)

# Counting the frequencies of each specialty
for specialty in it_services_specialties_list:
    it_services_specialties_freq[specialty] = it_services_specialties_freq.get(specialty, 0) + 1

# Creating lists to store unique specialties and their frequencies for 'Software Development'
software_dev_specialties_list = []
software_dev_specialties_freq = {}

# Extracting specialties and their frequencies for 'Software Development'
for company_specialties in industry_specialties['Software Development'].values():
    software_dev_specialties_list.extend(company_specialties)

# Counting the frequencies of each specialty
for specialty in software_dev_specialties_list:
    software_dev_specialties_freq[specialty] = software_dev_specialties_freq.get(specialty, 0) + 1

# Generate word cloud for 'IT Services and IT Consulting' with title
it_cloud_image = generate_wordcloud(it_services_specialties_freq, 'Word Cloud for IT Services and IT Consulting')

# Generate word cloud for 'Software Development' with title, ignoring the word 'Technology'
ignore_words_software_dev = ['technology']
software_cloud_image = generate_wordcloud(software_dev_specialties_freq, 'Word Cloud for Software Development', ignore_words=ignore_words_software_dev)

# Create the Tkinter GUI
root = tk.Tk()
root.title("Industry Distribution")

# Button to plot top industries
top_button = ttk.Button(root, text="Plot Top Industries", command=plot_top_industries)
bottom_button = ttk.Button(root, text="Plot Bottom Industries", command=plot_bottom_industries)
pie_button = ttk.Button(root, text="Plot Pie Chart for Top Industries", command=plot_pie_chart)
donut_button = ttk.Button(root, text="Plot Donut Chart for Top Skills", command=plot_donut_chart)

top_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
bottom_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
pie_button.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
donut_button.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

# Create a frame for displaying the plots
plot_frame = tk.Frame(root)
plot_frame.grid(row=0, column=0, rowspan=4, padx=10, pady=10, sticky="nsew")

# Create labels for the word clouds
it_cloud_label = ttk.Label(plot_frame, text="Word Cloud for IT Services and IT Consulting")
it_cloud_label.grid(row=0, column=0, padx=10, pady=10)
software_cloud_label = ttk.Label(plot_frame, text="Word Cloud for Software Development")
software_cloud_label.grid(row=0, column=1, padx=10, pady=10)

# Convert PIL Image to Tkinter PhotoImage
it_photo = ImageTk.PhotoImage(it_cloud_image)
software_photo = ImageTk.PhotoImage(software_cloud_image)

# Button to display IT services word cloud
it_button = ttk.Button(plot_frame, text="Show IT Services Word Cloud", command=lambda: display_wordcloud(it_photo))
it_button.grid(row=1, column=0, padx=10, pady=10)

# Button to display Software Development word cloud
software_button = ttk.Button(plot_frame, text="Show Software Development Word Cloud", command=lambda: display_wordcloud(software_photo))
software_button.grid(row=1, column=1, padx=10, pady=10)

# Function to display word cloud image
def display_wordcloud(image):
    # Create a new window to display word cloud
    wordcloud_window = tk.Toplevel(root)
    wordcloud_window.title("Word Cloud")
    
    # Display the image
    label = tk.Label(wordcloud_window, image=image)
    label.pack(padx=10, pady=10)

root.mainloop()

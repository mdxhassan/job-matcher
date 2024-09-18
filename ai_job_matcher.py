import csv
import os
from openai import OpenAI
from dotenv import load_dotenv
from job_scrapper import job_scrapper
import tiktoken

# Set up OpenAI API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to count the token usage and ensure the prompt is within the token limit
def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def get_user_input():
    skills = input("Enter your skills (comma-separated): ")
    strengths = input("Enter your strengths: ")
    job_preferences = input("What are you looking for in a job? ")
    return skills, strengths, job_preferences

def read_job_listings(file_path):
    job_listings = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            job_listings.append(row)
    return job_listings

def get_job_recommendations(user_input, job_listings):
    user_input = f"""
    User Input:
    Skills: {user_input[0]}
    Strengths: {user_input[1]}
    Job Preferences: {user_input[2]}

    Based on the user's skills, strengths, and job preferences, recommend the top 3 most suitable jobs from the given job listings. Provide a brief explanation for each recommendation.
    Include the job title, company name, location, a short description of the job, and the job URL.
    """

    system_prompt = "You are a helpful AI assistant that matches job seekers with suitable job listings."

    fixed_tokens = num_tokens_from_string(user_input, "cl100k_base") + \
                num_tokens_from_string(system_prompt, "cl100k_base")

    # Set maximum tokens (leaving some buffer)
    max_tokens = 16385 - fixed_tokens - 100 

    # Truncate job listings to fit within token limit
    truncated_listings = []
    current_tokens = 0
    for job in job_listings:
        job_str = str(job)
        job_tokens = num_tokens_from_string(job_str, "cl100k_base")
        if current_tokens + job_tokens > max_tokens:
            break
        truncated_listings.append(job)
        current_tokens += job_tokens

    user_prompt = f"""
    {user_input}

    Job Listings:
    {truncated_listings}
    """

    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ])

    return response.choices[0].message.content

def main():
    job_scrapper()
    print("Welcome to the AI Job Matcher!")
    user_input = get_user_input()

    job_listings = read_job_listings("job_listings.csv")

    print("\nAnalyzing job listings...")
    recommendations = get_job_recommendations(user_input, job_listings)

    print("\nHere are your top 3 job recommendations:")
    print(recommendations)

if __name__ == "__main__":
    main()

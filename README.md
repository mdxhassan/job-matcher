# AI Job Matcher

AI Job Matcher is a Python program that uses OpenAI's GPT model to match job seekers with suitable start-up job listings based on their skills, strengths, and job preferences.

## Features

- When initialized, scrapes job listings from thehub.io (set to scrape the first three pages for reasonable token usage) and saves the result to job_listing.csv
- Prompt the user to input their skills, strengths, and job preferences
- Uses OpenAI's GPT model to recommend the top 3 most suitable jobs based on the user input 
- Provides the job title, job location, description & url, and a short explanations for each job recommendation

## Why thehub.io?

Thehub.io is a platform that specializes in providing job listings at Nordic start-ups. It is a great platform for job seekers to find suitable, inspiring start-up jobs. Additionally, due to its niche nature, unlike other major job listing services, thehub.io allows ethical web scraping.

## Data Extracted 
The scraper collects job listings from thehub.io, including job titles, company names, locations, job types, descriptions, and URLs. The purpose is to match these job opportunities with users' skills, ensuring relevant and personalized job recommendations. By aligning a user's skill set with the job requirements, the program helps to streamline the job search process, providing tailored opportunities that are more likely to match the user's qualifications and skills.

## Requirements

- Python 3.7+
- Required packages are listed in `requirements.txt`

## Installation

1. Clone this repository.
`mkdir job_matcher`
`cd job_matcher`
`git clone https://github.com/mdxhassan/job-matcher.git`
2. Install the required packages (it is also recommended to create a virtual environment for the installation):
`pip install -r requirements.txt`
3. Set up your OpenAI API key:
   - Create a `.env` file in the project root directory
   `cd job-matcher`
   `touch .env`
   - Add your OpenAI API key to the `.env` file:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

## Usage

To run the AI Job Matcher:

`python3 ai_job_matcher.py`

Follow the prompts to input your skills, strengths, and job preferences.

The program will display the top 3 most suitable jobs and provide explanations for each recommendation.

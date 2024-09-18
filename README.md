# AI Job Matcher

AI Job Matcher is a Python program that uses OpenAI's GPT model to match job seekers with suitable job listings based on their skills, strengths, and job preferences.

## Features

- Scrapes job listings from thehub.io
- Analyzes user input (skills, strengths, and job preferences)
- Uses OpenAI's GPT model to recommend the top 3 most suitable jobs
- Provides explanations for each job recommendation

## Requirements

- Python 3.7+
- Required packages are listed in `requirements.txt`

## Installation

1. Clone this repository or download the source code.
2. Install the required packages:
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

## License

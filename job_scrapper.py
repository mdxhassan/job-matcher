from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://thehub.io/jobs")

# Rate limiting function to avoid overwhelming the server
def rate_limit(delay=2):
    print(f"Waiting for {delay} seconds to avoid rate limiting...")
    time.sleep(delay)

def extract_job_description(job_url):
    # Open a new tab
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    
    try:
        driver.get(job_url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'view-job-details__body'))
        )
        description = driver.find_element(By.CLASS_NAME, 'view-job-details__body').text
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error extracting job description: {e}")
        description = None
    finally:
        # Close the tab and switch back to the main tab
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    
    return description

def extract_job_info(job_element):
    try:
        # Extract job title
        title = job_element.find_element(By.CLASS_NAME, 'card-job-find-list__position').text
        
        # Extract company name and location
        key_info = job_element.find_element(By.CLASS_NAME, 'bullet-inline-list.text-gray-600.fw500').text
        company, location, job_type = split_key_info(key_info)
       
        # Extract job URL
        job_link = job_element.find_element(By.CSS_SELECTOR, 'a[href^="/jobs/"]')
        job_url = job_link.get_attribute('href')
        
        # Extract job description
        description = extract_job_description(job_url)
        
        return {
            'title': title,
            'company': company,
            'location': location,
            'job_type': job_type,
            'description': description,
            'url': job_url,
        }

    except NoSuchElementException as e:
        print(f"Error finding an element: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def split_key_info(key_info):
    info_parts = key_info.split(" ")
    company = info_parts[0]
    location = info_parts[1]
    job_type = " ".join(info_parts[2:])  # This handles cases where job type might have spaces (e.g., "Part-time")
    return company, location, job_type

def job_scrapper():
    job_list = []
    # scrape the first 3 pages of jobs
    number_of_pages = 2
    try:
        for page in range(1, number_of_pages + 1):
            page_url = f"https://thehub.io/jobs?page={page}"
            # Find job listings on the page
            driver.get(page_url)
            job_elements = driver.find_elements(By.CLASS_NAME, 'my-10')

            # Loop through each job and extract info
            for job_element in job_elements:
                job_info = extract_job_info(job_element)
                if job_info:
                    # Add the job info to the list
                    job_list.append(job_info)
            # Rate limiting after each extraction
                rate_limit(1)  # Pause 1 second between each extraction
            print(f"Page {page} completed")
    except TimeoutException:
        print("Timed out waiting for page to load")
    except NoSuchElementException as e:
        print(f"Error finding job listings: {e}")
    finally:
        # Close the browser
        driver.quit()

    csv_file = 'job_listings.csv'

    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        # Create a CSV writer object
        writer = csv.DictWriter(file, fieldnames=['title', 'company', 'location', 'job_type', 'description', 'url'])
        
        # Write the header row
        writer.writeheader()
        
        # Write each job listing as a row in the CSV file
        for job in job_list:
            writer.writerow(job)

    print(f"Job listings saved to {csv_file}")
    print(f"Total number of jobs found: {len(job_list)}")


#---


# WebDriverWait(driver, 5).until(
#     EC .presence_of_element_located((By.CLASS_NAME, "gLFyf"))
#     )

# input_element = driver.find_element(By.CLASS_NAME, "gLFyf")
# input_element.clear()
# input_element.send_keys("mdxh behance" + Keys.RETURN)

# WebDriverWait(driver, 5).until(
#     EC .presence_of_element_located((By.PARTIAL_LINK_TEXT, "Mohamed"))
#     )

# link = driver.find_element(By.PARTIAL_LINK_TEXT, "Mohamed")
# link.click()

# time.sleep(10)


#WebDriverWait(driver, 5).until(
#    EC .presence_of_element_located((By.CLASS_NAME, "my-10"))
#    )

#jobs = driver.find_elements(By.CLASS_NAME, 'my-10')
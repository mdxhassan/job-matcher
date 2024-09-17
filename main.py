from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import time

service = Service(executable_path ="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://thehub.io/jobs")

# Rate limiting function to avoid overwhelming the server
def rate_limit(delay=2):
    print(f"Waiting for {delay} seconds to avoid rate limiting...")
    time.sleep(delay)

def extract_job_info(job_element):
    try:
        # Extract job title
        title = job_element.find_element(By.CLASS_NAME, 'card-job-find-list__position').text
        
        # Extract company name and location
        key_info = job_element.find_element(By.CLASS_NAME, 'bullet-inline-list.text-gray-600.fw500').text
        company, location, job_type = split_key_info(key_info)
       
        return {
            'title': title,
            'company': company,
            'location': location,
            'job_type': job_type,
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

job_list = []
try:
    # Find job listings on the page
    job_elements = driver.find_elements(By.CLASS_NAME, 'my-10')

    # Loop through each job and extract info
    for job_element in job_elements:
        job_info = extract_job_info(job_element)
        if job_info:
            # Add the job info to the list
            job_list.append(job_info)

        # Rate limiting after each extraction
        rate_limit(1)  # Pause 1 second between each extraction
except TimeoutException:
    print("Timed out waiting for page to load")
except NoSuchElementException as e:
    print(f"Error finding job listings: {e}")
finally:
    # Close the browser
    driver.quit()

print(job_list)

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
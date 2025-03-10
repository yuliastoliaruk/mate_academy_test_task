from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd

web = "https://mate.academy/"
web_driver_path = "chromedriver-win64/chromedriver.exe"

service = Service(web_driver_path)
driver = webdriver.Chrome(service=service)

driver.get(web)

courses = driver.find_elements(By.XPATH, '//a[contains(@class, "ProfessionsListSectionTemplate_card")]')

course_title, course_type, description, topics_count, modules_count, duration = [], [], [], [], [], []
course_links = []

for course in courses:
    course_title.append(course.find_element(By.XPATH, './/h3[contains(@class, "ProfessionCard_title")]').text)
    duration.append(course.find_element(By.XPATH, './/p[contains(@class, "ProfessionCard_text")]').text)
    course_links.append(course.get_attribute("href"))

for link in course_links:
    driver.get(link)

    # extract course type
    full_time = False
    flex = False
    buttons = driver.find_elements(By.XPATH, '//span[contains(@class, "ButtonBody_buttonText")]')

    for button in buttons:
        try:
            text = button.text.strip()
            if "Навчатися повний день" in text:
                full_time = True
            if "Навчатися у вільний час" in text:
                flex = True
        except StaleElementReferenceException:
            continue

    course_type.append("/".join(filter(None, ["FULL-TIME" if full_time else "", "FLEX" if flex else ""])))

    description.append(driver.find_element(By.CSS_SELECTOR, 'p.SalarySection_aboutProfession__C6ftM').text)

    # extract number of topics
    topic_elements = driver.find_elements(By.XPATH, '//p[contains(@class, "CourseModulesList_topicsCount__H_fv3")]')
    total_topics = 0
    for topic in topic_elements:
        topics_text = topic.text
        topics_number = ''.join(filter(str.isdigit, topics_text))
        if topics_number:
            total_topics += int(topics_number)
    topics_count.append(str(total_topics))

    # extract number of modules
    try:
        show_more_modules_button = driver.find_element(By.XPATH,
                                                       './/button[contains(@class, "CourseModulesList_showMore")]')
        driver.execute_script("arguments[0].click();", show_more_modules_button)
    except NoSuchElementException:
        pass

    modules = driver.find_elements(By.XPATH, '//div[contains(@class, "CourseProgram_modules__GA_PJ")]//div[contains(@class, "CourseModulesList_moduleListItem__HKJqw")]')
    modules_count.append(len(modules))

driver.quit()

df_courses = pd.DataFrame({"name": course_title, "description": description, "type": course_type, "modules_count": modules_count, "topics_count": topics_count, "duration": duration})
df_courses.to_csv("courses.csv", index=False, encoding="utf-8-sig")

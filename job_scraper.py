import requests
from bs4 import BeautifulSoup
import csv
import argparse

def scrape_jobs(keyword, location):
    url = "https://realpython.github.io/fake-jobs/"
    
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.find_all("div", class_="card-content")

    results = []

    for job in jobs:
        title = job.find("h2", class_="title").text.strip()
        company = job.find("h3", class_="company").text.strip()
        loc = job.find("p", class_="location").text.strip()

        if keyword.lower() in title.lower():
            results.append([title, company, loc])

    return results


def save_to_csv(data):
    with open("jobs.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Company", "Location"])
        writer.writerows(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Job Scraper CLI Tool")

    parser.add_argument("--keyword", type=str, default="", help="Job keyword")
    parser.add_argument("--location", type=str, default="", help="Job location")

    args = parser.parse_args()

    jobs = scrape_jobs(args.keyword, args.location)
    save_to_csv(jobs)

    print(f"Saved {len(jobs)} jobs to jobs.csv")
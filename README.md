# Automated Web Scraper + Excel Report Generator

A Python pipeline that scrapes book data from [books.toscrape.com](https://books.toscrape.com/),
saves it with a run history, and generates a formatted Excel report on a daily schedule.

![Report preview](samples/report_preview.png)

## What it does

1. **Scrapes** titles, prices, ratings, and stock status (Requests + BeautifulSoup)
2. **Cleans** the data into proper types (Pandas)
3. **Saves** the latest run and an ever-growing history as CSV
4. **Generates** a multi-sheet Excel report with summary stats and a chart (openpyxl)
5. **Runs automatically** every day via Windows Task Scheduler

## Features

- Retry logic for network failures
- Logging to file and console
- Fails loudly if the site layout changes (zero results raises an error)
- Path handling that works no matter where the script is launched from

## Project structure

```
config.py     settings and paths
scraper.py    fetch, parse, clean, save
report.py     builds the Excel report
main.py       runs the full pipeline
run_scraper.bat   launcher used by Task Scheduler
```

## Setup

```bash
git clone https://github.com/YOUR-USERNAME/book-scraper-report.git
cd book-scraper-report
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Reports appear in `reports/`, data in `data/`, logs in `logs/`.

## Scheduling (Windows)

```bash
schtasks /Create /TN "Book Scraper Report" /TR "C:\full\path\to\run_scraper.bat" /SC DAILY /ST 08:00
```

On macOS/Linux, use cron instead:
`0 8 * * * /path/to/venv/bin/python /path/to/main.py`

## What I learned

- (Write 3 to 4 honest bullets here, for example: debugging a scheduled task that
  queued but never ran because of battery settings.)

## Possible next steps

- Scrape multiple pages
- Email the report automatically
- Run on a cloud scheduler (GitHub Actions or a small server) instead of a local PC

## Note

Scraped from a practice site built for this purpose. Always check a site's
terms and robots.txt before scraping real websites.
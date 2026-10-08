import logging
import sys

from config import LOG_DIR
import scraper
import report


def setup_logging():
    LOG_DIR.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_DIR / "scraper.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def main():
    logger = logging.getLogger("main")
    logger.info("Run started")

    try:
        rows = scraper.scrape_books()
        logger.info("Scraped %d books", len(rows))

        df = scraper.clean(rows)
        scraper.save(df)
        logger.info("Data saved")

        latest, history = report.load_data()
        path = report.build_report(latest, history)
        logger.info("Report created: %s", path)

    except Exception:
        logger.exception("Run failed")
        return 1

    logger.info("Run finished successfully")
    return 0


if __name__ == "__main__":
    setup_logging()
    sys.exit(main())
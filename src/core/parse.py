from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

class TMDBParser:
    instance = None  # хранение синглтона

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(TMDBParser, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        if hasattr(self, "initialized") and self.initialized:
            return

        self.options = Options()
        self.init_driver()
        self.driver = webdriver.Chrome(options=self.options)

        self.initialized = True

    def init_driver(self):
        self.options.add_argument("--headless=new")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--log-level=3")
        self.options.add_argument("--ignore-certificate-errors")
        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.managed_default_content_settings.stylesheets": 2,
            "profile.managed_default_content_settings.fonts": 2,
            "profile.managed_default_content_settings.media_stream": 2,
        }
        self.options.add_experimental_option("prefs", prefs)

    def parse(self, content_id: int, content_type: str, locale: str = "RU"):
        content_type = "movie" if content_type == "film" else content_type
        url = f"https://www.themoviedb.org/{content_type}/{content_id}/watch?translate=false&locale={locale}"

        self.driver.get(url)

        try:
            html = self.driver.find_element(By.CSS_SELECTOR, "ul.providers").get_attribute("outerHTML")
        except:
            return []

        soup = BeautifulSoup(html, "html.parser")
        provider_items = soup.find_all("li")

        result = []
        for item in provider_items:
            if 'hide' in item.get("class", []):
                continue

            a_tag = item.find("a", href=True)
            if not a_tag:
                continue

            link = a_tag["href"]

            img_tag = a_tag.find("img")
            img_src = img_tag["src"] if img_tag else None

            result.append({
                "link": link,
                "img_src": img_src
            })

        return result

    def quit(self):
        self.driver.quit()
        TMDBParser._instance = None
        self._initialized = False

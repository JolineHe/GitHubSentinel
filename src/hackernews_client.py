import requests
from bs4 import BeautifulSoup
from logger import LOG  # 导入日志模块
import os
from datetime import datetime



class HackerNewsClient:
    def __init__(self):
        pass

    def fetch_hacker_news(self):
        # URL of Hacker News
        url = 'https://news.ycombinator.com/'
        
        # Send a GET request to the website
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code != 200:
            raise Exception(f"Failed to load page {url}")
        
        # Parse the page content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all the items with the class 'athing' which are the news items
        items = soup.find_all('tr', class_='athing')
        
        news_items = []
        
        for item in items:
            # Extract the title
            title_element = item.find('span', class_='titleline')
            if title_element:
                title = title_element.get_text()
                
                # Extract the link
                link = title_element.find('a')['href']
                
                # Sometimes the link is relative, so we need to add the base URL
                if not link.startswith('http'):
                    link = f'https://news.ycombinator.com/{link}'
                
                news_items.append({'title': title, 'link': link})
        
        return news_items
      

    def save_to_markdown(self, news_items):
        # Get the directory path for daily_progress folder in the upper level
        news_dir = os.path.join('daily_progress', "hacker_news")
        
        # Create the directory if it doesn't exist
        if not os.path.exists(news_dir):
            os.makedirs(news_dir)
        
        # Create a file name with the current date
        date_str = datetime.now().strftime('%Y-%m-%d-%H-%M')
        file_path = os.path.join(news_dir, f'{date_str}.md')
        
        # Write the news items to the markdown file
        with open(file_path, 'w') as md_file:
            md_file.write(f"# Hacker News Top Stories - {date_str}\n\n")
            for i, item in enumerate(news_items, 1):
                md_file.write(f"### {i}. {item['title']}\n")
                md_file.write(f"[Link]({item['link']})\n\n")
        
        LOG.info(f"Hacker News 热点项目文件生成：{file_path}")
        return file_path


    def export_hacker_news(self):
        news_items = self.fetch_hacker_news()
        file_path = self.save_to_markdown(news_items)
        return file_path

if __name__ == "__main__":
    client = HackerNewsClient()
    news_items = client.fetch_hacker_news()
    client.save_to_markdown(news_items)


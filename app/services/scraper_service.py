import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass, asdict
from typing import List, Optional

@dataclass
class Post:
    title: str
    url: str
    points: int
    sent_by: Optional[str]
    published: Optional[str]
    comments: int

_cached_pages = {} # pages cached

def extract_post_title(post) -> tuple[str, str]:
    try:
        a_tag = post.find("span", class_="titleline").find("a")
        title = a_tag.text.strip()
        url = a_tag["href"].strip()
        return title, url
    except Exception:
        return "", ""

def extract_subtext_data(subtext) -> tuple[int, Optional[str], Optional[str], int]:
    td = subtext.find("td", class_="subtext") if subtext else None
    if not td:
        return 0, None, None, 0

    score_tag = td.find("span", class_="score")
    points = int(score_tag.text.replace(" points", "")) if score_tag else 0

    author_tag = td.find("a", class_="hnuser")
    sent_by = author_tag.text if author_tag else None

    age_tag = td.find("span", class_="age")
    published = age_tag.text if age_tag else None

    comments_tag = td.find_all("a")[-1] if td.find_all("a") else None
    comments_text = comments_tag.text if comments_tag else ""
    if "comment" in comments_text:
        try:
            comments = int(comments_text.split()[0])
        except ValueError:
            comments = 0
    else:
        comments = 0

    return points, sent_by, published, comments

def get_posts_by_page(page: int):
    url: str = f"https://news.ycombinator.com/?p={page}"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        return [{"error": str(e)}]

    soup = BeautifulSoup(response.text, "html.parser")
    post_rows = soup.find_all("tr", class_="athing")
    page_posts = []
    for post_html in post_rows:
        subtext = post_html.find_next_sibling("tr")

        title, post_url = extract_post_title(post_html)
        if not title or not post_url:
            continue  # Skip broken posts

        points, sent_by, published, comments = extract_subtext_data(subtext)

        post = Post(
            title=title,
            url=post_url,
            points=points,
            sent_by=sent_by,
            published=published,
            comments=comments
        )
        page_posts.append(asdict(post))
    
    _cached_pages[page] = page_posts
    return page_posts

def get_posts(page: int) -> List[dict]:
    global _cached_pages
    all_posts = []
    
    for i in range(page):
        page_index = i + 1
        if page_index in _cached_pages:
            all_posts.extend(_cached_pages[page_index])
        else:
            all_posts.extend(get_posts_by_page(page_index))

    return all_posts

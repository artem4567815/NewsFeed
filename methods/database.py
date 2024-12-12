from models import NewsFiles

def get_all_news_files():
    return NewsFiles.query.all()
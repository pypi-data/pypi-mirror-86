def show(article):
    """show article"""
    print(article)

def show_list(site,titles):
    """show list of articles"""
    print(f'the latest article from {site}')
    for article_id,title in enumerate(titles):
        print(f'{article_id>3} {title}')
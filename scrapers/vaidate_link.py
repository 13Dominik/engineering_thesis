import csv


def check_has_proper_end(link: str) -> str:
    """
    Funtion to check if link has a proper ending which is #product-reviews
    :param link: Link to allegro auction
    :return: proper form of link
    """
    if not link.endswith('#product-reviews'):
        return link + '#product-reviews'
    else:
        return link


def check_if_article_in_base(title: str) -> None:
    """
    Function to check if reviews of this specific auction already in database
    :param title: title of Allegro auction
    :return: None if title no in database, or raise exception if so
    """
    used_articles = []
    with open('../data/allegro/supplements/used_articles.csv', 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for line in reader:
            used_articles.append(line)

    if [title] in used_articles:
        raise Exception("Reviews of this product already in database!")

    with open('../data/allegro/supplements/used_articles.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow([title])


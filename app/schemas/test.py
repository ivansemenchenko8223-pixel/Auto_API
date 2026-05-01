def conversion_of_text(article:str):
    new_text = article.replace(" ", "").upper()
    return new_text

a = conversion_of_text("wffwfFFF")

print(a)
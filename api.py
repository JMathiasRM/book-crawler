class BookCrawlerAPI:
    def __init__(self):
        pass

    # Retorna as informações de N livros de uma categoria
    ## cat: categoria
    ## n: número de livros para retornar
    def livrosCategoria(cat: str, n: int):
        pass

    # Salva as informações de todos os livros de uma categoria
    ## cat: categoria
    def salvarCategoria(cat: str):
        pass

    # Apaga as informações de todos os livros de uma categoria
    ## cat: categoria
    def apagarCategoria(cat: str):
        pass

    # Retorna os livros de uma categoria com estoque abaixo de N
    ## cat: categoria
    ## n: número de livros
    def estoqueCategoria(cat: str, n: int):
        pass
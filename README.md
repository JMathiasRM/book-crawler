# book-crawler
API feita com FastAPI para um crawler para o site https://books.toscrape.com/index.html.

Para executar localmente com uvicorn:
```
uvicorn api:app
```


## Funções
def livrosCategoria(cat: str, n: int, crawl: bool = False):

Retorna as informações de N livros de uma categoria

 cat: categoria
 
 n: número de livros para retornar
 
 crawl: forçar crawleamento
 


async def salvarCategoria(cat: str):

Salva as informações de todos os livros de uma categoria

 cat: categoria
 


async def apagarCategoria(cat: str):

Apaga as informações de todos os livros de uma categoria

 cat: categoria
 


async def estoqueCategoria(cat: str, n: int):

Retorna os livros de uma categoria com estoque abaixo de N

 cat: categoria
 
 n: número de livros
 

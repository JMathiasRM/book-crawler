from typing import Optional
from unittest.util import strclass
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from db import Database
from crawler import Crawler

class Livro(BaseModel):
    titulo: str
    categoria: str
    preco: float
    estoque: int
    desc: str
    data: str

app = FastAPI()
crawler = Crawler()
db = Database()

@app.get('/')
async def root():
    return

class HTTPError(BaseModel):
    detail: str
    class Config:
        schema_extra = {
            "example": {"detail": "string"},
        }

@app.get('/search',
    responses={
        400: {
            'model': HTTPError
        },
        404: {
            'model': HTTPError
        }
})
# Retorna as informações de N livros de uma categoria
## cat: categoria
## n: número de livros para retornar
## crawl: forçar crawleamento
async def livrosCategoria(cat: str, n: int, crawl: bool = False):
    if crawl:
        db.deleteCat(cat)
        crawl_res = crawler.crawl(cat)
        db.insert(crawl_res)
    if n<0:
        raise HTTPException(
            status_code=400,
            detail=f"{n} is not a valid amount of books"
        )
    livros_categoria = db.fetchN(cat,n)
    if livros_categoria==[] and n>0:
        raise HTTPException(
            status_code=404,
            detail=f"Books from category '{cat}' not found (did you capitalize the first letters?)"
        )
    return livros_categoria

@app.get('/save',
    responses={
        400: {
            'model': HTTPError
        }
})
# Salva as informações de todos os livros de uma categoria
## cat: categoria
async def salvarCategoria(cat: str):
    crawl_res = {}
    try:
        crawl_res = crawler.crawl(cat)
    except:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to crawl books from category '{cat}' (did you capitalize the first letters?)"
        )
    else:
        db.insert(crawl_res)

@app.get('/delete')
# Apaga as informações de todos os livros de uma categoria
## cat: categoria
async def apagarCategoria(cat: str):
    db.deleteCat(cat)

@app.get('/stock')
# Retorna os livros de uma categoria com estoque abaixo de N
## cat: categoria
## n: número de livros
async def estoqueCategoria(cat: str, n: int):
    return db.fetchStockN(cat, n)
from pydantic import BaseModel
from typing import Dict, List, Optional

class Preparo(BaseModel):
    ingredientes: List[str]
    modoPreparo: str

class Receita(BaseModel):
    nomeReceita: str
    descricaoReceita: str
    sentimentoReceita: List[str]
    preparos: List[Preparo]
    tempoPreparo: str
    imagemReceita: str
    qtdeFinal: int
    observacoesUsuario: str

"""
Models para o sistema de receitas
--------------------------------
"""

from pydantic import BaseModel
from typing import Dict, List, Optional

class Preparo(BaseModel):
    """Modelo para as etapas de preparo de uma receita"""
    ingredientes: List[str]
    modoPreparo: str

class Receita(BaseModel):
    """Modelo principal para as receitas"""
    id: Optional[int] = None
    nomeReceita: str
    descricaoReceita: str
    sentimentoReceita: List[str]
    preparos: List[Preparo]
    tempoPreparo: str
    imagemReceita: str
    qtdeFinal: int
    observacoesUsuario: str
    autorId: Optional[str] = None
    qtdAvaliacao: int = 0

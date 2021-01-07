# AUTOGENERATED! DO NOT EDIT! File to edit: 00_main.ipynb (unless otherwise specified).

__all__ = ['process_bin']

# Cell
from typing import *
from fastcore.xtras import Path
from fastcore.script import *
from .parser import get_files

# Cell
@call_parse
def process_bin(entrada:Param("Diretório contendo arquivos .bin", str),
                saida:Param("Diretório para salvar os arquivos de saída", str),
                pivoted: Param("Indica se o DataFrame de Nível salvo é no Formato de Tabela Dinâmica", bool_arg)=True,
                recursivo:Param("Buscar arquivos de maneira recursiva?", bool_arg)=True,
                pastas:Param("Limita a busca às pastas", Iterable[str]) = None,
                verbose:Param("Imprimir mensagens de execução?", bool_arg) = False):

        lista_bins = get_files(entrada, extensions=['.bin'], recurse=recursivo, folders=pastas)

        if verbose:
            print(lista_bins)

        return lista_bins
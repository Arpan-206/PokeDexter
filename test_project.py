import inquirer
import pytest
import requests

from project import num_validator, poke_desc_fetcher, poke_fetcher, poke_lister


def test_poke_lister():
    assert poke_lister(1) == [{'name': 'bulbasaur',
                               'url': 'https://pokeapi.co/api/v2/pokemon/1/'}]
    assert poke_lister(5) == [{'name': 'bulbasaur', 'url': 'https://pokeapi.co/api/v2/pokemon/1/'}, {'name': 'ivysaur', 'url': 'https://pokeapi.co/api/v2/pokemon/2/'}, {'name': 'venusaur',
                                                                                                                                                                         'url': 'https://pokeapi.co/api/v2/pokemon/3/'}, {'name': 'charmander', 'url': 'https://pokeapi.co/api/v2/pokemon/4/'}, {'name': 'charmeleon', 'url': 'https://pokeapi.co/api/v2/pokemon/5/'}]


def test_num_validator():
    assert num_validator("56", "56") == True
    with pytest.raises(inquirer.errors.ValidationError):
        num_validator("56", "ab")


def test_poke_fetcher():
    assert poke_fetcher('ivysaur') == requests.get(
        "https://pokeapi.co/api/v2/pokemon/2/").json()
    assert poke_fetcher('bulbasaur') == requests.get(
        "https://pokeapi.co/api/v2/pokemon/1/").json()


def test_poke_desc_fetcher():
    assert poke_desc_fetcher(poke_fetcher(
        'bulbasaur')) == "While it is young, it uses the nutrients that are\nstored in the seed on its back in order to grow."

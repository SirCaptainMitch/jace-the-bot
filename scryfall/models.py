from pydantic import BaseModel, Field


class Scryfall(BaseModel):
    """
    The main client for interfacing with Scryfall
    """
    BaseEndpoint: str = Field(alias='base_endpoint', default='https://api.scryfall.com')


class Catalog(BaseModel):
    """
    The core base class for a catalog ( Type ).
    """
    Name: str = Field(alias='name')


class Land(Catalog):
    """
    Represents a land within the game.
    """


class Artist(Catalog):
    """
    Represents an artist for MTG art.
    """


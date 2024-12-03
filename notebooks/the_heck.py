import pandas as pd
from src.jace.main import parse_oracle_cards
from src.jace.database import db

cards = [dict(_) for _ in parse_oracle_cards()]

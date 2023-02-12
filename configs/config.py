from dataclasses import dataclass
from environs import Env


@dataclass
class Config:
    token: str
    admins: list


def load_config(path) -> Config:

    env: Env = Env()
    env.read_env(path)

    return Config(token=env("BOT_TOKEN"), admins=env("ADMINS_ID"))

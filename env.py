from environs import Env 


class EnvConfig:
    def __init__(self):
        self.env = Env()
        self.env.read_env()

    @property
    def OPEN_AI_KEY(self):
        return self.env("OPENAI_API_KEY")


env = EnvConfig()

__all__ = ['env']
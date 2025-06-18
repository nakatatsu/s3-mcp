from environs import Env

env = Env()
env.read_env()


class Config:
    @property
    def AWS_ACCESS_KEY_ID(self) -> str:
        return env.str("AWS_ACCESS_KEY_ID")

    @property
    def AWS_SECRET_ACCESS_KEY(self) -> str:
        return env.str("AWS_SECRET_ACCESS_KEY")

    @property
    def AWS_REGION(self) -> str:
        return env.str("AWS_REGION", "us-west-1")
    
    @property
    def AWS_S3_BUCKET(self) -> str:
        return env.str("AWS_S3_BUCKET")
    
    @property
    def AWS_S3_PREFIX(self) -> str:
        return env.str("AWS_S3_PREFIX", "logs")


env = Config()  # type: ignore
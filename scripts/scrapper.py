import yaml
from pydantic import BaseModel, HttpUrl
from typing import Literal
import os
import requests

class IConfigDocument(BaseModel):
    id: str
    name: str
    download_url: HttpUrl
    type: Literal['spec', 'tool']

class IConfig(BaseModel):
    documents: list[IConfigDocument]


class Config:
    def __init__(self, config: IConfig) -> None:
        self.config = config

    def get(self, id: str = "specv3")-> IConfigDocument:
        for document in self.config.documents:
            if document.id == id:
                return document
            
    def list(self) -> IConfig:
        return self.config

    @staticmethod
    def load(config_path: str = os.path.join(os.getcwd(), 'scrapper_config.yml')):
        with open(config_path, 'r') as file:
            raw_data = yaml.safe_load(file)
            config = IConfig(**raw_data)
            return Config(config)
    


def fetch_data(url: HttpUrl) -> None | str:
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.text


def scrapeAll(config: Config):
    folder_path = ".downloads"
    os.makedirs(folder_path, exist_ok=True)
    for document in config.list().documents:
        content = fetch_data(document.download_url)
        if content != None:
            file_path = os.path.join(os.getcwd(), folder_path, f"{document.id}.md")
            with open(file_path, 'w') as f:
                f.write(content)



if __name__ == "__main__":
    config = Config.load()
    scrapeAll(config)
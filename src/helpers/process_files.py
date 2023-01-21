import shutil
from pathlib import Path
from datetime import datetime
from logging import getLogger

import aiofiles
import os
from fastapi import UploadFile

PATH = Path("/tmp/test")
logger = getLogger("__name__")
logger.setLevel("WARNING")


async def delete_files():
    folder = PATH
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except OSError as e:
            logger.error(f"Failed to delete {file_path}. Reason: {e}")


class ProcessFiles:
    wheat: str
    seeds: dict
    basket: list[UploadFile]
    trash: list
    to_process: list

    def __init__(self, expected_content_type: str, files: list[UploadFile]):
        self.wheat = expected_content_type
        self.basket = files
        self.trash = []
        self.seeds = {}
        self.to_process = []
        self.path = PATH

    def recognize_seeds(self) -> dict:
        self.seeds.fromkeys(self.basket)
        for file in self.basket:
            self.seeds[file] = file.content_type
        return self.seeds

    def separate_wheat_form_chaff(self) -> list[UploadFile]:
        for seed, seed_type in self.seeds.items():
            if self.wheat == seed_type:
                self.to_process.append(seed)
            else:
                self.trash.append(seed)
        return self.to_process

    async def write_files(self, out_file_path: Path = Path(PATH)):
        out_file_path.mkdir(exist_ok=True)
        for seed in self.to_process:
            timestamp = datetime.now().timestamp()
            filename = f"{timestamp}_{seed.filename}"
            async with aiofiles.open(out_file_path.joinpath(filename), 'wb') as out_file:
                content = await seed.read()  # async read
                await out_file.write(content)

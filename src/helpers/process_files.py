from pathlib import Path
from datetime import datetime


import aiofiles
from fastapi import UploadFile

PATH = Path("/tmp/test")


class ProcessFiles:
    wheat: str
    seeds: dict
    basket: list[UploadFile]
    trash: list

    def __init__(self, expected_content_type: str, files: list[UploadFile]):
        self.wheat = expected_content_type
        self.basket = files
        self.trash = []
        self.seeds = {}

    def recognize_seeds(self) -> dict:
        self.seeds.fromkeys(self.basket)
        for file in self.basket:
            self.seeds[file] = file.content_type
        return self.seeds

    def separate_wheat_form_chaff(self) -> list[UploadFile]:
        for seed, seed_type in self.seeds.items():
            if self.wheat == seed_type:
                self.basket.append(seed)
            else:
                self.trash.append(seed)
        return self.basket

    async def write_files(self, out_file_path: Path = Path(PATH)):
        out_file_path.mkdir(exist_ok=True)
        for seed in self.basket:
            timestamp = datetime.now().timestamp()
            filename = f"{timestamp}_{seed.filename}"
            async with aiofiles.open(out_file_path.joinpath(filename), 'wb') as out_file:
                content = await seed.read()  # async read
                await out_file.write(content)

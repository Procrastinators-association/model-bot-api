import uvicorn
from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse

from src.helpers.process_files import ProcessFiles
from src.helpers.process_files import delete_files
from src.spec.result import ResultError, ResultOk
from src.spec.process_files import ProcessFiles as ProcessFilesSpec

app = FastAPI()


@app.get("/")
async def main() -> HTMLResponse:
    content = """
<body>
<form action="/upload/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)


@app.post("/upload/")
async def create_upload_file(files: list[UploadFile]) -> ProcessFilesSpec:
    process = ProcessFiles(expected_content_type="image/jpeg", files=files)
    process.recognize_seeds()
    process.separate_wheat_form_chaff()
    await process.write_files()
    return ProcessFilesSpec(accepted=process.to_process, not_accepted=process.trash)


@app.delete("/upload/")
async def delete_processed_files() -> ResultOk | ResultError:
    await delete_files()
    return ResultOk()


if __name__ == "__main__":
    uvicorn.run(app)

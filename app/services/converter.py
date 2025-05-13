import asyncio
import os
import tempfile

async def convert_word_file(file):
    docx_bytes = await file.read()

    with tempfile.TemporaryDirectory() as temp_dir:
        input_path = os.path.join(temp_dir, "input.docx")
        output_path = os.path.join(temp_dir, "input.pdf")

        with open(input_path, "wb") as f:
            f.write(docx_bytes)

        # Call libreoffice in headless mode
        cmd = [
            "libreoffice",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            temp_dir,
            input_path,
        ]

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise Exception(f"LibreOffice conversion failed: {stderr.decode()}")

        with open(output_path, "rb") as f:
            pdf_data = f.read()

        return pdf_data

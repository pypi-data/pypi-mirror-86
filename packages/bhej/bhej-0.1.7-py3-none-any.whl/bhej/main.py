import cgi
import magic
import os

from .utils import compress, decompress, check_and_rename, output, check_bhej_version, handleNetworkError
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from tqdm import tqdm
import pandas as pd
from io import BytesIO
import requests
import typer

from .config import URL

app = typer.Typer()

@app.command("up")
def cli_up(filename: str):
    return up(filename, cli = True)

def up(filename: str, cli: bool = False):
    check_bhej_version()

    try:
        typer.echo(f"Compressing {filename}")
        compressed_filename = compress(filename)
        file = open(compressed_filename, "rb").read()

        if len(file) > 1048576:
            typer.echo(
                "Compressed file size too large. Compressed files must be smaller than 1GB. Aborting."
            )
            raise typer.Exit(code=8)

        mime = magic.Magic(mime=True)
        files = {"upload_file": (filename, file, mime.from_file(filename))}
    except FileNotFoundError:
        typer.echo(f"No such file: '{filename}'. Aborting.")
        raise typer.Exit(code=3)
    except IsADirectoryError:
        files = {"upload_file": (filename, file, "application/x-gzip")}
    except Exception as err:
        typer.echo(f"Unexpected Error: {str(err)}")
        raise (err)

    output(f"Uploading {filename}", cli)

    e = MultipartEncoder(fields=files)

    with tqdm(total=e.len, dynamic_ncols=True, unit="B", unit_scale=True) as bar:
        m = MultipartEncoderMonitor(
            e, lambda monitor: bar.update(monitor.bytes_read - bar.n)
        )
        try:
            req = requests.post(
                URL + "/upload", data=m, headers={"Content-Type": m.content_type}
            )
        except Exception:
            handleNetworkError(cli)

    if req.status_code == 500:
        output("There was an unexpected server error. Please try again later.", cli)
        raise typer.Exit(code=7)

    code = req.text
    link = f"{URL}/file/{code}"

    output(f"Upload successful! Your code is -> {code}", cli)
    output(f"You can also download the file directly at {link}", cli)

    os.unlink(compressed_filename)

    return

@app.command("down")
def cli_down(filecode: str, dest: str = '.'):
    return down(filecode, dest, cli = True)
    
def down(filecode: str, dest: str = '.', cli: bool = False, return_file: bool = False, return_df: bool = False):
    check_bhej_version()
    # TODO: Add an option to change the file name?

    if not os.path.exists(dest):
        output(f"No such location: {dest}. Aborting.", cli)
        return

    if not os.path.isdir(dest):
        output(f"{dest} is not a directory. Aborting.", cli)
        # TODO: Add a prompt to ask whether you'd like to create the dir.
        return

    dest = os.path.join(dest, "")  # Adds trailing slash if missing.

    output(f"Downloading {filecode}", cli)
    req = requests.get(URL + "/download/" + filecode, stream=True)

    total_size_in_bytes = int(req.headers.get("Content-Length", 0))

    block_size = 1024
    progress_bar = tqdm(
        total=total_size_in_bytes, dynamic_ncols=True, unit="B", unit_scale=True
    )

    try:
        _, params = cgi.parse_header(req.headers["Content-Disposition"])
    except KeyError:
        output(f"File associated with {filecode} not found. Please check code.", cli)
        raise typer.Exit(code=10)
    except Exception as err:
        output("An unexpected error occurred", cli)
        output(err, cli)
        raise typer.Exit(code=11)

    filename = params["filename"]

    fname = dest + filename

    with open(fname, "wb") as file:
        for data in req.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)

    progress_bar.close()

    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")

    output(f"Downloaded {fname}. Starting decompression.", cli)

    dest_file = decompress(fname)

    os.remove(fname)

    output(f"Done!", cli)

    if return_df and os.path.isfile(dest_file):
        if "text/csv" in req.headers['Content-Type']:
            return pd.read_csv(dest_file, encoding="latin1")
        else:
            output(f"{dest_file} is not a csv file.", cli)

    if return_file:
        try:
            return BytesIO(open(dest_file, 'rb').read())
        except _:
            output(f"Error returning {dest_file}.", cli)
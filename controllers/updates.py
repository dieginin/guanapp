import os
import shutil
import subprocess
import sys
import time

import flet as ft
import requests

from config import APP_VERSION

VERSION_URL = "https://raw.githubusercontent.com/dieginin/guanapp/main/version.json"

from .helpers import error_snackbar, success_snackbar

IS_WINDOWS = os.name == "nt"
IS_MAC = sys.platform == "darwin"
IS_LINUX = sys.platform.startswith("linux")

DOWNLOAD_PATH = "update.exe" if IS_WINDOWS else "update_new"


def check_for_updates(page: ft.Page) -> None:
    try:
        response = requests.get(VERSION_URL)
        if response.status_code == 200:
            data = response.json()
            latest_version = data.get("version", "")
            download_url = (
                data.get("windows")
                if IS_WINDOWS
                else (
                    data.get("mac")
                    if IS_MAC
                    else data.get("linux") if IS_LINUX else None
                )
            )

            if latest_version > APP_VERSION and download_url:
                page.open(
                    ft.AlertDialog(
                        title=ft.Text("Nueva actualización disponible"),
                        content=ft.Text(
                            f"Versión {latest_version} disponible. Se actualizará automáticamente."
                        ),
                        actions=[
                            ft.TextButton(
                                "Aceptar",
                                on_click=lambda e: __start_update(download_url, page),
                            )
                        ],
                        actions_alignment=ft.MainAxisAlignment.CENTER,
                    )
                )
    except Exception as e:
        error_snackbar(page, f"Error al buscar actualizaciones: {e}")


def __start_update(download_url: str, page: ft.Page) -> None:
    progress_bar = ft.ProgressBar(width=400)
    page.add(progress_bar)
    page.update()

    response = requests.get(download_url, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    downloaded_size = 0

    with open(DOWNLOAD_PATH, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
                downloaded_size += len(chunk)
                progress_bar.value = downloaded_size / total_size
                page.update()

    if not IS_WINDOWS:
        os.chmod(DOWNLOAD_PATH, 0o755)

    success_snackbar(page, "Actualización descargada. Reiniciando aplicación...")
    __update_and_restart()


def __update_and_restart() -> None:
    current_exe = sys.executable
    backup_exe = current_exe + ".bak"

    time.sleep(2)

    shutil.move(current_exe, backup_exe)
    shutil.move(DOWNLOAD_PATH, current_exe)

    if not IS_WINDOWS:
        os.chmod(current_exe, 0o755)

    subprocess.Popen([current_exe])

    os._exit(0)

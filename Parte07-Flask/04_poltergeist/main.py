import json
import os
import subprocess
import sys
import threading
import webbrowser
from datetime import date
from pathlib import Path

import webview

APP_NAME = "Git Poltergeist v2.0"
DEFAULT_PROJECT = r"C:\Users\ALUNO\Rômulo Delalíbera Júnior\desenvolvedor_python_qua.544.003"
CONFIG_DIR = Path(os.environ.get("APPDATA", str(Path.home()))) / "GitPoltergeist"
CONFIG_FILE = CONFIG_DIR / "config.json"


def hoje():
    return date.today().strftime("%d/%m/%Y")


def load_project_folder():
    try:
        if CONFIG_FILE.exists():
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            folder = data.get("project_folder", "").strip()
            if folder and os.path.isdir(folder):
                return folder
    except Exception:
        pass
    return DEFAULT_PROJECT if os.path.isdir(DEFAULT_PROJECT) else ""


def save_project_folder(folder):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(
        json.dumps({"project_folder": folder}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


class GitAPI:
    def __init__(self):
        self.folder = load_project_folder()
        self.remote_url = ""
        self.window = None
        self.running = False

    def js(self, code):
        if self.window:
            try:
                self.window.run_js(code)
            except Exception:
                pass

    def send(self, kind, value):
        payload = json.dumps(str(value), ensure_ascii=False)
        calls = {
            "log": f"addLog({payload})",
            "status": f"setStatus({payload})",
            "folder": f"setFolder({payload})",
            "link": f"setLink({payload})",
        }
        if kind in calls:
            self.js(calls[kind])

    def get_info(self):
        return {"folder": self.folder, "remote": self.remote_url}

    def change_folder(self):
        directory = self.folder if self.folder and os.path.isdir(self.folder) else str(Path.home())
        try:
            result = self.window.create_file_dialog(
                webview.FileDialog.FOLDER,
                directory=directory,
            )
        except AttributeError:
            # Compatibility with older pywebview releases.
            result = self.window.create_file_dialog(
                webview.FOLDER_DIALOG,
                directory=directory,
            )

        if result:
            folder = result[0] if isinstance(result, (tuple, list)) else result
            if folder:
                self.folder = folder
                save_project_folder(folder)
                self.send("folder", folder)
                return {"folder": folder}
        return {"folder": ""}

    def open_remote(self):
        if self.remote_url:
            webbrowser.open(self.remote_url)
        return True

    def git_available(self):
        try:
            return subprocess.run(
                ["git", "--version"], capture_output=True, text=True
            ).returncode == 0
        except FileNotFoundError:
            return False

    def run_git(self, args):
        p = subprocess.run(
            ["git"] + args,
            cwd=self.folder,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        output = ((p.stdout or "") + (p.stderr or "")).strip()
        if output:
            self.send("log", output)
        return p.returncode, output

    def get_remote(self):
        p = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=self.folder,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        return p.stdout.strip().splitlines()[0] if p.returncode == 0 and p.stdout.strip() else ""

    def run_commit(self):
        if self.running:
            self.send("log", "⚠ Um Auto Commit já está em execução.")
            return False
        self.running = True
        threading.Thread(target=self._commit, daemon=True).start()
        return True

    def _commit(self):
        try:
            self.send("status", "Executando Auto Commit...")
            self.send("log", "=" * 70)
            self.send("log", "👻 GIT POLTERGEIST v2.0 • WEBVIEW")
            self.send("log", "=" * 70)
            self.send("log", f"📁 Pasta: {self.folder}")

            if not self.folder or not os.path.isdir(self.folder):
                self.send("status", "Selecione uma pasta.")
                self.send("log", "⚠ A pasta salva não existe mais.")
                return

            if not self.git_available():
                self.send("status", "Git não encontrado.")
                self.send("log", "❌ Instale o Git para Windows.")
                return

            self.remote_url = self.get_remote()
            self.send("link", self.remote_url)
            self.send("log", f"🔗 GitHub: {self.remote_url}" if self.remote_url else "⚠ Link do GitHub não configurado.")

            check = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                cwd=self.folder,
                capture_output=True,
                text=True,
            )
            if check.returncode != 0:
                self.send("status", "Não é um repositório Git.")
                self.send("log", "❌ A pasta não é um repositório Git.")
                return

            branch_code, branch = self.run_git(["rev-parse", "--abbrev-ref", "HEAD"])
            if branch_code != 0 or not branch.strip():
                self.send("status", "Erro ao descobrir a branch.")
                return
            branch = branch.strip()
            self.send("log", f"🌿 Branch: {branch}")

            self.send("log", "[1/4] git add .")
            code, _ = self.run_git(["add", "."])
            if code != 0:
                self.send("status", "❌ git add falhou.")
                return

            self.send("log", "[2/4] verificando alterações...")
            diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=self.folder)
            if diff.returncode == 0:
                self.send("log", "⚠ Nenhuma alteração nova para commit.")
                self.send("status", "✓ Tudo já está atualizado.")
                return

            message = f"Commit {hoje()}"
            self.send("log", f'[3/4] git commit -m "{message}"')
            code, _ = self.run_git(["commit", "-m", message])
            if code != 0:
                self.send("status", "❌ Commit falhou.")
                return

            self.send("log", f"[4/4] git push origin {branch}")
            code, _ = self.run_git(["push", "origin", branch])
            if code != 0:
                self.send("status", "⚠ Commit criado, push falhou.")
                return

            self.send("log", "")
            self.send("log", "✓ Arquivos adicionados")
            self.send("log", "✓ Commit criado")
            self.send("log", "✓ Push enviado para o GitHub")
            self.send("log", "✓ AUTO COMMIT CONCLUÍDO!")
            self.send("status", "✓ Concluído.")
        except Exception as e:
            self.send("log", f"❌ ERRO: {e}")
            self.send("status", "❌ Erro.")
        finally:
            self.running = False


def main():
    api = GitAPI()
    root = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    index = root / "index" / "index.html"
    window = webview.create_window(
        APP_NAME,
        url=str(index),
        js_api=api,
        width=1050,
        height=700,
        min_size=(820, 560),
        resizable=True,
        background_color="#0b1020",
        text_select=True,
    )
    api.window = window
    webview.start()


if __name__ == "__main__":
    main()

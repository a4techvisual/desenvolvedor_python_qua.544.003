import json
import os
import subprocess
import sys
import threading
import tkinter as tk
from datetime import date
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
import webbrowser

# Compatibilidade com PyInstaller --windowed/--noconsole: nesses modos
# o Windows pode deixar stdout/stderr como None.
if os.name == "nt":
    if sys.stdout is None:
        sys.stdout = open(os.devnull, "w")
    if sys.stderr is None:
        sys.stderr = open(os.devnull, "w")

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

    if os.path.isdir(DEFAULT_PROJECT):
        return DEFAULT_PROJECT
    return ""


def save_project_folder(folder):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(
        json.dumps({"project_folder": folder}, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def hidden_process_kwargs():
    """Configura subprocessos para nunca criarem uma janela CMD no Windows."""
    kwargs = {
        "creationflags": getattr(subprocess, "CREATE_NO_WINDOW", 0),
    }
    if os.name == "nt":
        startup = subprocess.STARTUPINFO()
        startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startup.wShowWindow = 0
        kwargs["startupinfo"] = startup
    return kwargs


class GitPoltergeist:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("900x620")
        self.root.minsize(760, 500)

        self.folder = load_project_folder()
        self.remote_url = ""
        self.github_account = ""
        self.github_connected = False
        self.running = False

        self.build()
        self.root.after(250, self.startup_check)

    def build(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        main = ttk.Frame(self.root, padding=18)
        main.pack(fill="both", expand=True)

        ttk.Label(
            main, text="👻 Git Poltergeist",
            font=("Segoe UI", 25, "bold")
        ).pack(anchor="w")

        ttk.Label(
            main, text="Auto Commit • execução manual",
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(0, 10))

        info = ttk.LabelFrame(main, text="Projeto salvo", padding=10)
        info.pack(fill="x", pady=(0, 10))

        self.folder_label = ttk.Label(
            info,
            text=self.folder or "Nenhuma pasta configurada",
            font=("Segoe UI", 9)
        )
        self.folder_label.pack(side="left", fill="x", expand=True)

        ttk.Button(
            info, text="▶ Executar Commit",
            command=self.start_commit
        ).pack(side="right", padx=(8, 0))

        ttk.Button(
            info, text="📁 Mudar pasta",
            command=self.change_folder
        ).pack(side="right", padx=(8, 0))

        github_box = ttk.Frame(info)
        github_box.pack(side="right")

        self.github_button = ttk.Button(
            github_box, text="🔐 Entrar no GitHub",
            command=self.github_button_action
        )
        self.github_button.pack(side="left")

        self.github_menu = tk.Menu(self.github_button, tearoff=False)
        self.github_menu.add_command(label="🔄 Trocar conta", command=self.github_switch_account)
        self.github_menu.add_command(label="🚪 Deslogar", command=self.github_logout)
        self.github_status = ttk.Label(
            github_box, text="  • verificando...",
            font=("Segoe UI", 9)
        )
        self.github_status.pack(side="left", padx=(5, 0))

        self.console = tk.Text(
            main, font=("Consolas", 10), wrap="word",
            state="disabled"
        )
        self.console.pack(fill="both", expand=True)

        bottom = ttk.Frame(main)
        bottom.pack(fill="x", pady=(10, 0))

        self.status = ttk.Label(bottom, text="Pronto. Clique em Executar Commit.")
        self.status.pack(side="left")

        self.link = ttk.Label(
            bottom, text="",
            cursor="hand2",
            font=("Segoe UI", 9, "underline")
        )
        self.link.pack(side="right")
        self.link.bind("<Button-1>", lambda e: self.open_remote())

    def log(self, text):
        self.root.after(0, self._log, text)

    def _log(self, text):
        self.console.configure(state="normal")
        self.console.insert("end", text + "\n")
        self.console.see("end")
        self.console.configure(state="disabled")

    def set_status(self, text):
        self.root.after(0, lambda: self.status.configure(text=text))

    def set_github_status(self, text):
        self.root.after(0, lambda: self.github_status.configure(text=text))

    def startup_check(self):
        if not self.folder:
            self.log("⚠ Nenhuma pasta configurada.")
            self.log("Escolha a pasta uma única vez. Ela ficará salva.")
            self.set_status("Selecione a pasta.")
            self.change_folder()
        else:
            self.log("✓ Pasta salva carregada.")
            self.set_status("Iniciando Auto Commit...")

        threading.Thread(target=self.startup_auth_then_commit, daemon=True).start()

    def startup_auth_then_commit(self):
        # Ao abrir pelo ícone, o Auto Commit é executado automaticamente.
        # O botão "▶ Executar Commit" fica disponível para repetir quando quiser.
        self.check_github_auth()
        if self.folder and os.path.isdir(self.folder):
            self.root.after(0, self.start_commit)

    def change_folder(self):
        folder = filedialog.askdirectory(
            title="Selecione a pasta principal do projeto",
            initialdir=(
                self.folder if self.folder and os.path.isdir(self.folder)
                else str(Path.home())
            )
        )

        if folder:
            self.folder = folder
            save_project_folder(folder)
            self.folder_label.configure(text=folder)
            self.log("")
            self.log(f"📁 Pasta salva: {folder}")
            self.set_status("Pasta salva. Clique em Executar Commit.")

    def start_commit(self):
        if self.running:
            return

        if not self.folder:
            self.change_folder()
            if not self.folder:
                return

        if not os.path.isdir(self.folder):
            messagebox.showerror(APP_NAME, "A pasta salva não existe mais. Escolha outra pasta.")
            self.change_folder()
            return

        self.running = True
        self.set_status("Executando commit...")
        threading.Thread(target=self.commit, daemon=True).start()

    def finish_run(self):
        self.running = False
        self.root.after(0, lambda: None)

    def github_button_action(self):
        """Botão dinâmico: login quando desconectado; menu da conta quando conectado."""
        if self.github_connected:
            try:
                x = self.github_button.winfo_rootx()
                y = self.github_button.winfo_rooty() + self.github_button.winfo_height()
                self.github_menu.post(x, y)
            finally:
                self.github_menu.grab_release() if self.github_menu.grab_current() == str(self.github_menu) else None
        else:
            self.github_login()

    def github_login(self):
        if self.running:
            self.log("⚠ Aguarde o Auto Commit terminar antes de iniciar o login.")
            return
        threading.Thread(target=self._github_login_worker, daemon=True).start()

    def check_github_auth(self):
        """Identifica uma conta GitHub já autenticada nesta máquina, sem abrir CMD."""
        account = ""

        try:
            p = subprocess.run(
                ["git", "credential-manager", "github", "list"],
                capture_output=True, text=True, encoding="utf-8", errors="replace",
                timeout=8, **hidden_process_kwargs()
            )
            output = ((p.stdout or "") + "\n" + (p.stderr or "")).strip()
            if p.returncode == 0 and output:
                lower = output.lower()
                bad = ("no account", "no accounts", "not logged", "not found")
                if not any(x in lower for x in bad):
                    lines = [line.strip() for line in output.splitlines() if line.strip()]
                    if lines:
                        account = lines[0]
        except Exception:
            pass

        if not account:
            try:
                p = subprocess.run(
                    ["gh", "auth", "status", "--active", "--hostname", "github.com"],
                    capture_output=True, text=True, encoding="utf-8", errors="replace",
                    timeout=8, **hidden_process_kwargs()
                )
                output = ((p.stdout or "") + "\n" + (p.stderr or "")).strip()
                if p.returncode == 0 and output:
                    for line in output.splitlines():
                        if "logged in to github.com" in line.lower():
                            account = line.strip()
                            break
            except Exception:
                pass

        self.github_account = account
        self.github_connected = bool(account)
        if account:
            self.root.after(0, self.update_github_ui)
            self.log(f"🔐 GitHub: já conectado ({account})")
        else:
            self.root.after(0, self.update_github_ui)
            self.log("🔐 GitHub: nenhuma autenticação encontrada nesta máquina.")

    def update_github_ui(self):
        if self.github_connected:
            account = self.github_account
            self.github_button.configure(text=f"✓ GitHub: {account}")
            self.github_status.configure(text="  • conectado")
            self.github_menu.entryconfigure(0, state="normal")
            self.github_menu.entryconfigure(1, state="normal")
        else:
            self.github_button.configure(text="🔐 Entrar no GitHub")
            self.github_status.configure(text="  • não conectado")
            self.github_menu.entryconfigure(0, state="normal")
            self.github_menu.entryconfigure(1, state="disabled")

    def github_switch_account(self):
        if self.running:
            self.log("⚠ Aguarde o Auto Commit terminar antes de trocar a conta.")
            return
        self.github_logout(relogin=True)

    def github_logout(self, relogin=False):
        if self.running:
            self.log("⚠ Aguarde o Auto Commit terminar antes de deslogar.")
            return

        threading.Thread(target=self._github_logout_worker, args=(relogin,), daemon=True).start()

    def _github_logout_worker(self, relogin=False):
        try:
            if not self.git_available():
                raise RuntimeError("Git não encontrado.")

            logout = subprocess.run(
                ["git", "credential-manager", "github", "logout"],
                capture_output=True, text=True, encoding="utf-8", errors="replace",
                timeout=30, **hidden_process_kwargs()
            )
            output = ((logout.stdout or "") + "\n" + (logout.stderr or "")).strip()
            if logout.returncode != 0:
                raise RuntimeError(output or "Não foi possível deslogar do GitHub.")

            self.github_account = ""
            self.github_connected = False
            self.root.after(0, self.update_github_ui)
            self.set_status("GitHub deslogado.")
            self.log("🚪 GitHub: conta desconectada.")

            if relogin:
                self.root.after(150, self.github_login)
            else:
                self.root.after(0, lambda: messagebox.showinfo(APP_NAME, "A conta do GitHub foi deslogada."))
        except Exception as e:
            self.log(f"❌ Logout GitHub: {e}")
            self.root.after(0, lambda: messagebox.showerror(APP_NAME, str(e)))

    def _github_login_worker(self):
        try:
            if not self.git_available():
                raise RuntimeError(
                    "Git não encontrado. Instale o Git para Windows e tente novamente."
                )

            configure = subprocess.run(
                ["git", "credential-manager", "configure"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=15,
                **hidden_process_kwargs()
            )
            if configure.returncode != 0:
                detail = (configure.stderr or configure.stdout or "").strip()
                raise RuntimeError(
                    "O Git Credential Manager não está disponível.\n\n"
                    + (detail or "Instale/reinstale o Git para Windows.")
                )

            self.set_status("🔐 Aguardando login no GitHub...")
            self.log("")
            self.log("🔐 Abrindo login do GitHub...")
            self.log("   Faça login no navegador e autorize o Git Credential Manager.")

            env = os.environ.copy()
            env["GCM_GITHUB_AUTHMODES"] = "oauth"

            login = subprocess.run(
                ["git", "credential-manager", "github", "login"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                env=env,
                timeout=300,
                **hidden_process_kwargs()
            )

            output = ((login.stdout or "") + "\n" + (login.stderr or "")).strip()
            if output:
                self.log(output)

            if login.returncode != 0:
                raise RuntimeError(
                    "O login do GitHub não foi concluído."
                    + (f"\n\n{output}" if output else "")
                )

            self.check_github_auth()
            self.set_status("✓ GitHub conectado. Pronto para usar.")
            self.root.after(0, lambda: messagebox.showinfo(
                APP_NAME,
                "✓ GitHub conectado com sucesso!\n\n"
                "Agora clique em '▶ Executar Commit' quando quiser enviar as alterações."
            ))

        except subprocess.TimeoutExpired:
            self.log("❌ Login GitHub: tempo limite excedido.")
            self.set_status("❌ Login não concluído.")
            self.root.after(0, lambda: messagebox.showerror(
                APP_NAME, "O login demorou demais e foi encerrado."
            ))
        except Exception as e:
            self.log(f"❌ Login GitHub: {e}")
            self.set_status("❌ Login não concluído.")
            self.root.after(0, lambda: messagebox.showerror(APP_NAME, str(e)))

    def git_available(self):
        try:
            p = subprocess.run(
                ["git", "--version"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=8,
                **hidden_process_kwargs()
            )
            return p.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def run_git(self, args):
        p = subprocess.run(
            ["git"] + args,
            cwd=self.folder,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            **hidden_process_kwargs()
        )
        output = ((p.stdout or "") + "\n" + (p.stderr or "")).strip()
        if output:
            self.log(output)
        return p.returncode, output

    def get_remote(self):
        code, output = self.run_git(["remote", "get-url", "origin"])
        if code == 0:
            return output.strip().splitlines()[0] if output.strip() else ""
        return ""

    def show_remote(self, url):
        if not url:
            self.root.after(
                0, lambda: self.link.configure(text="⚠ Link do GitHub não configurado")
            )
            return

        self.remote_url = url
        self.root.after(0, lambda: self.link.configure(text=f"🔗 {url}"))
        self.log(f"🔗 GitHub: {url}")

    def open_remote(self):
        if self.remote_url:
            webbrowser.open(self.remote_url)

    def commit(self):
        try:
            self.log("=" * 70)
            self.log("👻 GIT POLTERGEIST v2.0")
            self.log("=" * 70)
            self.log(f"📁 Pasta: {self.folder}")

            if not os.path.isdir(self.folder):
                raise RuntimeError("A pasta salva não existe mais.")

            if not self.git_available():
                raise RuntimeError(
                    "Git não encontrado. Instale o Git para Windows e tente novamente."
                )

            self.log("🔐 Verificando login do GitHub...")
            self.check_github_auth()

            self.log("🔗 Buscando link do GitHub...")
            self.remote_url = self.get_remote()
            self.show_remote(self.remote_url)

            check = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                cwd=self.folder,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                **hidden_process_kwargs()
            )
            if check.returncode != 0:
                raise RuntimeError("A pasta selecionada não é um repositório Git.")

            branch_code, branch = self.run_git(["rev-parse", "--abbrev-ref", "HEAD"])
            if branch_code != 0 or not branch.strip():
                raise RuntimeError("Não foi possível descobrir a branch.")

            branch = branch.strip()
            self.log(f"🌿 Branch: {branch}")

            self.log("[1/4] git add .")
            code, _ = self.run_git(["add", "."])
            if code != 0:
                raise RuntimeError("git add . falhou.")

            self.log("[2/4] verificando alterações...")
            diff = subprocess.run(
                ["git", "diff", "--cached", "--quiet"],
                cwd=self.folder,
                **hidden_process_kwargs()
            )

            if diff.returncode == 0:
                self.log("⚠ Nenhuma alteração nova para commit.")
                self.show_remote(self.remote_url)
                self.set_status("✓ Tudo já está atualizado.")
                self.root.after(
                    0,
                    lambda: messagebox.showinfo(
                        APP_NAME,
                        "Não existem alterações novas.\n\n"
                        f"GitHub:\n{self.remote_url or 'remote não configurado'}"
                    )
                )
                return

            message = f"Commit {hoje()}"
            self.log(f'[3/4] git commit -m "{message}"')
            code, _ = self.run_git(["commit", "-m", message])
            if code != 0:
                raise RuntimeError("O commit falhou.")

            self.log(f"[4/4] git push origin {branch}")
            code, _ = self.run_git(["push", "origin", branch])

            if code != 0:
                self.set_status("⚠ Commit criado, mas o push falhou.")
                self.root.after(
                    0,
                    lambda: messagebox.showwarning(
                        APP_NAME,
                        "O commit foi criado, mas o push falhou.\n\n"
                        "Se o GitHub não estiver conectado, clique em '🔐 Entrar no GitHub'."
                    )
                )
                return

            self.show_remote(self.remote_url)
            self.log("")
            self.log("✓ Arquivos adicionados")
            self.log("✓ Commit criado")
            self.log("✓ Push enviado para o GitHub")
            self.log("✓ AUTO COMMIT CONCLUÍDO!")
            self.set_status("✓ Concluído.")

            self.root.after(
                0,
                lambda: messagebox.showinfo(
                    APP_NAME,
                    "Auto Commit concluído!\n\n"
                    f"Branch: {branch}\n"
                    f"GitHub: {self.remote_url or 'remote não configurado'}"
                )
            )

        except Exception as e:
            self.log(f"❌ ERRO: {e}")
            self.set_status("❌ Erro.")
            self.root.after(0, lambda: messagebox.showerror(APP_NAME, str(e)))
        finally:
            self.root.after(0, self._unlock_after_commit)

    def _unlock_after_commit(self):
        self.running = False


def main():
    root = tk.Tk()
    GitPoltergeist(root)
    root.mainloop()


if __name__ == "__main__":
    main()

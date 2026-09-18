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

# Compatibilidade com PyInstaller --windowed/--noconsole.
if os.name == "nt":
    if sys.stdout is None:
        sys.stdout = open(os.devnull, "w")
    if sys.stderr is None:
        sys.stderr = open(os.devnull, "w")

APP_NAME = "Git Poltergeist v2.0"
DEFAULT_PROJECT = r"C:\Users\ALUNO\Rômulo Delalíbera Júnior\desenvolvedor_python_qua.544.003"
CONFIG_DIR = Path(os.environ.get("APPDATA", str(Path.home()))) / "GitPoltergeist"
CONFIG_FILE = CONFIG_DIR / "config.json"

# Opções de mensagem de commit. A opção "Programado" continua sendo a padrão
# para preservar o comportamento que você já tinha programado.
COMMIT_OPTIONS = [
    ("programado", "Commit programado", "Commit {date}"),
    ("feat", "feat — nova funcionalidade", "feat: atualização {date}"),
    ("fix", "fix — correção de bug", "fix: correções {date}"),
    ("docs", "docs — documentação", "docs: documentação {date}"),
    ("style", "style — formatação/estilo", "style: ajustes de estilo {date}"),
    ("refactor", "refactor — refatoração", "refactor: melhorias {date}"),
    ("test", "test — testes", "test: ajustes de testes {date}"),
    ("chore", "chore — manutenção", "chore: manutenção {date}"),
    ("perf", "perf — desempenho", "perf: melhorias de desempenho {date}"),
    ("build", "build — build/dependências", "build: atualização {date}"),
    ("ci", "ci — integração contínua", "ci: ajustes {date}"),
    ("revert", "revert — reversão", "revert: reversão {date}"),
]
DEFAULT_COMMIT_TYPE = "programado"


def hoje():
    return date.today().strftime("%d/%m/%Y")


def load_config():
    try:
        if CONFIG_FILE.exists():
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
    except Exception:
        pass
    return {}


def load_project_folder():
    data = load_config()
    folder = str(data.get("project_folder", "")).strip()
    if folder and os.path.isdir(folder):
        return folder
    if os.path.isdir(DEFAULT_PROJECT):
        return DEFAULT_PROJECT
    return ""


def load_commit_type():
    value = str(load_config().get("commit_type", DEFAULT_COMMIT_TYPE))
    valid = {key for key, _, _ in COMMIT_OPTIONS}
    return value if value in valid else DEFAULT_COMMIT_TYPE


def save_settings(folder=None, commit_type=None, github_account=None):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    data = load_config()
    if folder is not None:
        data["project_folder"] = folder
    if commit_type is not None:
        data["commit_type"] = commit_type
    if github_account is not None:
        data["github_account"] = github_account
    CONFIG_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def hidden_process_kwargs():
    """Executa Git/GCM sem criar janela de CMD no Windows."""
    kwargs = {"creationflags": getattr(subprocess, "CREATE_NO_WINDOW", 0)}
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
        self.root.geometry("980x680")
        self.root.minsize(820, 560)

        self.folder = load_project_folder()
        self.commit_type = load_commit_type()
        self.remote_url = ""
        self.github_account = str(load_config().get("github_account", "")).strip()
        self.github_connected = False
        self.running = False
        self._github_accounts = []

        self.build()
        self.root.after(250, self.startup_check)

    def build(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Title.TLabel", font=("Segoe UI", 25, "bold"))
        style.configure("Subtitle.TLabel", font=("Segoe UI", 10))
        style.configure("Status.TLabel", font=("Segoe UI", 9))

        main = ttk.Frame(self.root, padding=18)
        main.pack(fill="both", expand=True)

        ttk.Label(main, text="Git Poltergeist", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            main,
            text="Auto Commit • execução manual • GitHub",
            style="Subtitle.TLabel"
        ).pack(anchor="w", pady=(0, 12))

        info = ttk.LabelFrame(main, text="Projeto salvo", padding=10)
        info.pack(fill="x", pady=(0, 10))

        # Grid evita o problema visual de texto cortado/sobreposto quando a janela muda de tamanho.
        info.columnconfigure(0, weight=1)
        info.columnconfigure(1, weight=0)
        info.columnconfigure(2, weight=0)
        info.columnconfigure(3, weight=0)
        info.columnconfigure(4, weight=0)

        self.folder_label = ttk.Label(
            info,
            text=self.folder or "Nenhuma pasta configurada",
            font=("Segoe UI", 9),
            anchor="w"
        )
        self.folder_label.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        self.github_box = ttk.Frame(info)
        self.github_box.grid(row=0, column=1, sticky="e")

        self.github_button = ttk.Button(
            self.github_box,
            text="Entrar no GitHub",
            command=self.github_button_action,
            width=23
        )
        self.github_button.pack(side="left")

        self.github_status = ttk.Label(
            self.github_box,
            text=" • verificando...",
            style="Status.TLabel"
        )
        self.github_status.pack(side="left", padx=(4, 0))

        ttk.Button(
            info, text="Mudar pasta", command=self.change_folder, width=15
        ).grid(row=0, column=2, padx=(8, 0))

        ttk.Button(
            info, text="Executar Commit", command=self.start_commit, width=17
        ).grid(row=0, column=3, padx=(8, 0))

        ttk.Button(
            info, text="⚙ Configurações", command=self.open_settings, width=18
        ).grid(row=0, column=4, padx=(8, 0))

        self.github_menu = tk.Menu(self.root, tearoff=False)
        self.github_menu.add_command(label="Trocar conta", command=self.github_switch_account)
        self.github_menu.add_command(label="Deslogar", command=self.github_logout)

        commit_info = ttk.Frame(main)
        commit_info.pack(fill="x", pady=(0, 8))
        self.commit_label = ttk.Label(commit_info, text="", style="Status.TLabel")
        self.commit_label.pack(side="left")
        self.update_commit_label()

        self.console = tk.Text(
            main,
            font=("Consolas", 10),
            wrap="word",
            state="disabled",
            padx=10,
            pady=8
        )
        self.console.pack(fill="both", expand=True)

        bottom = ttk.Frame(main)
        bottom.pack(fill="x", pady=(10, 0))
        bottom.columnconfigure(0, weight=1)

        self.status = ttk.Label(
            bottom,
            text="Pronto. Clique em Executar Commit.",
            style="Status.TLabel"
        )
        self.status.grid(row=0, column=0, sticky="w")

        self.link = ttk.Label(
            bottom,
            text="",
            cursor="hand2",
            font=("Segoe UI", 9, "underline")
        )
        self.link.grid(row=0, column=1, sticky="e")
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

    def update_commit_label(self):
        for key, label, _ in COMMIT_OPTIONS:
            if key == self.commit_type:
                self.commit_label.configure(text=f"Mensagem selecionada: {label}")
                return

    def startup_check(self):
        if not self.folder:
            self.log("Nenhuma pasta configurada.")
            self.log("Escolha a pasta uma única vez. Ela ficará salva.")
            self.set_status("Selecione a pasta.")
            self.change_folder()
        else:
            self.log("Pasta salva carregada.")
            self.set_status("Iniciando verificação do GitHub...")

        threading.Thread(target=self.startup_auth_then_commit, daemon=True).start()

    def startup_auth_then_commit(self):
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
            save_settings(folder=folder)
            self.folder_label.configure(text=folder)
            self.log("")
            self.log(f"Pasta salva: {folder}")
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

    def github_button_action(self):
        if self.github_connected:
            x = self.github_button.winfo_rootx()
            y = self.github_button.winfo_rooty() + self.github_button.winfo_height()
            self.github_menu.post(x, y)
        else:
            self.github_login()

    def github_login(self):
        if self.running:
            self.log("Aguarde o Auto Commit terminar antes de iniciar o login.")
            return
        threading.Thread(target=self._github_login_worker, daemon=True).start()

    def get_github_accounts(self):
        """Retorna contas GitHub conhecidas pelo Git Credential Manager."""
        try:
            p = subprocess.run(
                ["git", "credential-manager", "github", "list"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=10,
                **hidden_process_kwargs()
            )
            output = ((p.stdout or "") + "\n" + (p.stderr or "")).strip()
            if p.returncode != 0:
                return []
            bad = (
                "no account", "no accounts", "not logged", "not found",
                "nenhuma conta", "nenhuma autenticação"
            )
            accounts = []
            for line in output.splitlines():
                value = line.strip()
                if not value or any(item in value.lower() for item in bad):
                    continue
                if value not in accounts:
                    accounts.append(value)
            return accounts
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
            return []

    def check_github_auth(self):
        accounts = self.get_github_accounts()
        self._github_accounts = accounts

        # Se o usuário já escolheu uma conta, mantém essa conta quando possível.
        account = self.github_account if self.github_account in accounts else (accounts[0] if accounts else "")
        self.github_account = account
        self.github_connected = bool(account)

        self.root.after(0, self.update_github_ui)
        if account:
            save_settings(github_account=account)
            self.log(f"GitHub: conectado ({account})")
        else:
            self.log("GitHub: nenhuma conta autenticada encontrada.")

    def update_github_ui(self):
        if self.github_connected:
            self.github_button.configure(text=f"GitHub: {self.github_account}")
            self.github_status.configure(text=" • conectado")
            self.github_menu.entryconfigure(0, state="normal")
            self.github_menu.entryconfigure(1, state="normal")
        else:
            self.github_button.configure(text="Entrar no GitHub")
            self.github_status.configure(text=" • não conectado")
            self.github_menu.entryconfigure(0, state="normal")
            self.github_menu.entryconfigure(1, state="disabled")

    def github_switch_account(self):
        if self.running:
            self.log("Aguarde o Auto Commit terminar antes de trocar a conta.")
            return
        self.open_account_selector(relogin=True)

    def open_account_selector(self, relogin=False):
        accounts = self.get_github_accounts()
        if not accounts:
            self.github_login()
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Contas do GitHub")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)

        ttk.Label(dialog, text="Selecione a conta do GitHub:", font=("Segoe UI", 11, "bold")).pack(
            anchor="w", padx=18, pady=(18, 10)
        )
        selected = tk.StringVar(value=self.github_account or accounts[0])
        frame = ttk.Frame(dialog, padding=(18, 0, 18, 10))
        frame.pack(fill="both", expand=True)
        for account in accounts:
            ttk.Radiobutton(frame, text=account, value=account, variable=selected).pack(anchor="w", pady=3)

        buttons = ttk.Frame(dialog, padding=18)
        buttons.pack(fill="x")

        def choose():
            self.github_account = selected.get()
            self.github_connected = True
            save_settings(github_account=self.github_account)
            self.apply_github_account_to_repo(self.github_account)
            self.update_github_ui()
            self.set_status(f"GitHub selecionado: {self.github_account}")
            dialog.destroy()

        ttk.Button(buttons, text="Cancelar", command=dialog.destroy).pack(side="right")
        ttk.Button(buttons, text="Usar esta conta", command=choose).pack(side="right", padx=(0, 8))

        if relogin:
            ttk.Button(buttons, text="Adicionar outra conta", command=lambda: [dialog.destroy(), self.github_login()]).pack(side="left")

        dialog.protocol("WM_DELETE_WINDOW", dialog.destroy)
        self.root.wait_window(dialog)

    def github_logout(self, relogin=False):
        if self.running:
            self.log("Aguarde o Auto Commit terminar antes de deslogar.")
            return
        threading.Thread(target=self._github_logout_worker, args=(relogin,), daemon=True).start()

    def _github_logout_worker(self, relogin=False):
        try:
            if not self.git_available():
                raise RuntimeError("Git não encontrado.")
            account = self.github_account
            if not account:
                raise RuntimeError("Nenhuma conta do GitHub está selecionada.")

            # Nas versões atuais do GCM, logout exige o nome da conta.
            logout = subprocess.run(
                ["git", "credential-manager", "github", "logout", account],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=30,
                **hidden_process_kwargs()
            )
            output = ((logout.stdout or "") + "\n" + (logout.stderr or "")).strip()
            if logout.returncode != 0:
                raise RuntimeError(output or "Não foi possível deslogar do GitHub.")

            self.github_account = ""
            self.github_connected = False
            save_settings(github_account="")
            self.root.after(0, self.update_github_ui)
            self.set_status("GitHub deslogado.")
            self.log(f"GitHub: conta desconectada ({account}).")

            if relogin:
                self.root.after(150, self.github_login)
        except Exception as e:
            self.log(f"Logout GitHub: {e}")
            self.root.after(0, lambda: messagebox.showerror(APP_NAME, str(e)))

    def _github_login_worker(self):
        try:
            if not self.git_available():
                raise RuntimeError("Git não encontrado. Instale o Git para Windows e tente novamente.")

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
                    "O Git Credential Manager não está disponível.\n\n" +
                    (detail or "Instale/reinstale o Git para Windows.")
                )

            before = set(self.get_github_accounts())
            self.set_status("Aguardando login no GitHub...")
            self.log("")
            self.log("Abrindo login do GitHub no navegador...")
            self.log("Faça login e autorize o Git Credential Manager.")

            # --browser é suportado pelo GCM atual e evita depender de prompts no console.
            login = subprocess.run(
                ["git", "credential-manager", "github", "login", "--browser"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=300,
                **hidden_process_kwargs()
            )
            output = ((login.stdout or "") + "\n" + (login.stderr or "")).strip()
            if output:
                self.log(output)
            if login.returncode != 0:
                raise RuntimeError(
                    "O login do GitHub não foi concluído." +
                    (f"\n\n{output}" if output else "")
                )

            accounts = self.get_github_accounts()
            new_accounts = [a for a in accounts if a not in before]
            account = new_accounts[0] if new_accounts else (accounts[0] if accounts else "")
            if not account:
                raise RuntimeError("O login terminou, mas o Git Credential Manager não encontrou a conta.")

            self.github_account = account
            self.github_connected = True
            self._github_accounts = accounts
            save_settings(github_account=account)
            self.apply_github_account_to_repo(account)
            self.root.after(0, self.update_github_ui)
            self.set_status("GitHub conectado. Pronto para usar.")
            self.log(f"GitHub: login concluído como {account}.")
            self.root.after(0, lambda: messagebox.showinfo(
                APP_NAME,
                f"GitHub conectado com sucesso!\n\nConta: {account}\n\nAgora você pode executar o commit."
            ))
        except subprocess.TimeoutExpired:
            self.log("Login GitHub: tempo limite excedido.")
            self.set_status("Login não concluído.")
            self.root.after(0, lambda: messagebox.showerror(APP_NAME, "O login demorou demais e foi encerrado."))
        except Exception as e:
            self.log(f"Login GitHub: {e}")
            self.set_status("Login não concluído.")
            self.root.after(0, lambda: messagebox.showerror(APP_NAME, str(e)))

    def apply_github_account_to_repo(self, account):
        if not self.folder or not account or not os.path.isdir(self.folder):
            return
        try:
            subprocess.run(
                ["git", "config", "credential.https://github.com.username", account],
                cwd=self.folder,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=10,
                **hidden_process_kwargs()
            )
        except Exception:
            pass

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
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
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
            self.root.after(0, lambda: self.link.configure(text="Link do GitHub não configurado"))
            return
        self.remote_url = url
        self.root.after(0, lambda: self.link.configure(text=url))
        self.log(f"GitHub: {url}")

    def open_remote(self):
        if self.remote_url:
            webbrowser.open(self.remote_url)

    def build_commit_message(self):
        for key, _, template in COMMIT_OPTIONS:
            if key == self.commit_type:
                return template.format(date=hoje())
        return f"Commit {hoje()}"

    def open_settings(self):
        if self.running:
            messagebox.showinfo(APP_NAME, "Aguarde o commit terminar para alterar as configurações.")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Configurações")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.geometry("520x600")
        dialog.minsize(480, 520)

        ttk.Label(dialog, text="Configurações do Auto Commit", font=("Segoe UI", 16, "bold")).pack(
            anchor="w", padx=20, pady=(18, 4)
        )
        ttk.Label(
            dialog,
            text="Marque uma opção para definir como o próximo commit será criado.",
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=20, pady=(0, 12))

        box = ttk.LabelFrame(dialog, text="Tipo de commit", padding=12)
        box.pack(fill="both", expand=True, padx=20, pady=(0, 12))

        selected = tk.StringVar(value=self.commit_type)

        # Checkbuttons com comportamento de seleção única: visualmente você marca/desmarca,
        # mas apenas uma opção pode ficar ativa por vez para não gerar commits ambíguos.
        def select_type(value):
            selected.set(value)

        for key, label, _ in COMMIT_OPTIONS:
            ttk.Checkbutton(
                box,
                text=label,
                variable=selected,
                onvalue=key,
                offvalue=key + "__off",
                command=lambda: None
            ).pack(anchor="w", pady=3)

        ttk.Label(
            box,
            text="A primeira opção é a que você já programou e fica pré-selecionada.",
            font=("Segoe UI", 9, "italic")
        ).pack(anchor="w", pady=(10, 0))

        history_box = ttk.LabelFrame(dialog, text="Histórico de commits", padding=10)
        history_box.pack(fill="x", padx=20, pady=(0, 12))
        ttk.Button(history_box, text="Ver commits existentes", command=self.show_commit_history).pack(side="left")
        ttk.Label(history_box, text="Consulta os commits reais do repositório selecionado.").pack(side="left", padx=10)

        buttons = ttk.Frame(dialog, padding=20)
        buttons.pack(fill="x")

        def save_and_close():
            value = selected.get()
            valid = {key for key, _, _ in COMMIT_OPTIONS}
            if value not in valid:
                value = DEFAULT_COMMIT_TYPE
            self.commit_type = value
            save_settings(commit_type=value)
            self.update_commit_label()
            self.set_status("Configurações salvas.")
            dialog.destroy()

        ttk.Button(buttons, text="Cancelar", command=dialog.destroy).pack(side="right")
        ttk.Button(buttons, text="Salvar", command=save_and_close).pack(side="right", padx=(0, 8))
        dialog.protocol("WM_DELETE_WINDOW", dialog.destroy)

    def show_commit_history(self):
        if not self.folder or not os.path.isdir(self.folder):
            messagebox.showwarning(APP_NAME, "Selecione uma pasta de projeto primeiro.")
            return
        code, output = self.run_git(["log", "--oneline", "--decorate", "--date=short", "-n", "100"])
        if code != 0:
            messagebox.showerror(APP_NAME, "Não foi possível ler o histórico de commits.")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Commits existentes")
        dialog.transient(self.root)
        dialog.geometry("780x500")

        ttk.Label(dialog, text="Histórico real do repositório", font=("Segoe UI", 14, "bold")).pack(
            anchor="w", padx=16, pady=(16, 8)
        )
        ttk.Label(
            dialog,
            text="Aqui ficam os commits que já existem. O Auto Commit cria um novo commit; ele não altera commits antigos.",
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=16, pady=(0, 8))

        text = tk.Text(dialog, font=("Consolas", 10), wrap="none")
        text.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        text.insert("1.0", output or "Nenhum commit encontrado.")
        text.configure(state="disabled")

    def commit(self):
        try:
            self.log("=" * 70)
            self.log("GIT POLTERGEIST v2.0")
            self.log("=" * 70)
            self.log(f"Pasta: {self.folder}")

            if not os.path.isdir(self.folder):
                raise RuntimeError("A pasta salva não existe mais.")
            if not self.git_available():
                raise RuntimeError("Git não encontrado. Instale o Git para Windows e tente novamente.")

            self.log("Verificando login do GitHub...")
            self.check_github_auth()

            self.log("Buscando link do GitHub...")
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
            self.log(f"Branch: {branch}")

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
                self.log("Nenhuma alteração nova para commit.")
                self.show_remote(self.remote_url)
                self.set_status("Tudo já está atualizado.")
                self.root.after(0, lambda: messagebox.showinfo(
                    APP_NAME,
                    "Não existem alterações novas.\n\n" +
                    f"GitHub: {self.remote_url or 'remote não configurado'}"
                ))
                return

            message = self.build_commit_message()
            self.log(f'[3/4] git commit -m "{message}"')
            code, _ = self.run_git(["commit", "-m", message])
            if code != 0:
                raise RuntimeError("O commit falhou.")

            self.log(f"[4/4] git push origin {branch}")
            code, _ = self.run_git(["push", "origin", branch])
            if code != 0:
                self.set_status("Commit criado, mas o push falhou.")
                self.root.after(0, lambda: messagebox.showwarning(
                    APP_NAME,
                    "O commit foi criado, mas o push falhou.\n\n"
                    "Verifique o login do GitHub e tente novamente."
                ))
                return

            self.show_remote(self.remote_url)
            self.log("")
            self.log("Arquivos adicionados")
            self.log(f"Commit criado: {message}")
            self.log("Push enviado para o GitHub")
            self.log("AUTO COMMIT CONCLUÍDO!")
            self.set_status("Concluído.")
            self.root.after(0, lambda: messagebox.showinfo(
                APP_NAME,
                "Auto Commit concluído!\n\n" +
                f"Commit: {message}\n" +
                f"Branch: {branch}\n" +
                f"GitHub: {self.remote_url or 'remote não configurado'}"
            ))
        except Exception as e:
            self.log(f"ERRO: {e}")
            self.set_status("Erro.")
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

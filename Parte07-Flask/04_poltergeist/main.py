import os
import subprocess
import threading
import tkinter as tk
from datetime import date
from tkinter import filedialog, messagebox, ttk

APP_NAME = "Git Poltergeist v2.0"


def hoje():
    return date.today().strftime("%d/%m/%Y")


class GitPoltergeist:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("900x700")
        self.root.minsize(760, 600)

        self.pasta = tk.StringVar()
        self.mensagem = tk.StringVar(value=f"Commit {hoje()}")
        self.branch = tk.StringVar(value="main")
        self.status = tk.StringVar(value="Pronto.")

        self.build()

    def build(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        base = ttk.Frame(self.root, padding=20)
        base.pack(fill="both", expand=True)

        ttk.Label(base, text="👻 Git Poltergeist",
                  font=("Segoe UI", 26, "bold")).pack(anchor="w")
        ttk.Label(base, text="v2.0 • Auto Commit para GitHub",
                  font=("Segoe UI", 11)).pack(anchor="w", pady=(0, 18))

        project = ttk.LabelFrame(base, text="Projeto", padding=14)
        project.pack(fill="x", pady=(0, 12))

        ttk.Label(project, text="Pasta principal:").grid(
            row=0, column=0, sticky="w")
        ttk.Entry(project, textvariable=self.pasta).grid(
            row=1, column=0, sticky="ew", pady=(6, 0))
        ttk.Button(project, text="📁 Selecionar",
                   command=self.selecionar).grid(
            row=1, column=1, padx=(10, 0), pady=(6, 0))
        project.columnconfigure(0, weight=1)

        options = ttk.LabelFrame(base, text="Commit", padding=14)
        options.pack(fill="x", pady=(0, 12))

        ttk.Label(options, text="Mensagem:").grid(
            row=0, column=0, sticky="w")
        ttk.Entry(options, textvariable=self.mensagem).grid(
            row=0, column=1, sticky="ew", padx=10)

        ttk.Label(options, text="Branch:").grid(
            row=1, column=0, sticky="w", pady=(10, 0))
        ttk.Entry(options, textvariable=self.branch).grid(
            row=1, column=1, sticky="ew", padx=10, pady=(10, 0))
        options.columnconfigure(1, weight=1)

        actions = ttk.Frame(base)
        actions.pack(fill="x", pady=(0, 12))

        self.btn = ttk.Button(actions, text="🚀 AUTO COMMIT",
                              command=self.start_commit)
        self.btn.pack(side="left")

        ttk.Button(actions, text="🔎 Verificar",
                   command=self.start_status).pack(side="left", padx=8)
        ttk.Button(actions, text="🧹 Limpar",
                   command=self.clear).pack(side="right")

        console_frame = ttk.LabelFrame(base, text="Console", padding=8)
        console_frame.pack(fill="both", expand=True)

        self.console = tk.Text(console_frame, font=("Consolas", 10),
                               wrap="word", state="disabled")
        self.console.pack(side="left", fill="both", expand=True)

        scroll = ttk.Scrollbar(console_frame, orient="vertical",
                               command=self.console.yview)
        scroll.pack(side="right", fill="y")
        self.console.configure(yscrollcommand=scroll.set)

        ttk.Label(base, textvariable=self.status,
                  relief="sunken", anchor="w").pack(fill="x", pady=(12, 0))

    def log(self, text):
        self.root.after(0, self._log, text)

    def _log(self, text):
        self.console.configure(state="normal")
        self.console.insert("end", text + "\n")
        self.console.see("end")
        self.console.configure(state="disabled")

    def status_msg(self, text):
        self.root.after(0, lambda: self.status.set(text))

    def selecionar(self):
        folder = filedialog.askdirectory(title="Escolha a pasta principal do projeto")
        if folder:
            self.pasta.set(folder)
            self.log(f"📁 Pasta: {folder}")

    def clear(self):
        self.console.configure(state="normal")
        self.console.delete("1.0", "end")
        self.console.configure(state="disabled")

    def git_ok(self):
        try:
            subprocess.run(["git", "--version"], capture_output=True,
                           check=True, text=True)
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False

    def run_git(self, args, cwd):
        p = subprocess.run(["git"] + args, cwd=cwd,
                           capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        out = (p.stdout or "") + (p.stderr or "")
        if out.strip():
            self.log(out.strip())
        return p.returncode

    def start_status(self):
        threading.Thread(target=self.status_check, daemon=True).start()

    def status_check(self):
        folder = self.pasta.get().strip()
        if not folder or not os.path.isdir(folder):
            messagebox.showwarning(APP_NAME, "Selecione uma pasta válida.")
            return
        if not self.git_ok():
            messagebox.showerror(APP_NAME, "Git não encontrado. Instale o Git.")
            return

        self.log("=" * 64)
        self.log("VERIFICAÇÃO")
        self.log("=" * 64)
        code = self.run_git(["rev-parse", "--is-inside-work-tree"], folder)
        if code != 0:
            self.log("⚠ Esta pasta ainda não é um repositório Git.")
            self.status_msg("Não é um repositório Git.")
            return
        self.log("✓ Repositório encontrado.")
        self.log("STATUS:")
        self.run_git(["status", "--short"], folder)
        self.log("REMOTE:")
        self.run_git(["remote", "-v"], folder)
        self.status_msg("✓ Verificação concluída.")

    def start_commit(self):
        folder = self.pasta.get().strip()
        msg = self.mensagem.get().strip()
        branch = self.branch.get().strip()

        if not folder or not os.path.isdir(folder):
            messagebox.showwarning(APP_NAME, "Selecione uma pasta válida.")
            return
        if not msg:
            messagebox.showwarning(APP_NAME, "Digite uma mensagem de commit.")
            return
        if not branch:
            messagebox.showwarning(APP_NAME, "Informe a branch.")
            return

        self.btn.configure(state="disabled")
        threading.Thread(target=self.commit,
                         args=(folder, msg, branch), daemon=True).start()

    def commit(self, folder, msg, branch):
        try:
            self.status_msg("Executando Auto Commit...")
            self.log("=" * 64)
            self.log("👻 GIT POLTERGEIST v2.0")
            self.log("=" * 64)

            if not self.git_ok():
                raise RuntimeError("Git não encontrado no PATH.")

            check = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                cwd=folder, capture_output=True, text=True
            )

            if check.returncode != 0:
                self.log("⚠ Repositório não encontrado. Executando git init...")
                if self.run_git(["init"], folder) != 0:
                    raise RuntimeError("Não foi possível executar git init.")

            self.log("[1/4] git add .")
            if self.run_git(["add", "."], folder) != 0:
                raise RuntimeError("git add . falhou.")

            self.log("[2/4] verificando alterações...")
            diff = subprocess.run(["git", "diff", "--cached", "--quiet"],
                                  cwd=folder)
            if diff.returncode == 0:
                self.log("⚠ Nenhuma alteração nova.")
                self.status_msg("Nada para fazer commit.")
                messagebox.showinfo(APP_NAME, "Não existem alterações novas.")
                return

            self.log("[3/4] git commit")
            if self.run_git(["commit", "-m", msg], folder) != 0:
                raise RuntimeError("O commit falhou. Veja o console.")

            self.log(f"[4/4] git push origin {branch}")
            if self.run_git(["push", "origin", branch], folder) != 0:
                self.status_msg("⚠ Commit criado, mas o push falhou.")
                messagebox.showwarning(
                    APP_NAME,
                    "O commit foi criado localmente, mas o push falhou.\n\n"
                    "Verifique o remote, a branch e a autenticação do GitHub."
                )
                return

            self.log("✓ Arquivos adicionados")
            self.log("✓ Commit criado")
            self.log("✓ Push enviado para o GitHub")
            self.log("✓ AUTO COMMIT CONCLUÍDO!")
            self.status_msg("✓ Enviado para o GitHub.")
            messagebox.showinfo(APP_NAME, "Auto Commit concluído com sucesso!")

        except Exception as e:
            self.log(f"❌ ERRO: {e}")
            self.status_msg("❌ Erro.")
            messagebox.showerror(APP_NAME, str(e))
        finally:
            self.root.after(0, lambda: self.btn.configure(state="normal"))


def main():
    root = tk.Tk()
    GitPoltergeist(root)
    root.mainloop()


if __name__ == "__main__":
    main()

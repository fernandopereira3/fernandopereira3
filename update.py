import datetime
import subprocess
import sys


# Cores simples para o terminal
class Style:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def run(cmd, description):
    print(f"{Style.CYAN}>> {description}...{Style.RESET}")
    try:
        # check=True faz o script parar se o comando falhar (ex: erro de lint)
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"{Style.RED}Erro em: {description}{Style.RESET}")
        if e.stderr:
            print(e.stderr.decode())
        sys.exit(1)


def main():
    try:
        # 1. Verifica se é um repositório git
        if (
            subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"], capture_output=True
            ).returncode
            != 0
        ):
            print(f"{Style.RED}Erro: Você não está em um repositório Git!{Style.RESET}")
            return

        date = datetime.datetime.now().strftime("%d-%m-%y %H:%M")

        # 2. Qualidade de Código (Opcional - tenta rodar se o ruff estiver instalado)
        try:
            run(["ruff", "format", "."], "Formatando código")
            run(["ruff", "check", "--fix", "."], "Checando erros")
        except FileNotFoundError:
            print(
                f"{Style.CYAN}Nota: Ruff não encontrado, pulando linting.{Style.RESET}"
            )

        # 3. Informações do Commit
        subprocess.run(["clear"])
        current_branch = (
            subprocess.check_output(["git", "branch", "--show-current"])
            .strip()
            .decode()
        )

        print(f"{Style.BOLD}Repositório atual:{Style.RESET} {current_branch}")
        commit = input(f"{Style.GREEN}Detalhes do commit: {Style.RESET}").strip()

        if not commit:
            print(f"{Style.RED}Cancelado: Mensagem de commit vazia.{Style.RESET}")
            return

        # 4. Git Flow
        run(["git", "add", "."], "Adicionando arquivos")
        run(["git", "commit", "-m", f"{commit} / {date}"], "Realizando commit")

        push_confirm = input(
            f"{Style.GREEN}Deseja executar o comando 'git push' para a branch {Style.RED}{current_branch}{Style.BOLD}? (s/n): "
        )
        if push_confirm.lower() == "s":
            run(["git", "push", "origin", current_branch], "Enviando para o servidor")
            print(f"{Style.GREEN}✔ Processo finalizado com sucesso!{Style.RESET}")
        else:
            print(f"{Style.CYAN}Commit feito localmente. Push ignorado.{Style.RESET}")

    except KeyboardInterrupt:
        print(f"\n{Style.RED}Operação cancelada pelo usuário.{Style.RESET}")
        sys.exit(0)


if __name__ == "__main__":
    main()

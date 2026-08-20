import os, sys, json, argparse, re
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

VERSION = "GHOST-SecretsScanner v1.0-PRO"
BANNER = """
[bold cyan] ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗     ███████╗███████╗ ██████╗██████╗ ███████╗███████╗[/bold cyan]
[bold cyan]██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝     ██╔════╝██╔════╝██╔════╝██╔══██╗██╔════╝██╔════╝[/bold cyan]
[bold white]██║  ███╗███████║██║   ██║███████╗   ██║        ███████╗█████╗  ██║     ██████╔╝█████╗  ███████╗[/bold white]
[bold white]██║   ██║██╔══██║██║   ██║╚════██║   ██║        ╚════██║██╔══╝  ██║     ██╔══██╗██╔══╝  ╚════██║[/bold white]
[bold blue]╚██████╔╝██║  ██║╚██████╔╝███████║   ██║   ██╗  ███████║███████╗╚██████╗██║  ██║███████╗███████║[/bold blue]
[bold blue] ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚══════╝╚══════╝  ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝[/bold blue]
[bold yellow]     GHOST-SecretsScanner: High-Performance Hardcoded Secrets & API Key Detection[/bold yellow]
"""

console = Console()

def main():
    parser = argparse.ArgumentParser(description="GHOST-SecretsScanner")
    parser.add_argument("--path", default=".", help="Directory to scan for hardcoded secrets")
    args = parser.parse_args()
    
    console.print(Panel(BANNER, border_style="cyan", expand=False))
    console.print(f"[+] Scanning path '{args.path}' for hardcoded API keys, tokens, and private keys...")
    
    patterns = {
        "AWS Access Key": r"AKIA[0-9A-Z]{16}",
        "Generic API Key": r"api[_-]?key['\" ]*[:=]['\" ][0-9a-zA-Z]{16,45}",
        "Private Key": r"-----BEGIN (RSA|PRIVATE) KEY-----"
    }
    
    findings = []
    for root, dirs, files in os.walk(args.path):
        if ".git" in dirs:
            dirs.remove(".git")
        for file in files:
            if file.endswith(('.py', '.json', '.env', '.yml', '.yaml', '.sh', '.js')):
                fpath = os.path.join(root, file)
                try:
                    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        for p_name, p_regex in patterns.items():
                            if re.search(p_regex, content, re.IGNORECASE):
                                findings.append((fpath, p_name))
                except:
                    pass

    table = Table(title=f"Secrets Hygiene Report: {args.path}", border_style="red")
    table.add_column("File Path", style="cyan")
    table.add_column("Secret Type", style="yellow")
    table.add_column("Status", style="red")
    
    if findings:
        for fpath, stype in findings:
            table.add_row(fpath, stype, "EXPOSED")
    else:
        table.add_row("No exposed patterns matched", "Clean", "SECURE")
        
    console.print(table)
    console.print("\n[bold green][+] Secrets scan completed successfully.[/bold green]")

if __name__ == "__main__":
    main()

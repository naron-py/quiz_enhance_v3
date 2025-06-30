from rich.console import Console

# Create console
console = Console()

# Print test red messages
print("Normal text")
console.print("Standard rich print")
console.print("[bold red]Question not found in database.[/bold red]")
console.print("[bold red]Question matched, but choice not found.[/bold red]")

# Test using style method
print("Using style method:")
print(f"{console.style('Question not found in database.', 'red bold')}")
print(f"{console.style('Question matched, but choice not found.', 'red bold')}") 
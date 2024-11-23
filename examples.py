from pyquant import QuantumSimulator
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.tree import Tree
from datetime import datetime
import numpy as np

console = Console()

def demonstrate_bell_pair():
    """
    Demonstrates creation and measurement of a Bell pair
    """
    console.print("[bold cyan]Creating Bell Pair...[/bold cyan]")
    
    sim = QuantumSimulator(2)
    sim.create_bell_pair()
    sim.measure_all()
    results = sim.run(shots=1000)
    
    # Display results
    console.print("\n[bold green]Bell Pair Results:[/bold green]")
    
    # Create histogram
    hist = "\n"
    for state, count in sorted(results.items()):
        percentage = (count / 1000) * 100
        bars = "█" * int(percentage / 2)
        hist += f"|{state}⟩ {bars} {percentage:5.1f}% ({count})\n"
    
    console.print(Panel(hist, title="Measurement Distribution", border_style="blue"))
    
    # Display quantum circuit
    circuit = """
    Bell Pair Circuit:
    q₀: ──[H]──[●]──
              │
    q₁: ─────[X]──
    """
    console.print(Panel(circuit, title="Quantum Circuit", border_style="green"))
    
    # Statistics
    stats_table = Table(title="Statistical Analysis")
    stats_table.add_column("Metric", style="cyan")
    stats_table.add_column("Value", style="magenta")
    
    stats_table.add_row("Total Measurements", str(sum(results.values())))
    stats_table.add_row("Unique States", str(len(results)))
    stats_table.add_row("Fidelity", f"{(results.get('00', 0) + results.get('11', 0))/1000:.3f}")
    
    console.print(stats_table)
    return results

def demonstrate_teleportation():
    """
    Demonstrates quantum teleportation protocol
    """
    console.print("\n[bold cyan]Performing Quantum Teleportation...[/bold cyan]")
    
    sim = QuantumSimulator(3)
    state_to_teleport = [1, 0.5]
    sim.quantum_teleportation(state_to_teleport)
    results = sim.run(shots=1000)
    
    # Display results
    console.print("\n[bold green]Teleportation Results:[/bold green]")
    
    # Create histogram
    hist = "\n"
    for state, count in sorted(results.items()):
        percentage = (count / 1000) * 100
        bars = "█" * int(percentage / 2)
        hist += f"|{state}⟩ {bars} {percentage:5.1f}% ({count})\n"
    
    console.print(Panel(hist, title="Measurement Distribution", border_style="blue"))
    
    # Display quantum circuit
    circuit = """
    Teleportation Circuit:
    q₀: ──[X]──[H]──[M]────
    q₁: ──[H]──[●]──[M]────
              │
    q₂: ─────[X]─────────
    """
    console.print(Panel(circuit, title="Quantum Circuit", border_style="green"))
    
    # Statistics
    stats_table = Table(title="Statistical Analysis")
    stats_table.add_column("Metric", style="cyan")
    stats_table.add_column("Value", style="magenta")
    
    stats_table.add_row("Total Measurements", str(sum(results.values())))
    stats_table.add_row("Unique States", str(len(results)))
    max_prob = max(results.values()) / 1000
    stats_table.add_row("Max State Probability", f"{max_prob:.3f}")
    
    console.print(stats_table)
    return results

def run_all_demos():
    """
    Runs all demonstration examples
    """
    console.clear()
    console.print(
        Panel.fit(
            "[bold magenta]Quantum Computing Simulator Demonstrations",
            border_style="bold green"
        )
    )
    
    # Print timestamp
    console.print(
        f"\n[bold blue]Running demonstrations at: [/bold blue]"
        f"[yellow]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/yellow]\n"
    )
    
    # Run demonstrations
    bell_results = demonstrate_bell_pair()
    teleport_results = demonstrate_teleportation()
    
    # Final summary
    console.print("\n[bold yellow]Overall Summary[/bold yellow]")
    summary = Table(show_header=True)
    summary.add_column("Experiment", style="cyan")
    summary.add_column("Outcome", style="green")
    summary.add_column("Quality", style="yellow")
    
    # Calculate quality metrics
    bell_quality = (bell_results.get('00', 0) + bell_results.get('11', 0))/1000
    teleport_quality = max(teleport_results.values()) / 1000
    
    summary.add_row(
        "Bell Pair",
        f"{len(bell_results)} states",
        f"{bell_quality:.3f} fidelity"
    )
    summary.add_row(
        "Teleportation",
        f"{len(teleport_results)} states",
        f"{teleport_quality:.3f} probability"
    )
    
    console.print(summary)
    
    return {
        'bell_pair': bell_results,
        'teleportation': teleport_results
    }

if __name__ == "__main__":
    run_all_demos()
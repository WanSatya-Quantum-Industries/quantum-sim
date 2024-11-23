from transformers import AutoTokenizer
from pyquant import QuantumSimulator
import numpy as np
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
import torch
from typing import List, Dict, Tuple
from rich.panel import Panel
from dotenv import load_dotenv
import os
import huggingface_hub
from datetime import datetime

console = Console()

# Load environment variables
load_dotenv()

def log_proses(message: str, error: bool = False):
    """Helper untuk logging proses"""
    style = "red" if error else "green"
    timestamp = datetime.now().strftime("%H:%M:%S")
    console.print(f"[{style}][{timestamp}] {message}[/{style}]")

class QuantumTokenProcessor:
    def __init__(self, model_name: str = "mistralai/Mixtral-8x7B-v0.1", n_qubits: int = 4):
        """
        Inisialisasi Quantum Token Processor dengan autentikasi HuggingFace
        
        Args:
            model_name: Nama model untuk tokenizer
            n_qubits: Jumlah qubit yang digunakan
        """
        self.hf_token = os.getenv("HUGGINGFACE_TOKEN")
        if not self.hf_token:
            raise ValueError("HUGGINGFACE_TOKEN tidak ditemukan dalam variabel lingkungan")

        try:
            # Login ke HuggingFace
            huggingface_hub.login(token=self.hf_token)
            log_proses("Berhasil autentikasi dengan HuggingFace")

            # Inisialisasi tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                token=self.hf_token,
                trust_remote_code=True
            )
            log_proses(f"Berhasil memuat tokenizer untuk {model_name}")
        except Exception as e:
            log_proses(f"Error saat inisialisasi tokenizer: {str(e)}", error=True)
            raise

        self.n_qubits = n_qubits
        self.quantum_sim = QuantumSimulator(n_qubits)
        
        # Inisialisasi skema encoding
        self.initialize_quantum_schemes()
        
    def initialize_quantum_schemes(self):
        """
        Inisialisasi berbagai skema encoding kuantum
        """
        self.encoding_schemes = {
            'amplitude': self._amplitude_encoding,
            'phase': self._phase_encoding,
            'hybrid': self._hybrid_encoding
        }
        
    def _amplitude_encoding(self, token_id: int) -> None:
        """
        Mengkodekan informasi token dalam amplitudo keadaan kuantum
        """
        normalized_value = (token_id % 2**self.n_qubits) / (2**self.n_qubits)
        angle = normalized_value * np.pi
        
        self.quantum_sim.circuit.ry(angle, 0)
        
        for i in range(self.n_qubits - 1):
            self.quantum_sim.apply_cnot(i, i + 1)
            
    def _phase_encoding(self, token_id: int) -> None:
        """
        Mengkodekan informasi token dalam fase kuantum
        """
        for i in range(self.n_qubits):
            self.quantum_sim.circuit.h(i)
            
        normalized_phase = (token_id % 2**self.n_qubits) / (2**self.n_qubits) * 2 * np.pi
        self.quantum_sim.circuit.rz(normalized_phase, 0)
        
        for i in range(self.n_qubits - 1):
            self.quantum_sim.apply_cnot(i, i + 1)
            
    def _hybrid_encoding(self, token_id: int) -> None:
        """
        Menggunakan encoding amplitudo dan fase
        """
        amplitude_part = token_id % 2**(self.n_qubits-1)
        phase_part = token_id // 2**(self.n_qubits-1)
        
        self._amplitude_encoding(amplitude_part)
        self._phase_encoding(phase_part)
        
    def process_token(self, token_id: int, scheme: str = 'hybrid') -> Dict[str, float]:
        """
        Memproses satu token melalui sirkuit kuantum
        
        Args:
            token_id: ID token yang akan diproses
            scheme: Skema encoding yang digunakan ('amplitude', 'phase', atau 'hybrid')
        """
        self.quantum_sim = QuantumSimulator(self.n_qubits)
        
        encoding_func = self.encoding_schemes.get(scheme, self._hybrid_encoding)
        encoding_func(token_id)
        
        self.quantum_sim.measure_all()
        results = self.quantum_sim.run(shots=1000)
        
        prob_dist = {k: v/1000 for k, v in results.items()}
        return prob_dist
    
    def process_text(self, text: str, scheme: str = 'hybrid') -> List[Dict[str, float]]:
        """
        Memproses seluruh teks melalui sirkuit kuantum
        
        Args:
            text: Teks input yang akan diproses
            scheme: Skema encoding yang digunakan
        """
        tokens = self.tokenizer.encode(text)
        
        quantum_embeddings = []
        with Progress() as progress:
            task = progress.add_task("[cyan]Memproses token...", total=len(tokens))
            
            for token in tokens:
                quantum_embeddings.append(self.process_token(token, scheme))
                progress.advance(task)
                
        return quantum_embeddings
    
    def visualize_processing(self, text: str) -> None:
        """
        Visualisasi pemrosesan token kuantum
        
        Args:
            text: Teks input untuk divisualisasi
        """
        schemes = ['amplitude', 'phase', 'hybrid']
        results = {}
        
        console.print("\n[bold green]Memproses teks dengan berbagai skema kuantum...[/bold green]")
        
        tokens = self.tokenizer.encode(text)
        token_strings = self.tokenizer.convert_ids_to_tokens(tokens)
        
        for scheme in schemes:
            results[scheme] = self.process_text(text, scheme)
            
        # Tabel perbandingan
        table = Table(title="Hasil Pemrosesan Token Kuantum")
        table.add_column("Token", style="cyan")
        for scheme in schemes:
            scheme_name = {
                'amplitude': 'Amplitudo',
                'phase': 'Fase',
                'hybrid': 'Hibrid'
            }[scheme]
            table.add_column(scheme_name, style="magenta")
            
        for i, token in enumerate(token_strings):
            row = [token]
            for scheme in schemes:
                prob_dist = results[scheme][i]
                max_state = max(prob_dist.items(), key=lambda x: x[1])
                row.append(f"|{max_state[0]}⟩ ({max_state[1]:.2f})")
            table.add_row(*row)
            
        console.print(table)
        
        # Contoh sirkuit
        circuit = """
        Contoh Sirkuit Kuantum (Encoding Hibrid):
        q₀: ──[H]──[Ry]──[●]─────
                         │
        q₁: ──[H]────────[X]──[●]
                              │
        q₂: ──[H]─────────────[X]
        """
        console.print(Panel(circuit, title="Sirkuit Kuantum", border_style="blue"))
        
        # Hitung nilai untuk format string
        start_cnot = self.n_qubits + 1
        end_cnot = (self.n_qubits * 2)
        
        # Informasi encoding
        encoding_info = f"""
        [bold]Skema Encoding:[/bold]
        
        1. [cyan]Amplitude Encoding[/cyan]:
           - Mengkodekan informasi token ke dalam amplitudo keadaan kuantum
           - Menggunakan rotasi Ry berdasarkan nilai token
           - Amplitudo menentukan probabilitas pengukuran
           - Cocok untuk merepresentasikan besaran nilai token
        
        2. [cyan]Phase Encoding[/cyan]:
           - Mengkodekan informasi dalam fase kuantum
           - Menggunakan rotasi Rz untuk manipulasi fase
           - Fase memengaruhi interferensi antar qubit
           - Berguna untuk merepresentasikan pola dalam token
        
        3. [cyan]Hybrid Encoding[/cyan]:
           - Menggabungkan encoding amplitudo dan fase
           - Memberikan representasi kuantum yang lebih kaya
           - Memanfaatkan kedua sifat kuantum sekaligus
           - Optimal untuk token dengan informasi kompleks
        
        [bold]Statistik Pemrosesan:[/bold]
        - Jumlah token yang diproses: {len(tokens)}
        - Kedalaman sirkuit kuantum: {self.n_qubits * 2 + 1}
           • Layer 1-{self.n_qubits}: Gate Hadamard (H)
           • Layer {start_cnot}-{end_cnot}: Gate CNOT
           • Layer {self.n_qubits * 2 + 1}: Gate rotasi final
        - Pengukuran per token: 1000
           • Setiap pengukuran menghasilkan state basis
           • Distribusi menunjukkan properti kuantum token
           • 1000 shot memberikan statistik yang reliable
        
        [bold]Catatan Penting:[/bold]
        - Semakin dalam sirkuit, semakin kaya representasi
        - Jumlah pengukuran memengaruhi akurasi distribusi
        - Entanglement antar qubit menciptakan korelasi kuantum
        """
        
        console.print(Panel(encoding_info, title="Detail Pemrosesan", border_style="yellow"))
        
        # Statistik tambahan
        stats_info = f"""
        [bold]Statistik Pemrosesan:[/bold]
        - Token yang diproses: {len(token_strings)}
        - Total pengukuran: {len(token_strings) * 1000}
        - Kedalaman sirkuit: {self.n_qubits * 2 + 1} layer
        - Status: [green]Selesai[/green]
        """
        console.print(Panel(stats_info, title="Ringkasan Statistik", border_style="cyan"))

def main():
    if "HUGGINGFACE_TOKEN" not in os.environ:
        console.print(Panel(
            "[red]Error: HUGGINGFACE_TOKEN tidak ditemukan dalam variabel lingkungan[/red]\n\n"
            "Silakan buat file .env dengan token HuggingFace Anda:\n"
            "HUGGINGFACE_TOKEN=your_token_here\n\n"
            "Anda bisa mendapatkan token dari:\n"
            "https://huggingface.co/settings/tokens",
            title="Error Autentikasi",
            border_style="red"
        ))
        return

    try:
        processor = QuantumTokenProcessor()
        
        text = "Quantum computing is fascinating!"
        
        console.print(Panel.fit(
            "[bold magenta]Demo Pemrosesan Token Kuantum[/bold magenta]\n"
            f"Memproses teks: '{text}'",
            border_style="green"
        ))
        
        processor.visualize_processing(text)
        
    except Exception as e:
        console.print(Panel(
            f"[red]Terjadi kesalahan:[/red]\n{str(e)}\n\n"
            "[yellow]Saran penyelesaian:[/yellow]\n"
            "1. Pastikan token HuggingFace valid\n"
            "2. Periksa koneksi internet\n"
            "3. Coba restart program",
            title="Error",
            border_style="red"
        ))
        raise

if __name__ == "__main__":
    main()
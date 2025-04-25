"""
Arquivo principal para iniciar o aplicativo Schedule 1 Calculator.
"""

import os
import sys
from gui import Schedule1Calculator

def main():
    """Função principal para iniciar o aplicativo."""
    app = Schedule1Calculator()
    app.mainloop()

if __name__ == "__main__":
    main()
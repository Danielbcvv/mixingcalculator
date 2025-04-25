from cx_Freeze import setup, Executable

# Configuração do executável
executables = [
    Executable(
        script="main.py",  # Arquivo principal
        icon="icon.ico",  # Ícone do executável
        base="Win32GUI"  # Esta linha impede que o cmd seja aberto
    )
]

# Configuração do pacote
setup(
    name="Mixing Calculator",
    version="1.0",
    description="The Mixing Calculator is a straightforward program designed to calculate the best mixtures for the game Schedule 1. Optimize your gameplay with ease!",
    options={
        "build_exe": {
            "include_files": [
                "images/",  # Inclui a pasta images
                "icon.ico"  # Inclui o arquivo de ícone
            ],
            "packages": [],  # Adicione bibliotecas externas aqui, se necessário
            "include_msvcr": True,  # Inclui bibliotecas do Microsoft Visual C++
            "optimize": 2  # Otimiza o bytecode do Python
        }
    },
    executables=executables
)
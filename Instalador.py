import subprocess
import os

def install_pyqt5():
    powershell_code = r'''
$package = "PyQt5"
$packageInstalled = Get-Module -ListAvailable | Where-Object { $_.Name -eq $package }

if (-not $packageInstalled) {
    Write-Host "Instalando..."
    & pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org "G:\\Desenvolvimento Farmacotecnico Neo\\59. Softwares_Farmacotecnico\\Arquivos\\PyQt5-5.15.9-cp37-abi3-win_amd64.whl" db-sqlite3 pandas numpy unidecode
} else {
    Write-Host "Tudo já está instalado."
}
    '''

    # Salva o código PowerShell em um arquivo temporário
    ps_script_path = os.path.join(os.environ["TEMP"], "install_pyqt5.ps1")
    with open(ps_script_path, "w") as ps_file:
        ps_file.write(powershell_code)

    try:
        # Executa o arquivo PowerShell com powershell.exe
        subprocess.run(["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", ps_script_path], shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o PowerShell: {e}")
    else:
        print("Instalado com sucesso!")

if __name__ == "__main__":
    install_pyqt5()

$ErrorActionPreference = "Stop"

$projectPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectPath

Write-Host "Limpando artefatos antigos..."
if (Test-Path "allure-results") { Remove-Item "allure-results" -Recurse -Force }
if (Test-Path "allure-report") { Remove-Item "allure-report" -Recurse -Force }
if (Test-Path "img") { Remove-Item "img" -Recurse -Force }

New-Item -ItemType Directory -Force -Path "allure-results" | Out-Null
New-Item -ItemType Directory -Force -Path "allure-report" | Out-Null
New-Item -ItemType Directory -Force -Path "img" | Out-Null

Write-Host "Executando testes..."
pytest -v -s --alluredir=allure-results

Write-Host "Gerando relatório Allure..."
allure generate allure-results --clean -o allure-report

Write-Host "Abrindo o relatório..."
allure open allure-report

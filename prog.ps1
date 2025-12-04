Write-Host "=== Conversión masiva del proyecto a UTF-8 sin BOM ===" -ForegroundColor Cyan

# Extensiones permitidas
$extensions = @("*.html", "*.py", "*.txt", "*.json", "*.md", "*.css", "*.js")

# Carpeta raíz del proyecto (donde está este script)
$root = Get-Location

Write-Host "Carpeta del proyecto: $root" -ForegroundColor Yellow

# Función para guardar en UTF-8 sin BOM
function Save-AsUtf8($path, $content) {
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($path, $content, $utf8NoBom)
}

# Buscar archivos
$files = foreach ($ext in $extensions) {
    Get-ChildItem -Recurse -Filter $ext
}

foreach ($file in $files) {

    Write-Host "Procesando: $($file.FullName)" -ForegroundColor Yellow

    try {
        # Leer contenido bruto
        $raw = Get-Content $file.FullName -Raw -ErrorAction Stop
    }
    catch {
        Write-Host "  ERROR: No se pudo leer este archivo." -ForegroundColor Red
        continue
    }

    # --- FIX para HTML (agrega charset si falta) ---
    if ($file.Extension -eq ".html") {
        if ($raw -notmatch "<meta.*charset") {
            Write-Host "  -> Agregando <meta charset='UTF-8'>"
            $raw = $raw -replace "<head>", "<head>`n    <meta charset=""UTF-8"">"
        }
    }

    try {
        Save-AsUtf8 $file.FullName $raw
        Write-Host "  -> Guardado en UTF-8 sin BOM" -ForegroundColor Green
    }
    catch {
        Write-Host "  ERROR: No se pudo guardar el archivo." -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "   TODO EL PROYECTO ESTÁ AHORA EN UTF-8 CORRECTO"
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "Reinicia Django y presiona CTRL+F5 en el navegador."

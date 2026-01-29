Write-Host "=== CSS Bundle Diagnostic ===" -ForegroundColor Cyan
$cssFile = Get-ChildItem -Path "dist/assets" -Filter "*.css" | Select-Object -First 1
if ($cssFile) {
    Write-Host "CSS File: $($cssFile.Name)" -ForegroundColor Green
    $content = Get-Content $cssFile.FullName -Raw
    
    $classes = ".campus-selection-container", ".campus-selection-title", ".floor-detail", ".students-grid"
    foreach ($class in $classes) {
        if ($content -like "*$class*") {
            Write-Host " $class FOUND" -ForegroundColor Green
        } else {
            Write-Host "X $class NOT FOUND" -ForegroundColor Red
        }
    }
    
    $vars = "--text-primary", "--text-secondary", "--glass-bg"
    foreach ($var in $vars) {
        if ($content -like "*$var*") {
            Write-Host " $var FOUND" -ForegroundColor Green
        } else {
            Write-Host "X $var NOT FOUND" -ForegroundColor Red
        }
    }
} else {
    Write-Host "ERROR: No CSS file found. Run npm run build first!" -ForegroundColor Red
}

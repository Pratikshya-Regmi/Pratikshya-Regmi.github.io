$ErrorActionPreference = 'Stop'
$siteRoot = $PSScriptRoot
$repositoryRoot = Split-Path -Parent $siteRoot
$portableNode = Join-Path $repositoryRoot '.tools/node-v22.23.2-win-x64'
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    if (-not (Test-Path -LiteralPath (Join-Path $portableNode 'node.exe'))) {
        throw 'Install Node.js 22.12 or newer, then run npm ci and npm run build inside astro-site.'
    }
    $env:PATH = $portableNode + ';' + $env:PATH
}
$env:ASTRO_TELEMETRY_DISABLED = '1'
if (-not (Test-Path -LiteralPath (Join-Path $siteRoot 'dist/index.html'))) {
    throw 'Build the site first: cd astro-site; npm ci; npm run build'
}
& npm.cmd --prefix $siteRoot run preview -- --host 127.0.0.1

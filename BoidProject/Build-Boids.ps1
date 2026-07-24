[CmdletBinding()]
param(
    [ValidateSet("Portable", "Installer")]
    [string]$Type = "Portable",
    [string]$JdkHome
)

$ErrorActionPreference = "Stop"

$projectRoot = $PSScriptRoot
$repoRoot = Split-Path -Parent $projectRoot
$workRoot = Join-Path $projectRoot "build\boids-package"
$classesDir = Join-Path $workRoot "classes"
$testClassesDir = Join-Path $workRoot "test-classes"
$inputDir = Join-Path $workRoot "input"
$jarPath = Join-Path $inputDir "Boids.jar"
$distDir = Join-Path $repoRoot "dist"
$appVersion = "1.1"
$windowsUpgradeUuid = "e2afd0e6-7e75-3473-b759-6c566b88397c"

function Find-JdkBin {
    if ($JdkHome) {
        $candidate = Join-Path $JdkHome "bin"
        if (Test-Path -LiteralPath (Join-Path $candidate "jpackage.exe")) {
            return $candidate
        }
        throw "JDK tools were not found under '$JdkHome\bin'."
    }

    $jpackageCommand = Get-Command "jpackage.exe" -ErrorAction SilentlyContinue
    if ($jpackageCommand) {
        return Split-Path -Parent $jpackageCommand.Source
    }

    $javaRoot = Join-Path $env:ProgramFiles "Java"
    if (Test-Path -LiteralPath $javaRoot) {
        $installedJdks = Get-ChildItem -LiteralPath $javaRoot -Directory |
            Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName "bin\jpackage.exe") } |
            Sort-Object Name -Descending

        if ($installedJdks) {
            return Join-Path $installedJdks[0].FullName "bin"
        }
    }

    throw "JDK 17 or newer was not found. Install a JDK or pass -JdkHome 'C:\path\to\jdk'."
}

function Find-WixBin {
    $candleCommand = Get-Command "candle.exe" -ErrorAction SilentlyContinue
    $lightCommand = Get-Command "light.exe" -ErrorAction SilentlyContinue
    if ($candleCommand -and $lightCommand) {
        return Split-Path -Parent $candleCommand.Source
    }

    $wixCommand = Get-Command "wix.exe" -ErrorAction SilentlyContinue
    if ($wixCommand) {
        return Split-Path -Parent $wixCommand.Source
    }

    $commonWixLocations = @(
        (Join-Path ${env:ProgramFiles(x86)} "WiX Toolset v3.11\bin"),
        (Join-Path ${env:ProgramFiles(x86)} "WiX Toolset v3.14\bin"),
        (Join-Path $env:ProgramFiles "WiX Toolset v4\bin"),
        (Join-Path $env:ProgramFiles "WiX Toolset v5\bin"),
        (Join-Path $env:ProgramFiles "WiX Toolset v6\bin"),
        (Join-Path $env:ProgramFiles "WiX Toolset v7\bin")
    )

    foreach ($candidate in $commonWixLocations) {
        $hasWix3 = (Test-Path -LiteralPath (Join-Path $candidate "candle.exe")) -and
            (Test-Path -LiteralPath (Join-Path $candidate "light.exe"))
        $hasModernWix = Test-Path -LiteralPath (Join-Path $candidate "wix.exe")

        if ($hasWix3 -or $hasModernWix) {
            return $candidate
        }
    }

    return $null
}

function Invoke-JdkTool {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Tool,
        [Parameter(Mandatory = $true)]
        [string[]]$Arguments
    )

    & $Tool @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "'$Tool' failed with exit code $LASTEXITCODE."
    }
}

$jdkBin = Find-JdkBin
$javac = Join-Path $jdkBin "javac.exe"
$java = Join-Path $jdkBin "java.exe"
$jar = Join-Path $jdkBin "jar.exe"
$jpackage = Join-Path $jdkBin "jpackage.exe"

foreach ($tool in @($javac, $java, $jar, $jpackage)) {
    if (-not (Test-Path -LiteralPath $tool)) {
        throw "Required JDK tool not found: $tool"
    }
}

if (Test-Path -LiteralPath $workRoot) {
    Remove-Item -LiteralPath $workRoot -Recurse -Force
}
New-Item -ItemType Directory -Path $classesDir, $testClassesDir, $inputDir, $distDir -Force | Out-Null

[string[]]$sources = Get-ChildItem `
    -Path (Join-Path $projectRoot "src\main\*.java"), (Join-Path $projectRoot "src\entity\*.java") |
    ForEach-Object FullName

if ($sources.Count -eq 0) {
    throw "No Java source files were found."
}

Write-Host "Compiling Boids with $javac"
Invoke-JdkTool -Tool $javac -Arguments (@("-Xlint:all", "-d", $classesDir) + $sources)

Write-Host "Running the simulation smoke test"
[string[]]$testSources = Get-ChildItem -Path (Join-Path $projectRoot "test\main\*.java") |
    ForEach-Object FullName
Invoke-JdkTool -Tool $javac -Arguments (
    @("-Xlint:all", "-d", $testClassesDir) + $sources + $testSources
)
Invoke-JdkTool -Tool $java -Arguments @("-cp", $testClassesDir, "main.BoidsSmokeTest")

Write-Host "Creating $jarPath"
Invoke-JdkTool -Tool $jar -Arguments @(
    "--create",
    "--file", $jarPath,
    "--main-class", "main.Main",
    "-C", $classesDir,
    "."
)

$commonPackageArguments = @(
    "--input", $inputDir,
    "--main-jar", "Boids.jar",
    "--main-class", "main.Main",
    "--name", "Boids",
    "--app-version", $appVersion,
    "--vendor", "Luippe",
    "--description", "Boids flocking simulation",
    "--dest", $distDir
)

if ($Type -eq "Installer") {
    $wixBin = Find-WixBin

    if (-not $wixBin) {
        throw "WiX is required for an installer build. Install WiX, reopen PowerShell, and run this command again."
    }

    Write-Host "Using WiX from $wixBin"
    $env:Path = $wixBin + [IO.Path]::PathSeparator + $env:Path

    $versionedInstaller = Join-Path $distDir "Boids-$appVersion.exe"
    $installer = Join-Path $distDir "Boids.exe"
    if (Test-Path -LiteralPath $versionedInstaller) {
        Remove-Item -LiteralPath $versionedInstaller -Force
    }

    Write-Host "Creating the Windows installer"
    Invoke-JdkTool -Tool $jpackage -Arguments (
        @("--type", "exe") +
        $commonPackageArguments +
        @(
            "--win-per-user-install",
            "--win-menu",
            "--win-shortcut",
            "--win-upgrade-uuid", $windowsUpgradeUuid
        )
    )

    if (-not (Test-Path -LiteralPath $versionedInstaller)) {
        throw "jpackage completed, but '$versionedInstaller' was not created."
    }

    try {
        if (Test-Path -LiteralPath $installer) {
            Remove-Item -LiteralPath $installer -Force -ErrorAction Stop
        }
        Move-Item -LiteralPath $versionedInstaller -Destination $installer -ErrorAction Stop
        Write-Host "Installer created: $installer"
    }
    catch {
        Write-Warning "The existing '$installer' is locked by another process."
        Write-Host "Versioned installer created instead: $versionedInstaller"
    }

    Write-Host "Run this installer once, then launch Boids from its desktop shortcut or Start menu entry."
}
else {
    $portableDir = Join-Path $distDir "Boids"
    $portableZip = Join-Path $distDir "Boids-Windows.zip"

    if (Test-Path -LiteralPath $portableDir) {
        Remove-Item -LiteralPath $portableDir -Recurse -Force
    }
    if (Test-Path -LiteralPath $portableZip) {
        Remove-Item -LiteralPath $portableZip -Force
    }

    Write-Host "Creating the portable Windows application"
    Invoke-JdkTool -Tool $jpackage -Arguments (
        @("--type", "app-image") + $commonPackageArguments
    )

    $launcher = Join-Path $portableDir "Boids.exe"
    if (-not (Test-Path -LiteralPath $launcher)) {
        throw "jpackage completed, but '$launcher' was not created."
    }

    Compress-Archive -Path (Join-Path $portableDir "*") -DestinationPath $portableZip
    Write-Host "Launcher created: $launcher"
    Write-Host "Portable archive created: $portableZip"
}

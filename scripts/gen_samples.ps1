$sampleDir = Join-Path (Get-Location).ProviderPath "ai-backend\static\samples"
New-Item -ItemType Directory -Path $sampleDir -Force | Out-Null

$sampleRate = 16000
$duration = 3
$amplitude = 16000

$presets = @{
    "gentle_female" = 260
    "mature_male" = 140
    "sweet_child" = 320
    "magnetic_male" = 110
    "intellectual_female" = 230
    "news_anchor" = 180
    "anime_boy" = 350
    "queen_female" = 200
}

foreach ($key in $presets.Keys) {
    $freq = $presets[$key]
    $path = Join-Path -Path $sampleDir -ChildPath "$key.wav"
    $numSamples = $sampleRate * $duration
    $dataSize = $numSamples * 2
    $fileSize = 36 + $dataSize

    $stream = [System.IO.MemoryStream]::new()
    $writer = [System.IO.BinaryWriter]::new($stream)

    $writer.Write([char[]]'RIFF')
    $writer.Write([int]$fileSize)
    $writer.Write([char[]]'WAVE')
    $writer.Write([char[]]'fmt ')
    $writer.Write([int]16)
    $writer.Write([int]1)
    $writer.Write([int]1)
    $writer.Write([int]$sampleRate)
    $writer.Write([int]($sampleRate * 2))
    $writer.Write([int]2)
    $writer.Write([int]16)
    $writer.Write([char[]]'data')
    $writer.Write([int]$dataSize)

    $omega = 2.0 * [Math]::PI * $freq / $sampleRate
    for ($i = 0; $i -lt $numSamples; $i++) {
        $val = [int]($amplitude * [Math]::Sin($omega * $i))
        $writer.Write([int16]$val)
    }

    $writer.Flush()
    [System.IO.File]::WriteAllBytes($path, $stream.ToArray())
    $writer.Dispose()
    $stream.Dispose()

    $size = (Get-Item $path).Length
    Write-Host ("$key.wav ({0}Hz, {1}KB)" -f $freq, [math]::Round($size/1KB, 1))
}

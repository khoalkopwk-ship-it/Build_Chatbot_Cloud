$faqApiBase = 'https://ts6153n8b5.execute-api.us-east-1.amazonaws.com'
$faqApiBase = $faqApiBase.TrimEnd('/')
$faqPayload = @{ question = 'Nhóm được sử dụng những Region nào?' } | ConvertTo-Json -Compress
Add-Type -AssemblyName System.Net.Http
$faqClient = [System.Net.Http.HttpClient]::new()
$faqClient.Timeout = [TimeSpan]::FromSeconds(20)
$faqContent = [System.Net.Http.StringContent]::new($faqPayload, [System.Text.Encoding]::UTF8, 'application/json')
try {
    $faqResponse = $faqClient.PostAsync("$faqApiBase/chat", $faqContent).GetAwaiter().GetResult()
    "HTTP $([int]$faqResponse.StatusCode)"
    $faqResponse.Content.ReadAsStringAsync().GetAwaiter().GetResult()
} finally {
    $faqContent.Dispose()
    $faqClient.Dispose()
}
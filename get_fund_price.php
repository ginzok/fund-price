<?php
// スプレッドシートからのfundcodeを受け取る
$fundcode = isset($_GET['fundcode']) ? $_GET['fundcode'] : '';

if (empty($fundcode)) {
    header("HTTP/1.1 400 Bad Request");
    echo json_encode(["error" => "fundcode is required"]);
    exit;
}

// MUFG APIのURL
$apiUrl = "https://developer.am.mufg.jp/fund_information_latest/fund_cd/" . $fundcode;

// ブラウザを模倣するためのヘッダー
$options = [
    "http" => [
        "method" => "GET",
        "header" => "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36\r\n" .
                    "Accept: application/json, text/javascript, */*; q=0.01\r\n" .
                    "Referer: https://202505121002v48733j5.conohawing.com/\r\n"
    ]
];

$context = stream_context_create($options);

// APIからデータを取得
$response = file_get_contents($apiUrl, false, $context);

// レスポンスヘッダーをJSONに設定
header("Content-Type: application/json; charset=utf-8");

// 受け取ったデータをそのまま出力する
echo $response;
?>
# Go HTTP/2 + TLS ローカルサンプル

HTTP/2 + TLS で動く最小のWebアプリです。

## 前提

- Go 1.22+
- `openssl`

## 1) 証明書を生成

```bash
chmod +x generate_local_certs.sh
./generate_local_certs.sh
```

## 2) サーバー起動

```bash
go run .
```

起動後: <https://localhost:8443>

## 3) HTTP/2 の確認

```bash
curl --http2 -k -I https://localhost:8443
```

`HTTP/2 200` が表示されればOKです。

## 補足

自己署名証明書を使っているため、ブラウザで警告が出ます。ローカル検証用途として想定しています。

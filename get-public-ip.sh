curl -fSs https://1.1.1.1/cdn-cgi/trace | awk -F= '/ip/ { print $2 }'

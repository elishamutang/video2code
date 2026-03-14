# Note to self
- If SSL certificates expire and fail to renew automatically, run the following docker command to renew the certs manually.

`docker compose run --rm certbot certonly --webroot --webroot-path=/var/www/certbot -d video2code.xyz -d www.video2code.xyz`

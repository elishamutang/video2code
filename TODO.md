# TO-DO LIST

1. ~~Add feature where picking a certain point in time will also move the slider of the video~~.
2. ~~For each code extract, allow the user to click on the timestamp to navigate to that point in time of the video (similar to above)~~.
3. ~~Code highlighting~~
4. ~~Rate limiting.~~
   - ~~Create a history by storing generated code extracts in local storage.~~
   - ~~Limit users from abusing API (maybe give 8 as the limit.)~~

# Note to self
- If SSL certificates expire and fail to renew automatically, run the following docker command to renew the certs manually.

`docker compose run --rm certbot certonly --webroot --webroot-path=/var/www/certbot -d video2code.xyz -d www.video2code.xyz`

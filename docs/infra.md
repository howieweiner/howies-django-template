# DigitalOcean Server Setup

The app is hosted on a DigitalOcean droplet. The droplet is provisioned using Ansible.
The Ansible playbook is located in the `infra` directory.

To pull code from Github, the IP address of the server needs to be in `~/.ssh/config` to allow port forwarding

```bash
Host XXX.XXX.XX.XX
  ForwardAgent yes
```

## Server provisioning

To provision a server for the first time, run the following command:

```bash
make ansible env=stage|prod playbook=server
```

You will be prompted for the vault password, which is in Bitwarden

## Database provisioning

Now, the database can be provisioned by running the following command:

```bash
make ansible env=stage|prod playbook=postgres
```

## Redis and Celery provisioning

Now, Redis can be provisioned by running the following command:

```bash
make ansible env=stage|prod playbook=redis
```

The Celery service cand also be provisioned by running the following command:

```bash
make ansible env=stage|prod playbook=celery
```

```bash
## Django App provisioning

The Django app can be provisioned by running the following command:

```bash
make ansible env=stage|prod playbook=django
```

The Ansible playbook does not currently create a Django superuser. This needs to be done manually
by ssh'ing onto the server and running the following command:

```bash
source /venv/bin/activate
DJANGO_SETTINGS_MODULE=config.settings.production make createsuperuser
```

## Gunicorn provisioning

Gunicorn can be provisioned by running the following command:

```bash
make ansible env=stage|prod playbook=gunicorn
```

## Nginx provisioning

Nginx can be provisioned by running the following command:

```bash
make ansible env=stage|prod playbook=nginx
make ansible env=stage|prod playbook=ssl
```

To add Basic Auth to the app, run the following command:

```bash
make ansible env=stage|prod playbook=nginx-auth
```

The nginx conf file for the domain located in `sites-available` needs updating as follows:

```bash
location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
        auth_basic "Private Property";
        auth_basic_user_file /etc/nginx/.htpasswd;
    }
```

Now restart the nginx service

```bash
sudo systemctl restart nginx
```

If changes are made to nginx, it can be necessary to recreate the SSL cert and restart the nginx service e.g.

```bash
sudo certbot --nginx -d {{ project_name }}.stagedbyhowie.co.uk
sudo systemctl restart nginx
```

It is also necessary to generate a self-signed cert for the dummy server used to catch bots
by executing the following command when logged onto the server:

```bash
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt
````

## Fail2ban provisioning

Fail2ban can be provisioned by running the following command:

```bash
make ansible env=stage|prod playbook=fail2ban
```

## Set up db backup cron job

Installation of a cronjob to run nightly db backups can by running the following command:

```bash
make ansible env=stage|prod playbook=cron_db_backup
```

## Ansible

The Ansible playbook uses Ansible Vault to encrypt sensitive variables. The vault password is stored in Bitwarden.
To use the vault password:

First login to Bitwarden and sync the vault:

```bash
bw login
export BW_SESSION=$(bw unlock --raw)
bw sync
```

Then from the root directory run the following command:

```bash
ansible-vault encrypt_string --vault-password-file infra/vault-pass.sh 'secret' --name 'key'
```

To create an encrypted file, run the following command:

```bash
ansible-vault create --vault-password-file infra/vault-pass.sh secred_creds.json
```

This will launch a text editor. Enter the secret content and save the file.

## References

- [Setting up Django, Postgres, Ngin, Unicorn](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04).
- [Nginx + SSL](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-22-04)
- [NGinx GZIP](https://www.digitalocean.com/community/tutorials/how-to-improve-website-performance-using-gzip-and-nginx-on-ubuntu-20-04)
- [Self signed Nginx cert](https://www.digitalocean.com/community/tutorials/how-to-create-a-self-signed-ssl-certificate-for-nginx-in-ubuntu-22-04)

To decrypt a vault variable:

```bash
echo 'encrypted string' | ansible-vault decrypt --vault-password-file infra/vault-pass.sh
```

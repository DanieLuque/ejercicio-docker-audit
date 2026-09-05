# Despliegue en EC2

## 1. DNS y Security Group

Crea estos registros DNS apuntando a la IP pública de la instancia:

- `fases1-5.duckdns.org`
- `kuma-fases1-5.duckdns.org`
- `dozzle-fases1-5.duckdns.org`

En el Security Group permite `80/tcp` y `443/tcp` desde Internet. Permite `22/tcp` únicamente desde tu IP. No abras `3001`, `8080` ni `3306`.

## 2. Preparar EC2

Ejecuta en la instancia Ubuntu:

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-plugin ufw git
sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"

sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow from TU_IP_PUBLICA to any port 22 proto tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

Cierra la sesión y vuelve a conectarte para que el grupo `docker` tenga efecto.

## 3. Primera instalación

Copia el proyecto en EC2 y crea el archivo de entorno. No subas este archivo a GitHub:

```bash
mkdir -p ~/ejercicio-docker-audit
cd ~/ejercicio-docker-audit
cp .env.example .env
nano .env
```

Cambia `DB_PASS` y `DB_ROOT_PASS` por contraseñas largas y únicas.

## 4. Emitir certificados por primera vez

La configuración HTTPS necesita certificados existentes. Para el primer arranque, guarda temporalmente la configuración final:

```bash
cd ~/ejercicio-docker-audit
mv nginx/conf.d/default.conf nginx/conf.d/default.https.conf.disabled
cat > nginx/conf.d/default.conf <<'NGINX'
server {
    listen 80;
    server_name fases1-5.duckdns.org kuma-fases1-5.duckdns.org dozzle-fases1-5.duckdns.org;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 200 "Certificados en proceso\n";
        add_header Content-Type text/plain;
    }
}
NGINX

docker compose up -d db api nginx
```

Solicita un único certificado SAN para los tres dominios:

```bash
docker compose run --rm --entrypoint certbot certbot certonly \
  --webroot \
  --webroot-path=/var/www/certbot \
  --email TU_EMAIL \
  --agree-tos \
  --no-eff-email \
    -d fases1-5.duckdns.org \
    -d kuma-fases1-5.duckdns.org \
    -d dozzle-fases1-5.duckdns.org
```

Activa la configuración HTTPS definitiva:

```bash
rm nginx/conf.d/default.conf
mv nginx/conf.d/default.https.conf.disabled nginx/conf.d/default.conf
docker compose exec -T nginx nginx -t
docker compose up -d
```

## 5. Comprobar servicios

```bash
docker compose ps
curl -f https://fases1-5.duckdns.org/health
curl -I https://kuma-fases1-5.duckdns.org
curl -I https://dozzle-fases1-5.duckdns.org
```

Los puertos internos permanecen así:

- API: `api:8080`
- Uptime Kuma: `kuma:3001`
- Dozzle: `dozzle:8080`

Solo Nginx publica `80` y `443`.

## 6. Renovación de certificados

Configura una tarea de renovación en EC2:

```bash
crontab -e
```

```cron
0 3 * * * cd /home/ubuntu/ejercicio-docker-audit && docker compose run --rm --entrypoint certbot certbot renew && docker compose exec -T nginx nginx -s reload
```

Ajusta `/home/ubuntu` si utilizas otro usuario.

## 7. Secrets de GitHub Actions

Configura en `Settings > Secrets and variables > Actions`:

- `DEPLOY_HOST`: IP o DNS público de EC2.
- `DEPLOY_USER`: usuario de EC2, por ejemplo `ubuntu`.
- `DEPLOY_SSH_KEY`: clave privada SSH completa.

El archivo `.env` y los certificados se crean solo en EC2. El workflow no los sobrescribe.

## 8. Despliegue continuo

Después de configurar los secrets, un push a `main` ejecuta:

1. Pytest.
2. Bandit.
3. Construcción de la imagen.
4. Trivy.
5. Copia del proyecto a EC2 por SSH.
6. `docker compose pull`, `build` y `up -d`.
7. Validación de Nginx y estado de los servicios.

Si falla una prueba de seguridad, el job de despliegue no se ejecuta.

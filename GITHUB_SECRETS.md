# GitHub Secrets requeridos para Fase 3

## Secrets de despliegue (solo necesarios en Fase 4)

Estos secrets se documentan aquí para que puedan configurarse cuando llegue la Fase 4. No se utilizan en la Fase 3 actualmente.

### Para Docker Hub (opcional en Fase 3, obligatorio en Fase 4)

| Secret | Descripción | Ejemplo |
|--------|-------------|---------|
| `DOCKERHUB_USERNAME` | Usuario de Docker Hub | `tu_usuario` |
| `DOCKERHUB_TOKEN` | Token de acceso de Docker Hub | `dckr_pat_xxx...` |

### Para despliegue en EC2 (Fase 4)

| Secret | Descripción | Ejemplo |
|--------|-------------|---------|
| `DEPLOY_SSH_KEY` | Clave privada SSH para acceso a EC2 | Contenido de `~/.ssh/ec2_key.pem` |
| `DEPLOY_HOST` | IP pública o DNS de la instancia EC2 | `ec2-18-123-45-67.compute-1.amazonaws.com` |
| `DEPLOY_USER` | Usuario SSH de la instancia | `ubuntu` o `ec2-user` |

## Cómo configurar los secrets

1. Ve a tu repositorio en GitHub.
2. Settings > Secrets and variables > Actions.
3. New repository secret.
4. Pega el nombre y el valor correspondiente.

No incluyas estos valores en archivos versionados.

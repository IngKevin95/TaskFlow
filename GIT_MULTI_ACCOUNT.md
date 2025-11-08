# 🔐 Configuración de Múltiples Cuentas Git

Este proyecto está configurado para permitirte usar múltiples cuentas de GitHub.

## 📋 Cuentas Disponibles

| Cuenta | Email | Usar para |
|--------|-------|----------|
| **IngKevin95** | kevin.f.o@hotmail.com | Commits personales |
| **LeadKevinDev2895** | kevin.orduz@trycore.com.co | Commits de trabajo |

## 🔧 Configuración Actual

```bash
# Para ver la configuración actual:
git config --list | grep user

# Para cambiar la cuenta antes de hacer commit:
git config user.name "IngKevin95"
git config user.email "kevin.f.o@hotmail.com"

# O para LeadKevinDev2895:
git config user.name "LeadKevinDev2895"
git config user.email "kevin.orduz@trycore.com.co"
```

## 🔑 Opción 1: Usar GitHub Desktop (Recomendado)

Si tienes GitHub Desktop instalado, es la forma más fácil:

1. **Abrir GitHub Desktop**
2. **File → Options → Accounts**
3. **Agregar ambas cuentas GitHub**
4. En cada repositorio, puedes cambiar de cuenta desde:
   - **Repository → Repository settings → Git Configuration**

## 🔑 Opción 2: Usar Autenticación SSH

Para usar SSH (sin contraseña en cada push):

### Paso 1: Generar claves SSH para cada cuenta

```bash
# Para IngKevin95
ssh-keygen -t ed25519 -C "kevin.f.o@hotmail.com" -f ~/.ssh/id_ed25519_ingkevin95

# Para LeadKevinDev2895
ssh-keygen -t ed25519 -C "kevin.orduz@trycore.com.co" -f ~/.ssh/id_ed25519_leadkevin
```

### Paso 2: Agregar claves a GitHub

1. Copiar contenido de `~/.ssh/id_ed25519_ingkevin95.pub`
2. Ir a GitHub → Settings → SSH and GPG keys → New SSH key
3. Pegar la clave
4. Repetir para la segunda cuenta

### Paso 3: Configurar SSH Config

Crear o editar `~/.ssh/config`:

```
# Cuenta IngKevin95
Host github.com-ingkevin95
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_ingkevin95

# Cuenta LeadKevinDev2895
Host github.com-leadkevin
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_leadkevin
```

### Paso 4: Cambiar remotes según la cuenta

```bash
# Para usar IngKevin95:
git remote set-url origin git@github.com-ingkevin95:IngKevin95/TaskFlow.git

# Para usar LeadKevinDev2895:
git remote set-url origin git@github.com-leadkevin:IngKevin95/TaskFlow.git
```

## 🔑 Opción 3: Usar Token de GitHub (Token Personal)

1. **Ir a GitHub → Settings → Developer settings → Personal access tokens**
2. **Crear token con permisos de repo**
3. **Usar como contraseña cuando git lo pida**

## ✅ Para Hacer Commit con tu Cuenta Actual

### Paso 1: Configurar usuario local (antes de hacer commit)

```bash
# Cambiar a IngKevin95
git config user.name "IngKevin95"
git config user.email "kevin.f.o@hotmail.com"

# Verificar
git config user.name
git config user.email
```

### Paso 2: Hacer commit

```bash
# Agregar cambios
git add .

# Commit
git commit -m "docs: actualizar README con funcionalidades completas"

# Push (aquí te pedirá credenciales si aún no las has guardado)
git push origin master
```

## 📝 Ejemplo Paso a Paso

```bash
# 1. Estar en la rama correcta
git branch

# 2. Ver cambios
git status

# 3. Configurar cuenta a usar
git config user.name "IngKevin95"
git config user.email "kevin.f.o@hotmail.com"

# 4. Agregar cambios
git add README.md API_REQUESTS.rest

# 5. Crear commit
git commit -m "docs: actualizar README y API_REQUESTS.rest

- Agregar descripción completa de todas las funcionalidades
- Documentar sistema RBAC con matriz de permisos
- Incluir guía de testing con API_REQUESTS.rest
- Documentar filtros avanzados de tareas
- Agregar ejemplos de endpoints completos
- Incluir modelos de base de datos
- Agregar instrucciones de despliegue"

# 6. Verificar commit
git log --oneline -1

# 7. Hacer push
git push origin master
```

## 🔒 Seguridad

- **Nunca guardes contraseñas en el código**
- **Usa SSH o tokens personales**
- **No compartas tokens en repositorios públicos**
- **Revisa los permisos de los tokens**

## 🆘 Troubleshooting

### ¿Olvidé cambiar la cuenta?

```bash
# Ver quién hizo el último commit
git log -1 --format="%aN <%aE>"

# Enmendar el commit anterior (cambiar autor)
git commit --amend --author="IngKevin95 <kevin.f.o@hotmail.com>"

# Si ya está pusheado, forzar actualización (cuidado):
git push origin master --force-with-lease
```

### ¿No puedo hacer push?

```bash
# Verificar configuración
git config user.name
git config user.email

# Verificar remote
git remote -v

# Si hay problemas de autenticación:
git config --global credential.helper store
# Esto te pedirá credenciales la próxima vez que hagas push
```

### ¿Cambiar cuenta global?

```bash
# Para cambiar la cuenta por defecto en tu máquina:
git config --global user.name "IngKevin95"
git config --global user.email "kevin.f.o@hotmail.com"

# Esto afectará todos los repos. Para cambiar solo en este repo:
git config --local user.name "IngKevin95"
git config --local user.email "kevin.f.o@hotmail.com"
```

## 📚 Recursos

- [Documentación GitHub - Multiple Accounts](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-multiple-accounts)
- [Git Documentation - Config](https://git-scm.com/book/en/v2/Git-Tools-Credential-Storage)
- [SSH y GitHub](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

---

**Última actualización:** Noviembre 2025

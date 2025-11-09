// Custom Swagger UI con validación automática de token
(function() {
    console.log('🔧 Script de validación de token cargado');
    
    // Función para mostrar notificaciones
    function showNotification(message, type) {
        // Remover notificación anterior
        const existing = document.querySelector('.token-validation-notification');
        if (existing) existing.remove();
        
        // Crear notificación
        const notification = document.createElement('div');
        notification.className = 'token-validation-notification token-' + type;
        notification.innerHTML = message;
        document.body.appendChild(notification);
        
        // Auto-remover después de 5 segundos
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }
    
    // Función para actualizar el estado de autenticación en el banner
    function updateAuthStatus(isAuthenticated, username, role) {
        const authStatus = document.getElementById('authStatus');
        if (authStatus) {
            if (isAuthenticated) {
                authStatus.innerHTML = '<span class="status-indicator status-logged-in">🟢&nbsp;Autenticado:&nbsp;<span class="username">' + username + '</span>&nbsp;(' + role + ')</span>';
            } else {
                authStatus.innerHTML = '<span class="status-indicator status-logged-out">🔴 No autenticado</span>';
            }
        }
    }
    
    // Función para cambiar el color del botón Authorize
    function updateAuthorizeButton(isValid) {
        // Buscar el botón de Authorize
        const authorizeBtn = document.querySelector('.btn.authorize');
        
        if (authorizeBtn) {
            // Remover clases previas
            authorizeBtn.classList.remove('token-valid', 'token-invalid');
            
            if (isValid === true) {
                authorizeBtn.classList.add('token-valid');
                authorizeBtn.querySelector('span')?.setAttribute('title', 'Token válido ✅');
                console.log('🟢 Botón Authorize marcado como válido');
            } else if (isValid === false) {
                authorizeBtn.classList.add('token-invalid');
                authorizeBtn.querySelector('span')?.setAttribute('title', 'Token inválido ❌');
                console.log('🔴 Botón Authorize marcado como inválido');
            }
        } else {
            console.log('⚠️ Botón Authorize no encontrado aún');
        }
    }
    
    // Función para validar el token
    async function validateToken(token) {
        console.log('🔍 Validando token...', token.substring(0, 30) + '...');
        showNotification('🔄 Validando token...', 'info');
        
        try {
            const response = await fetch('/api/auth/validate-token', {
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + token,
                    'Content-Type': 'application/json'
                }
            });
            
            console.log('📡 Respuesta recibida - Status:', response.status);
            
            if (response.ok) {
                const data = await response.json();
                console.log('✅ Token válido:', data);
                showNotification(
                    '✅ Token válido<br>Usuario: <strong>' + data.user.username + '</strong><br>Rol: <strong>' + data.user.role + '</strong>',
                    'success'
                );
                updateAuthorizeButton(true);
                updateAuthStatus(true, data.user.username, data.user.role);
                return true;
            } else if (response.status === 401) {
                try {
                    const error = await response.json();
                    console.log('❌ Token inválido (401):', error);
                    showNotification(
                        '❌ Token inválido<br>' + (error.detail || 'No autorizado'),
                        'error'
                    );
                } catch (parseError) {
                    console.log('❌ Token inválido (401) - Error al parsear respuesta');
                    showNotification(
                        '❌ Token inválido<br>No autorizado',
                        'error'
                    );
                }
                updateAuthorizeButton(false);
                updateAuthStatus(false);
                return false;
            } else if (response.status === 403) {
                console.log('❌ Token rechazado (403)');
                showNotification('❌ Acceso prohibido<br>Token no autorizado', 'error');
                updateAuthorizeButton(false);
                return false;
            } else {
                console.log('⚠️ Error inesperado:', response.status);
                showNotification('⚠️ Error al validar token<br>Código: ' + response.status, 'error');
                updateAuthorizeButton(false);
                return false;
            }
        } catch (error) {
            console.error('❌ Error de red o excepción:', error);
            showNotification('❌ Error de conexión<br>' + error.message, 'error');
            updateAuthorizeButton(false);
            return false;
        }
    }
    
    // Interceptar cuando se guarda la autorización
    function interceptAuthorization() {
        const originalSetItem = localStorage.setItem;
        
        localStorage.setItem = function(key, value) {
            console.log('💾 localStorage.setItem llamado:', key);
            
            // Llamar al método original
            originalSetItem.apply(this, arguments);
            
            // Detectar cuando se guarda autorización
            if (key && key.indexOf('authorized') !== -1) {
                console.log('� Clave de autorización detectada:', key);
                console.log('📦 Valor:', value.substring(0, 100) + '...');
                
                setTimeout(function() {
                    try {
                        const authData = JSON.parse(value);
                        console.log('📋 Datos parseados:', authData);
                        
                        // Buscar el token Bearer
                        if (authData && authData.BearerAuth) {
                            const token = authData.BearerAuth.value;
                            console.log('🎯 Token encontrado, longitud:', token ? token.length : 0);
                            
                            if (token && token.length > 20) {
                                console.log('✅ Token válido para validar, iniciando validación...');
                                validateToken(token);
                            } else {
                                console.log('⚠️ Token muy corto o vacío');
                                showNotification('⚠️ Token inválido<br>El token proporcionado es demasiado corto', 'error');
                            }
                        } else {
                            console.log('⚠️ No se encontró BearerAuth en los datos');
                        }
                    } catch (e) {
                        console.error('❌ Error al parsear autorización:', e);
                        showNotification('❌ Error al procesar token<br>' + e.message, 'error');
                    }
                }, 600);
            }
        };
        
        console.log('✅ Interceptor de autorización instalado correctamente');
    }
    
    // Inicializar cuando el DOM esté listo
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', interceptAuthorization);
    } else {
        interceptAuthorization();
    }
    
    // Observer para detectar cuando aparece el botón Authorize
    setTimeout(function() {
        const observer = new MutationObserver(function(mutations) {
            const authorizeBtn = document.querySelector('.btn.authorize');
            if (authorizeBtn && !authorizeBtn.dataset.observerAttached) {
                authorizeBtn.dataset.observerAttached = 'true';
                console.log('🔍 Botón Authorize detectado y registrado');
            }
            
            // Arreglar los campos del login
            fixLoginInputs();
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
        
        console.log('👀 Observer del botón Authorize activado');
    }, 1000);
    
    // Función para arreglar los inputs de username y password
    function fixLoginInputs() {
        // Buscar inputs con placeholder username y password
        const usernameInput = document.querySelector('input[placeholder="username"]');
        const passwordInput = document.querySelector('input[placeholder="password"]');
        
        if (usernameInput && !usernameInput.dataset.fixed) {
            // Remover el valor "string" por defecto
            if (usernameInput.value === 'string') {
                usernameInput.value = '';
            }
            usernameInput.dataset.fixed = 'true';
            console.log('✅ Campo username arreglado');
        }
        
        if (passwordInput && !passwordInput.dataset.fixed) {
            // Remover el valor "string" por defecto
            if (passwordInput.value === 'string') {
                passwordInput.value = '';
            }
            // Cambiar el tipo a password
            passwordInput.type = 'password';
            passwordInput.dataset.fixed = 'true';
            console.log('✅ Campo password arreglado y enmascarado');
        }
    }
    
    // Ejecutar la función periódicamente durante los primeros segundos
    let fixAttempts = 0;
    const fixInterval = setInterval(function() {
        fixLoginInputs();
        fixAttempts++;
        if (fixAttempts > 20) {
            clearInterval(fixInterval);
            console.log('🛑 Intentos de arreglar inputs finalizados');
        }
    }, 500);
})();

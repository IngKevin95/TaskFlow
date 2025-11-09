// Hook para autenticación

import { useState, useEffect } from "react";
import { User, AuthRequest, RegisterRequest } from "../types";
import authAPI from "../api/auth.api";
import { STORAGE_KEYS } from "../config/constants";

export const useAuth = () => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isInitialized, setIsInitialized] = useState(false);

  // Cargar token y usuario del localStorage al montar
  useEffect(() => {
    const initializeAuth = () => {
      const storedToken = localStorage.getItem(STORAGE_KEYS.TOKEN);
      const storedUser = localStorage.getItem(STORAGE_KEYS.USER);

      if (storedToken && storedUser) {
        try {
          setToken(storedToken);
          setUser(JSON.parse(storedUser));
          setIsAuthenticated(true);
        } catch (err) {
          console.error('Error al parsear usuario del localStorage:', err);
          localStorage.removeItem(STORAGE_KEYS.TOKEN);
          localStorage.removeItem(STORAGE_KEYS.USER);
        }
      }
      setIsInitialized(true);
    };

    initializeAuth();
  }, []);

  const register = async (data: RegisterRequest) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await authAPI.register(data);
      setToken(response.access_token);
      localStorage.setItem(STORAGE_KEYS.TOKEN, response.access_token);
      setIsAuthenticated(true);
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || "Error en el registro";
      setError(errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (credentials: AuthRequest) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await authAPI.login(credentials);
      const accessToken = response.access_token;
      
      // Guardar token primero
      setToken(accessToken);
      localStorage.setItem(STORAGE_KEYS.TOKEN, accessToken);
      
      // Obtener datos del usuario
      const currentUser = await authAPI.getCurrentUser();
      setUser(currentUser);
      localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(currentUser));
      
      // Establecer autenticado al final
      setIsAuthenticated(true);
      
      console.log('Login exitoso:', { user: currentUser, token: accessToken });
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || "Error en el login";
      setError(errorMessage);
      console.error('Error en login:', err);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    setIsAuthenticated(false);
    localStorage.removeItem(STORAGE_KEYS.TOKEN);
    localStorage.removeItem(STORAGE_KEYS.USER);
  };

  return {
    user,
    token,
    isLoading,
    error,
    isAuthenticated,
    isInitialized,
    register,
    login,
    logout,
  };
};

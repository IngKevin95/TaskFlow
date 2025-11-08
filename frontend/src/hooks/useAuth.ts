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

  // Cargar token y usuario del localStorage al montar
  useEffect(() => {
    const storedToken = localStorage.getItem(STORAGE_KEYS.TOKEN);
    const storedUser = localStorage.getItem(STORAGE_KEYS.USER);

    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(JSON.parse(storedUser));
      setIsAuthenticated(true);
    }
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
      setToken(response.access_token);
      localStorage.setItem(STORAGE_KEYS.TOKEN, response.access_token);
      
      // Obtener datos del usuario
      const currentUser = await authAPI.getCurrentUser();
      setUser(currentUser);
      localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(currentUser));
      setIsAuthenticated(true);
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || "Error en el login";
      setError(errorMessage);
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
    register,
    login,
    logout,
  };
};

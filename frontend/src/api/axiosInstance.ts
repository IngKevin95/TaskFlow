// Instancia de Axios configurada
// Maneja todas las solicitudes HTTP con autenticación

import axios, { AxiosInstance, AxiosRequestConfig } from "axios";
import { API_BASE_URL, API_TIMEOUT } from "../config/api.config";
import { STORAGE_KEYS } from "../config/constants";

class AxiosClient {
  private axiosInstance: AxiosInstance;

  constructor() {
    this.axiosInstance = axios.create({
      baseURL: API_BASE_URL,
      timeout: API_TIMEOUT,
      headers: {
        "Content-Type": "application/json",
      },
    });

    // Interceptor para agregar token a cada request
    this.axiosInstance.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem(STORAGE_KEYS.TOKEN);
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Interceptor para manejo de errores
    this.axiosInstance.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Token expirado o inválido
          localStorage.removeItem(STORAGE_KEYS.TOKEN);
          localStorage.removeItem(STORAGE_KEYS.USER);
          window.location.href = "/login";
        }
        return Promise.reject(error);
      }
    );
  }

  getInstance(): AxiosInstance {
    return this.axiosInstance;
  }
}

export default new AxiosClient().getInstance();

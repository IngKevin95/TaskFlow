// Servicio de API para autenticación

import axiosInstance from "./axiosInstance";
import { ENDPOINTS } from "../config/api.config";
import { AuthRequest, AuthResponse, RegisterRequest, User } from "../types";

class AuthAPI {
  async register(data: RegisterRequest): Promise<AuthResponse> {
    const response = await axiosInstance.post(ENDPOINTS.AUTH.REGISTER, data);
    return response.data;
  }

  async login(credentials: AuthRequest): Promise<AuthResponse> {
    // El backend espera application/x-www-form-urlencoded
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);
    
    const response = await axiosInstance.post(ENDPOINTS.AUTH.LOGIN, formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  }

  async getCurrentUser(): Promise<User> {
    const response = await axiosInstance.get(ENDPOINTS.AUTH.ME);
    return response.data;
  }
}

export default new AuthAPI();

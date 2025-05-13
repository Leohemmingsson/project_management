import { ref } from "vue";
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export function useAuth() {
  const accessToken = ref(null);
  const refreshToken = ref(null);
  const error = ref(null);

  const login = async (username, password) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/login`, {
        username,
        password,
      });
      accessToken.value = response.data.access_token;
      refreshToken.value = response.data.refresh_token;
      error.value = null;
      return true;
    } catch (err) {
      error.value = err.response?.data?.detail || "Login failed";
      return false;
    }
  };

  return {
    accessToken,
    refreshToken,
    error,
    login,
  };
}

import { ref } from "vue";
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_BACKEND_BASE_URL;

export function useAuth() {
  const accessToken = ref(localStorage.getItem("access_token"));
  const refreshToken = ref(localStorage.getItem("refresh_token"));
  const error = ref(null);

  const login = async (username, password) => {
    try {
      const params = new URLSearchParams();
      params.append("username", username);
      params.append("password", password);

      const response = await axios.post(`${API_BASE_URL}/login`, params, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });

      accessToken.value = response.data.access_token;
      refreshToken.value = response.data.refresh_token;

      // Save to localStorage
      localStorage.setItem("access_token", accessToken.value);
      localStorage.setItem("refresh_token", refreshToken.value);

      error.value = null;
      return true;
    } catch (err) {
      error.value = err.response?.data?.detail || "Login failed";
      return false;
    }
  };

  const logout = () => {
    // TODO
    // * Add a logout request (to remove refresh_token form backend)
    accessToken.value = null;
    refreshToken.value = null;
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
  };

  return {
    accessToken,
    refreshToken,
    error,
    login,
    logout,
  };
}

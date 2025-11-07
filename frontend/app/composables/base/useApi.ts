import type { User, Read, Access, Threshold } from "~/types/app";

const API_BASE_URL = "http://localhost:8000";

export const useApi = () => {
  // ============================================
  // GENERIC HTTP METHODS
  // ============================================

  const get = async <T = any>(path: string): Promise<T> => {
    try {
      const url = path.startsWith("http") ? path : `${API_BASE_URL}${path}`;
      const response = await fetch(url);
      if (!response.ok) {
        const error = await response
          .json()
          .catch(() => ({ message: "Error en la petición" }));
        throw new Error(error.message || `Error ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error(`Error in GET ${path}:`, error);
      throw error;
    }
  };

  const post = async <T = any>(path: string, data?: any): Promise<T> => {
    try {
      const url = path.startsWith("http") ? path : `${API_BASE_URL}${path}`;
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: data ? JSON.stringify(data) : undefined,
      });
      if (!response.ok) {
        const error = await response
          .json()
          .catch(() => ({ message: "Error en la petición" }));
        throw new Error(error.message || `Error ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error(`Error in POST ${path}:`, error);
      throw error;
    }
  };

  const put = async <T = any>(path: string, data?: any): Promise<T> => {
    try {
      const url = path.startsWith("http") ? path : `${API_BASE_URL}${path}`;
      const response = await fetch(url, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: data ? JSON.stringify(data) : undefined,
      });
      if (!response.ok) {
        const error = await response
          .json()
          .catch(() => ({ message: "Error en la petición" }));
        throw new Error(error.message || `Error ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error(`Error in PUT ${path}:`, error);
      throw error;
    }
  };

  const del = async <T = any>(path: string): Promise<T | void> => {
    try {
      const url = path.startsWith("http") ? path : `${API_BASE_URL}${path}`;
      const response = await fetch(url, {
        method: "DELETE",
      });
      if (!response.ok) {
        const error = await response
          .json()
          .catch(() => ({ message: "Error en la petición" }));
        throw new Error(error.message || `Error ${response.status}`);
      }
      // 204 No Content no tiene body, retornar void
      if (response.status === 204) {
        return;
      }
      // Intentar parsear JSON solo si hay contenido
      const contentType = response.headers.get("content-type");
      if (contentType && contentType.includes("application/json")) {
        const text = await response.text();
        return text ? JSON.parse(text) : undefined;
      }
    } catch (error) {
      console.error(`Error in DELETE ${path}:`, error);
      throw error;
    }
  };

  return {
    // Generic methods
    get,
    post,
    put,
    delete: del,
  };
};

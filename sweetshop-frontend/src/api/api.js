import axios from "axios";

export const API_URL = "http://127.0.0.1:8000/api"; // Backend base URL

// For public requests (register, login, etc.)
export const axiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// For authenticated requests (requires token)
export const axiosAuthInstance = (token) =>
  axios.create({
    baseURL: API_URL,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  });

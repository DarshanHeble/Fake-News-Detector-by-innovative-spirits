import axios from "axios";

const api = axios.create({
  baseURL: "https://my-fastapi-backend.onrender.com",
});

export default api;

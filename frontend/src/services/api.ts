import axios from "axios";

const api = axios.create({
  baseURL: "https://fake-news-detection-testing-69gw.onrender.com",
});

export default api;

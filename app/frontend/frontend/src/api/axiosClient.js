import axios from "axios";

const axiosClient = axios.create({
  baseURL: 'https://localhost:8443',
  headers: {
    'Content-Type': 'application/json'
  }
  // ❌ ما تحطش httpsAgent هنا!
});

export default axiosClient;



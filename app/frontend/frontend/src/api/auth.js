import axiosClient from './axiosClient';

export const login = async (username, password) => {
  try {
    const response = await axiosClient.post('/login', { username, password });
    return response.data;
  } catch (error) {
    console.error("Login error:", error.response || error.message);
    throw error;
  }
};


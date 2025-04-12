import api from "./axiosClient";

export const chatWithBot = async (prompt) => {
  const response = await api.post("/chat", { prompt });
  return response.data;
};

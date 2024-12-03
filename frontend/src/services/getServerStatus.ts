import api from "./api";

const getServerStatus = async (): Promise<string> => {
  const response = await api.get("/connection-status");
  return response.data.status;
};

export default getServerStatus;

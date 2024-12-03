import api from "./api";

const getServerStatus = async (): Promise<boolean> => {
  try {
    const response = await api.get("/connection-status");
    return response.status === 200;
  } catch (error) {
    console.error(error);
    return false;
  }
};

export default getServerStatus;

// import required types and API instances
import { InputNewsType, OutputNewsType } from "@Types/types";
import api from "./api";

/**
 * verifies the authenticity of a news by sending it to the backend.
 *
 * @param newsData - An object containing the news and its type (e.g., text or url).
 * @returns A promise that resolves to the verification result ("outputNewsType") or "false" if an error occurs.
 */

const verifyNews = async (
  newsData: InputNewsType
): Promise<OutputNewsType | false> => {
  try {
    // Make a POST request to the /verifyNews endpoint with the provided newsData
    const response = await api.post<OutputNewsType>("/verify-news", newsData);
    console.log(response);

    // Return the data received from the backend
    return response.data;
  } catch (error) {
    console.error("Error while verifying the news: ", error);

    // Return "false" to indicate the operation failed
    return false;
  }
};

export const verifyMessage = async (
  messageData: InputNewsType
): Promise<OutputNewsType | false> => {
  try {
    const response = await api.post<OutputNewsType>(
      "/verify-message",
      messageData
    );
    return response.data;
  } catch (error) {
    console.error("Error while verifying the message: ", error);
    return false;
  }
};

export default verifyNews;

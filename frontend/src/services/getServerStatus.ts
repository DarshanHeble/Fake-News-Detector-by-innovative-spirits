import api from "./api"; // import api instance from axios

/**
 * getServerStatus
 * This function checks if the server's connection status but making a HTTP GET request
 * to the "/connection-status" endpoint
 *
 * @returns {Promise<boolean>} - returns true if the server is reachable (HTTP 200), otherwise false}
 */

const getServerStatus = async (): Promise<boolean> => {
  try {
    // Send a GET request to the server
    const response = await api.get("/connection-status");

    // Return true if the response status code is 200 (OK)
    return response.status === 200;
  } catch (error) {
    console.error("Error checking server status:", error);

    // Return false if the server is unreachable or an error occurs
    return false;
  }
};

export default getServerStatus;

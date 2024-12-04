// import
import { NewsDataType } from "@Types/types";

const verifyNews = (newsData: NewsDataType) => {
  try {
    console.log(newsData);
  } catch (error) {
    console.error(error);
  }
};

export default verifyNews;

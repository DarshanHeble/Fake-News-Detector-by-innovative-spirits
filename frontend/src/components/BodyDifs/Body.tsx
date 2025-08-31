import style from "./Body.module.css";
import FNDB from "../../assets/FNDbackground.png";
import { useRef, useState } from "react";
import verifyNews from "@services/verifyNews";
import { FetchedNewsType, InputNewsType, OutputNewsType } from "@Types/types";
import { motion } from "framer-motion";
import Loading from "@components/Loading";

type Message = {
  newsInput: InputNewsType;
  result?: OutputNewsType;
};

export const Body = () => {
  const [inputValue, setInputValue] = useState(""); // State for input value
  const [result, setResult] = useState<false | OutputNewsType>(false);
  const [loading, setLoading] = useState(false);
  const [showPopup, setShowPopup] = useState(false);
  const [data, setData] = useState<FetchedNewsType[]>([]); // State for table data

  const inputRef = useRef<HTMLTextAreaElement>(null);

  const [, setMessage] = useState<Message[]>([]); // State for message

  const isValidInput = (input: string): boolean => {
    if (!input.trim()) return false; // Reject empty input

    const urlPattern = new RegExp(
      "^(https?:\\/\\/)?" + // protocol
        "((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.?)+[a-z]{2,}|" + // domain name
        "((\\d{1,3}\\.){3}\\d{1,3}))" + // OR ip (v4) address
        "(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*" + // port and path
        "(\\?[;&a-z\\d%_.~+=-]*)?" + // query string
        "(\\#[-a-z\\d_]*)?$",
      "i"
    );

    // Return true if valid URL or non-empty text
    return urlPattern.test(input) || input.trim().length > 0;
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const value = e.target.value;
    setInputValue(value);

    if (value && !isValidInput(value)) {
      alert("Please enter a valid URL or non-empty text.");
    }
  };

  const handleDetect = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true); // Start loading

    const value = inputValue.trim();

    if (!value.trim()) {
      alert("Please provide text to analyze."); // Replace with a styled alert component if needed
      setLoading(false); // Stop loading
      return;
    }

    const isURL = isValidInput(value) && value.startsWith("http");
    if (inputRef.current) inputRef.current.blur();

    try {
      const response = await verifyNews({
        category: isURL ? "url" : "text",
        content: value,
      });

      console.log(isURL);

      if (response !== false) {
        setMessage((prev) => [
          ...prev,
          {
            newsInput: { category: isURL ? "url" : "text", content: value },
            result: response,
          },
        ]); // Update message state
      }

      setResult(response);
      setShowPopup(true); // Show popup on successful result

      // Update data state with suggestions
      if (response && response.relatedNews) {
        setData(
          response.relatedNews.map((suggestion: FetchedNewsType) => ({
            link: suggestion.link,
            source: suggestion.source,
          }))
        );
      }
    } catch (error) {
      console.error("Error verifying news:", error);
      setResult(false);
      setShowPopup(true); // Show popup even on failure
    } finally {
      setLoading(false); // Stop loading
      if (inputRef.current) inputRef.current.blur();
    }
  };

  return (
    <div className={style.Mw}>
      <div className={style.mainwork}>
        {/* Background Image */}
        <img className={style.fndb} src={FNDB} alt="FNDB" />

        {/* Header Section */}
        <motion.div
          initial={{ y: 30, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 1, ease: "anticipate" }}
          className={style.mainlettercon}
        >
          <span
            className={`${style.mainletterstyle} ${style["anton-regular"]}`}
          >
            Detect Fake News With
          </span>
          <br />
          <span
            className={`${style.mainletterstyle} ${style["anton-regular"]}`}
          >
            Our Real-Time AI Fake News Checker
          </span>
        </motion.div>

        {/* Main Content */}
        <motion.div
          initial={{ y: 40, opacity: 0 }}
          animate={{ y: 30, opacity: 1 }}
          transition={{ duration: 0.8, ease: "anticipate" }}
          className={style.mainCon}
        >
          <form className={style.processCon} onSubmit={handleDetect}>
            {/* Input Section */}
            <div className={style.textBox}>
              <svg
                className={style.ailogo}
                viewBox="0 0 167 195"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M84 50L62.3494 37.5L62.3494 12.5L84 1.62913e-06L105.651 12.5L105.651 37.5L84 50Z"
                  fill="black"
                />
                <path
                  d="M43.7858 75.7877L22.0795 88.1909L0.484937 75.5944L0.596567 50.5946L22.3028 38.1914L43.8974 50.788L43.7858 75.7877Z"
                  fill="black"
                />
                <path
                  d="M122.544 75.713L122.493 50.7131L144.118 38.1692L165.794 50.6252L165.845 75.6251L144.22 88.1691L122.544 75.713Z"
                  fill="black"
                />
                <path
                  d="M43.8561 146.04L22.454 158.96L0.563088 146.886L0.0743392 121.891L21.4765 108.97L43.3673 121.044L43.8561 146.04Z"
                  fill="black"
                />
                <path
                  d="M123.395 120.711L144.985 108.106L166.696 120.501L166.817 145.501L145.227 158.106L123.516 145.711L123.395 120.711Z"
                  fill="black"
                />
                <path
                  d="M83.9999 67.0549L110.008 82.0073L110.063 112.007L84.1097 127.055L58.1016 112.102L58.0467 82.1024L83.9999 67.0549Z"
                  fill="black"
                />
                <path
                  d="M84.2395 144.12L105.83 156.724L105.71 181.723L83.9997 194.119L62.4093 181.516L62.5291 156.516L84.2395 144.12Z"
                  fill="black"
                />
                <path
                  d="M144 63L145 133"
                  stroke="white"
                  strokeWidth="3"
                  strokeLinecap="round"
                />
                <path
                  d="M84 26L144 63"
                  stroke="white"
                  strokeWidth="3"
                  strokeLinecap="round"
                />
                <path
                  d="M84 26L22 63"
                  stroke="white"
                  strokeWidth="3"
                  strokeLinecap="round"
                />
                <path
                  d="M84 169L145 134"
                  stroke="white"
                  strokeWidth="3"
                  strokeLinecap="round"
                />
                <path
                  d="M84 97L22 63"
                  stroke="white"
                  strokeWidth="3"
                  strokeLinecap="round"
                />
                <path
                  d="M84 97L143 63"
                  stroke="white"
                  strokeWidth="3"
                  strokeLinecap="round"
                />
                <path
                  d="M84 97V168"
                  stroke="white"
                  strokeWidth="3"
                  strokeLinecap="round"
                />
                <path
                  d="M22 63V134"
                  stroke="white"
                  strokeWidth="3"
                  strokeLinecap="round"
                />
                <path
                  d="M84 169L22 135"
                  stroke="white"
                  strokeWidth="3"
                  strokeLinecap="round"
                />
              </svg>
              <textarea
                className={style.inputbox}
                placeholder="Type text or URL"
                value={inputValue}
                ref={inputRef}
                onChange={handleInputChange}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault(); // Prevent new line
                    handleDetect(e); // Trigger form submission
                  }
                }}
                rows={3} // Minimum 3 lines
              />
            </div>

            <div
              className={style.btndetect}
              onClick={!loading ? handleDetect : undefined} // Prevent double-click during loading
              style={{
                pointerEvents: loading ? "none" : "auto",
                opacity: loading ? 0.8 : 1,
              }}
            >
              {loading ? <Loading /> : "Detect"}
            </div>
          </form>
        </motion.div>

        {/* Popup Section */}
        {showPopup && (
          <div className={style.popup}>
            <div className={style.popupContent}>
              {result ? (
                <>
                  <h2
                    className={
                      result.label === "fake"
                        ? style.red
                        : result.label === "neutral"
                        ? style.neutral
                        : style.green
                    }
                  >
                    Result: This article is {result.label}
                  </h2>
                  <p>
                    {result.label === "fake"
                      ? "Be cautious! This news article might be misleading."
                      : result.label === "neutral"
                      ? "This article is neutral. Please review further."
                      : "This article seems genuine. Stay informed!"}
                  </p>
                </>
              ) : (
                <h2 style={{ color: "red" }}>
                  Error verifying news. Please try again.
                </h2>
              )}
              <button
                className={style.closeBtn}
                onClick={() => setShowPopup(false)}
              >
                Close
              </button>
            </div>
          </div>
        )}
      </div>
      {/* Table Section */}
      {data.length > 0 && (
        <div className={style.tableContainer}>
          <table className={style.table}>
            <thead>
              <tr>
                <th>Sr.no</th>
                <th>Link</th>
                <th>Domain</th>
              </tr>
            </thead>
            <tbody>
              {data.map((row, index) => (
                <tr key={index}>
                  <td>{index + 1}</td>
                  {/* Use index as key */}
                  <td>
                    <a href={row.link} target="_blank" rel="noreferrer">
                      {row.link}
                    </a>
                  </td>
                  <td>{row.source}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      {/* End of Table Section */}
    </div>
  );
};

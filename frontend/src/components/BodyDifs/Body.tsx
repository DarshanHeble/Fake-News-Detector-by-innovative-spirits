import style from "./Body.module.css";
import FNDB from "../../assets/FNDbackground.png";
import { useState} from "react";
import verifyNews from "@services/verifyNews";
import { OutputNewsType } from "@Types/types";

export const Body = () => {
  const [inputValue, setInputValue] = useState(""); // State for input value
  const [result, setResult] = useState<false | OutputNewsType>(false);
  const [loading, setLoading] = useState(false);
  const [showPopup, setShowPopup] = useState(false);


  const handleDetect = async () => {
    if (!inputValue.trim()) {
      alert("Please provide text to analyze."); // Replace with a styled alert component if needed
      return;
    }


    setLoading(true); // Start loading
    try {
      const response = await verifyNews({ category: "text", content: inputValue });
      setResult(response);
      setShowPopup(true); // Show popup on successful result
    } catch (error) {
      console.error("Error verifying news:", error);
      setResult(false);
      setShowPopup(true); // Show popup even on failure
    } finally {
      setLoading(false); // Stop loading
    }
  };

  return (
    <div className={style.mainwork}>
      {/* Background Image */}
      <img className={style.fndb} src={FNDB} alt="FNDB" />

      {/* Header Section */}
      <div className={style.mainlettercon}>
        <span className={style.mainletterstyle}>Detect Fake News With</span>
        <br />
        <span className={style.mainletterstyle}>Our Real-Time AI Fake News Detector</span>
      </div>

      {/* Main Content */}
      <div className={style.mainCon}>
        <div className={style.processCon}>
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
            <input
              className={style.inputbox}
              type="text"
              placeholder="Type text or URL"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)} // Update state on input change
            />
          </div>

          <div
            className={style.btndetect}
            onClick={!loading ? handleDetect : undefined} // Prevent double-click during loading
            style={{ pointerEvents: loading ? "none" : "auto", opacity: loading ? 0.6 : 1 }}
          >
            {loading ? "Loading..." : "Detect"}
          </div>
        </div>
      </div>

      {/* Popup Section */}
      {showPopup && (
        <div className={style.popup}>
          <div className={style.popupContent}>
            {result ? (
              <>
                <h2 style={{ color: result.label === "fake" ? "red" : "green" }}>
                  Result: This article is {result.label}
                </h2>
                <p>
                  {result.label === "fake"
                    ? "Be cautious! This news article might be misleading."
                    : "This article seems genuine. Stay informed!"}
                </p>
              </>
            ) : (

              <h2 style={{ color: "red" }}>Error verifying news. Please try again.</h2>
            )}
            <button className={style.closeBtn} onClick={() => setShowPopup(false)}>
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
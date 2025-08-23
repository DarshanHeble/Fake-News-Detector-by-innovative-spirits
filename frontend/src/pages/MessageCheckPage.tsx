import { useState, useRef } from "react";
import style from "../components/BodyDifs/Body.module.css";
import Loading from "@components/Loading";
import verifyNews from "@services/verifyNews";
import { OutputNewsType, FetchedNewsType } from "@Types/types";
import FNDB from "../assets/FNDbackground.png";

const MessageCheckPage = () => {
  const [inputValue, setInputValue] = useState("");
  const [result, setResult] = useState<false | OutputNewsType>(false);
  const [loading, setLoading] = useState(false);
  const [showPopup, setShowPopup] = useState(false);
  const [data, setData] = useState<FetchedNewsType[]>([]);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputValue(e.target.value);
  };

  const handleDetect = async (e: React.FormEvent | React.MouseEvent) => {
    e.preventDefault();
    setLoading(true);

    const value = inputValue.trim();
    if (!value) {
      alert("Please provide a message to analyze.");
      setLoading(false);
      return;
    }

    try {
      const response = await verifyNews({
        category: "text",
        content: value,
      });

      if (response !== false) {
        setResult(response);
        setShowPopup(true);
        if (response.relatedNews) {
          setData(
            response.relatedNews.map((suggestion: FetchedNewsType) => ({
              link: suggestion.link,
              source: suggestion.source,
            }))
          );
        }
      } else {
        setResult(false);
        setShowPopup(true);
      }
    } catch (error) {
      setResult(false);
      setShowPopup(true);
    } finally {
      setLoading(false);
      if (inputRef.current) inputRef.current.blur();
    }
  };

  return (
    <div className={style.pageWrap}>
      <img src={FNDB} alt="background" className={style["page-bg"]} />
      <div className={style.pageContent}>
        <div
          style={{
            background: "#fff",
            borderRadius: 12,
            boxShadow: "0 2px 12px #e0e0e0",
            padding: "18px 32px",
            minWidth: 320,
            maxWidth: 480,
            width: "100%",
            textAlign: "center",
            margin: "0 auto",
          }}
        >
          <h2 style={{ fontWeight: 700, fontSize: "1.5rem", color: "#00796b" }}>
            Check Fake News in Your Message
          </h2>
          <p style={{ color: "#444", fontSize: "1rem", marginBottom: 18 }}>
            Paste or type a message (e.g., WhatsApp, SMS, Email) to check if it contains fake news.
          </p>
          <form onSubmit={handleDetect}>
            <textarea
              ref={inputRef}
              className={style.inputbox}
              placeholder="Paste your message here..."
              value={inputValue}
              onChange={handleInputChange}
              rows={5}
              style={{
                marginBottom: 16,
                minHeight: 80,
                fontSize: "1.1rem",
                border: "1.5px solid #b2dfdb",
                background: "#f7fafc",
              }}
            />
            <div
              className={style.btndetect}
              onClick={!loading ? handleDetect : undefined}
              style={{
                pointerEvents: loading ? "none" : "auto",
                opacity: loading ? 0.8 : 1,
                background: "#00796b",
                color: "#fff",
                fontWeight: 600,
                marginTop: 8,
              }}
            >
              {loading ? <Loading /> : "Check Message"}
            </div>
          </form>
        </div>
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
                    Result: This message is {result.label}
                  </h2>
                  <p>
                    {result.label === "fake"
                      ? "Warning: This message may contain misleading or false information."
                      : result.label === "neutral"
                      ? "This message is neutral. Please review further."
                      : "This message seems genuine. Stay informed!"}
                  </p>
                </>
              ) : (
                <h2 style={{ color: "red" }}>
                  Error verifying message. Please try again.
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
    </div>
  );
};

export default MessageCheckPage;

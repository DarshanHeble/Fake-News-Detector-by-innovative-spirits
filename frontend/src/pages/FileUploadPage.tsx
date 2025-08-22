import { useState, useRef } from "react";
import style from "../components/BodyDifs/Body.module.css";
import Loading from "@components/Loading";
import verifyNews from "@services/verifyNews";
import { OutputNewsType, FetchedNewsType } from "@Types/types";

const FileUploadPage = () => {
  const [file, setFile] = useState<File | null>(null);
  const [fileContent, setFileContent] = useState<string>("");
  const [result, setResult] = useState<false | OutputNewsType>(false);
  const [loading, setLoading] = useState(false);
  const [showPopup, setShowPopup] = useState(false);
  const [data, setData] = useState<FetchedNewsType[]>([]);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0] || null;
    setFile(selectedFile);

    if (selectedFile) {
      const reader = new FileReader();
      reader.onload = (event) => {
        setFileContent(event.target?.result as string);
      };
      reader.readAsText(selectedFile);
    } else {
      setFileContent("");
    }
  };

  const handleDetect = async (e: React.FormEvent | React.MouseEvent) => {
    e.preventDefault();
    setLoading(true);

    if (!file || !fileContent.trim()) {
      alert("Please upload a file with content to analyze.");
      setLoading(false);
      return;
    }

    try {
      const response = await verifyNews({
        category: "text",
        content: fileContent,
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
      if (inputRef.current) inputRef.current.value = "";
    }
  };

  return (
    <div className={style.Mw}>
      <div className={style.mainwork}>
        <div
          style={{
            position: "absolute",
            top: 40,
            left: "50%",
            transform: "translateX(-50%)",
            zIndex: 2,
            background: "#fff",
            borderRadius: 12,
            boxShadow: "0 2px 12px #e0e0e0",
            padding: "18px 32px",
            minWidth: 320,
            maxWidth: 480,
            width: "90%",
            textAlign: "center",
          }}
        >
          <h2 style={{ fontWeight: 700, fontSize: "1.5rem", color: "#00796b" }}>
            Check Fake News from File
          </h2>
          <p style={{ color: "#444", fontSize: "1rem", marginBottom: 18 }}>
            Upload a text file (.txt) containing news or message content to check for fake news.
          </p>
          <form onSubmit={handleDetect}>
            <input
              ref={inputRef}
              type="file"
              accept=".txt"
              onChange={handleFileChange}
              style={{
                marginBottom: 16,
                padding: "8px 0",
                fontSize: "1.1rem",
                border: "1.5px solid #b2dfdb",
                background: "#f7fafc",
                borderRadius: 8,
                width: "100%",
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
              {loading ? <Loading /> : "Check File"}
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
                    Result: This file content is {result.label}
                  </h2>
                  <p>
                    {result.label === "fake"
                      ? "Warning: This file may contain misleading or false information."
                      : result.label === "neutral"
                      ? "This file is neutral. Please review further."
                      : "This file seems genuine. Stay informed!"}
                  </p>
                </>
              ) : (
                <h2 style={{ color: "red" }}>
                  Error verifying file. Please try again.
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

export default FileUploadPage;

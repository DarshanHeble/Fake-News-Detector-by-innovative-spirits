import "./index.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import getServerStatus from "@services/getServerStatus";
import { Header } from "@components/HeaderDifs/Header";
import { Body } from "@components/BodyDifs/Body";
import QuizPage from "@pages/QuizPage";
import MessageCheckPage from "@pages/MessageCheckPage";
import FileUploadPage from "@pages/FileUploadPage";

function App() {
  getServerStatus().then((responce) => {
    console.log("Connection Status: " + responce);
  });

  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route path="/" element={<Body />} />
        <Route path="/quiz" element={<QuizPage />} />
        <Route path="/messages" element={<MessageCheckPage />} />
        <Route path="/file" element={<FileUploadPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

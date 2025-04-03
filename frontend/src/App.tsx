import ChatPage from "@pages/ChatPage";
import "./index.css";
import getServerStatus from "@services/getServerStatus";
import { Header } from "@components/HeaderDifs/Header";
import { Body } from "@components/BodyDifs/Body";
import Chat from "@components/Chat/Chat";

function App() {
  getServerStatus().then((responce) => {
    console.log("Connection Status: " + responce);
  });

  return (
    <>
      <Header />
      <Body />
      {/* <Chat /> */}
      {/* <ChatPage /> */}
    </>
  );
}

export default App;

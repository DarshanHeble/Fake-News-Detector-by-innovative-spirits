import { Header } from "@components/HeaderDifs/Header";
import "./App.css";
import { Body } from "@components/BodyDifs/Body";
import getServerStatus from "@services/getServerStatus";
import Chat from "@components/Chat/Chat";

function App() {
  getServerStatus().then((responce) => {
    console.log("Connection Status: " + responce);
  });

  return (
    <>
      <Header />
      <Body />
      <Chat />
    </>
  );
}

export default App;

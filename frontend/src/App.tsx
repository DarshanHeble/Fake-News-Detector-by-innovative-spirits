import "./index.css";
import getServerStatus from "@services/getServerStatus";
import { Header } from "@components/HeaderDifs/Header";
import { Body } from "@components/BodyDifs/Body";

function App() {
  getServerStatus().then((responce) => {
    console.log("Connection Status: " + responce);
  });

  return (
    <>
      <Header />
      <Body />
    </>
  );
}

export default App;

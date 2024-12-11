import { Header } from "@components/HeaderDifs/Header";
import "./App.css";
import getServerStatus from "@services/getServerStatus";
import verifyNews from "@services/verifyNews";
import { Body } from "@components/BodyDifs/Body";

function App() {
  // get server status
  getServerStatus().then((status) => {
    console.log(status);
  });

  // verify news(testing)
  verifyNews({ category: "text", content: "hello" }).then((response) => {
    console.log(response);
  });

  return (
    <>
      <Header />
      <Body />
    </>
  );
}

export default App;

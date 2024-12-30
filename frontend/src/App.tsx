import { Header } from "@components/HeaderDifs/Header";
import "./App.css";
import { Body } from "@components/BodyDifs/Body";
// import {  } from "@components/TableDifs/Table";
// import { ResultsTable } from "@components/TableDifs/Result";
import getServerStatus from "@services/getServerStatus";

function App() {
  getServerStatus().then((responce) => {
    console.log("Connection Status: " + responce);
  });
  return (
    <>
      <Header />
      <Body />
      {/* <ResultsTable data={[]} /> */}
    </>
  );
}

export default App;

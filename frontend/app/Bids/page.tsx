import Header from "../../components/Header";
import Footer from "../../components/Footer";
import Bids from "./BidList";


export default function Home() {
  return (
    <main>
      <Header />
      <Bids params={1}/>
      
      <Footer />
     </main>
  );
}

import Header from "../../components/Header";
import Footer from "../../components/Footer";
import AuctionGrid from "./CombiAuctionList";

import CreateProduct from "./Product_form"
import CreateAuction from "./Auction_form"


export default function Home() {
  return (
    <main>
      <Header />
      <AuctionGrid /> 

      <Footer />
     </main>
  );
}

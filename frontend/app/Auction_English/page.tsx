import Header from "../../components/Header";
import Footer from "../../components/Footer";
import AuctionGrid from "./EnglishAuctionList";
import CreateAuctionForm from "./form";
// import AuctionProductPage from "../components/AuctionProductPage";
// import English_Auction_Item from "../components/EnglishAuctionItem";

export default function Home() {
  return (
    <main>
      <Header />
      <AuctionGrid /> 
      
      <Footer />
     </main>
  );
}

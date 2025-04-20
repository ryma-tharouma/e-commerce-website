import Header from "../../../components/Header";
import Footer from "../../../components/Footer";
import CreateAuctionForm from "../form";
// import AuctionProductPage from "../components/AuctionProductPage";
// import English_Auction_Item from "../components/EnglishAuctionItem";

export default function Home() {
  return (
    <main>
      <Header />
      
      <CreateAuctionForm/>
      <Footer />
     </main>
  );
}

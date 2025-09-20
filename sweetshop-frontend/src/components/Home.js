import { Link } from "react-router-dom";
import "./Home.css";

function Home() {
  return (
    <div className="home-container">
      <div className="overlay">
        <h1>🍬 Welcome to Sweet Shop 🍬</h1>
        <p>Your one-stop shop for delicious sweets!</p>
        <div className="home-buttons">
          <Link to="/register" className="btn btn-primary">Register</Link>
          <Link to="/login" className="btn btn-secondary">Login</Link>
        </div>
      </div>
    </div>
  );
}

export default Home;

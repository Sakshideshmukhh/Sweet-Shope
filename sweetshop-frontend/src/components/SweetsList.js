import { useEffect, useState } from "react";
import { axiosAuthInstance } from "../api/api";
import { useNavigate, Link } from "react-router-dom";
import "./SweetList.css";

function SweetsList() {
  const [sweets, setSweets] = useState([]);
  const navigate = useNavigate();
  const token = localStorage.getItem("access_token");
  const axios = axiosAuthInstance(token);

  const fetchSweets = async () => {
    try {
      const response = await axios.get("/sweets");
      setSweets(response.data);
    } catch {
      alert("Error fetching sweets");
    }
  };

  const deleteSweet = async (id) => {
    if (!window.confirm("Are you sure you want to delete this sweet?")) return;
    try {
      await axios.delete(`/sweets/${id}`);
      fetchSweets();
    } catch {
      alert("Error deleting sweet");
    }
  };

  useEffect(() => {
    fetchSweets();
  }, []);

  return (
    <div className="sweets-container">
      <h2>Our Delicious Sweets 🍬</h2>
      <Link to="/sweets/add" className="btn-add">Add Sweet</Link>
      <div className="sweets-grid">
        {sweets.map((sweet) => (
          <div className="sweet-card" key={sweet.id}>
            <img src={`https://source.unsplash.com/200x150/?candy,${sweet.name}`} alt={sweet.name} />
            <h3>{sweet.name}</h3>
            <p>Category: {sweet.category}</p>
            <p>Price: {sweet.price}rs</p>
            <p>Quantity: {sweet.quantity}</p>
            <button className="btn-delete" onClick={() => deleteSweet(sweet.id)}>Delete</button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default SweetsList;

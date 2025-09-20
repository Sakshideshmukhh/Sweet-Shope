import { useState } from "react";
import { axiosAuthInstance } from "../api/api";
import { useNavigate } from "react-router-dom";
import "./Form.css";

function SweetForm() {
  const [name, setName] = useState("");
  const [category, setCategory] = useState("");
  const [price, setPrice] = useState("");
  const [quantity, setQuantity] = useState("");
  const navigate = useNavigate();
  const token = localStorage.getItem("access_token");
  const axios = axiosAuthInstance(token);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("/sweets", { name, category, price: parseFloat(price), quantity: parseInt(quantity) });
      navigate("/sweets");
    } catch {
      alert("Error adding sweet");
    }
  };

  return (
    <div className="form-container">
      <h2>Add a New Sweet 🍭</h2>
      <form onSubmit={handleSubmit}>
        <input placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
        <input placeholder="Category" value={category} onChange={(e) => setCategory(e.target.value)} />
        <input placeholder="Price" value={price} onChange={(e) => setPrice(e.target.value)} />
        <input placeholder="Quantity" value={quantity} onChange={(e) => setQuantity(e.target.value)} />
        <button type="submit">Add Sweet</button>
      </form>
    </div>
  );
}

export default SweetForm;

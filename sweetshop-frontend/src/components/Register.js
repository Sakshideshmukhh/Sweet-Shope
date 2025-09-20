import { useState } from "react";
import { axiosInstance } from "../api/api";
import { useNavigate } from "react-router-dom";
import "./Form.css";

function Register() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
    //  const response = await axiosInstance.post("/register", { username, email, password });
      const response = await axiosInstance.post("/auth/register", { username, email, password });


      localStorage.setItem("access_token", response.data.access_token);
      navigate("/sweets");
    } catch (err) {
      alert(err.response?.data?.detail || "Error registering user");
    }
  };

  return (
    <div className="form-container">
      <h2>Register</h2>
      <form onSubmit={handleRegister}>
        <input placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
        <input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <button type="submit">Register</button>
      </form>
    </div>
  );
}

export default Register;

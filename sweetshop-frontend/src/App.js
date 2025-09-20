import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Home from "./components/Home";
import Register from "./components/Register";
import Login from "./components/Login";
import SweetsList from "./components/SweetsList";
import SweetForm from "./components/SweetForm";

function App() {
  const isLoggedIn = !!localStorage.getItem("access_token"); // check login

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route
          path="/sweets"
          element={isLoggedIn ? <SweetsList /> : <Navigate to="/login" />}
        />
        <Route
          path="/sweets/add"
          element={isLoggedIn ? <SweetForm /> : <Navigate to="/login" />}
        />
      </Routes>
    </Router>
  );
}

export default App;

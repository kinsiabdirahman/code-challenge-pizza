import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./layout/Layout";
import Home from "./pages/Home";
import Restaurant from "./pages/Restaurant";
import Pizzas from "./pages/Pizzas";

function App() {
  return (
    <div>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Home />} />
            <Route path="restaurants/:id" element={<Restaurant />} />
            <Route path="pizzas" element={<Pizzas />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;

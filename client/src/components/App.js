import { useState, useEffect } from "react";
import { Switch, Route } from "react-router-dom";
import Article from "./Article";
import Header from "./Header";
import Home from "./Home";
import Login from "./Login";

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetch("/check_session").then((response) => {
      if (response.ok) {
        response.json().then((user) => setUser(user));
      }
    });
  }, []);

  function handleLogin(user) {
    fetch("/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username: user.username }), // Expecting username field
    })
      .then((response) => {
        if (response.ok) {
          response.json().then((data) => setUser(data));
        } else {
          console.error("Login failed");
        }
      })
      .catch((error) => console.error("Login error:", error));
  }

  // Handle logout
  function handleLogout() {
    fetch("/logout", { method: "DELETE" }).then(() => {
      setUser(null);
    });
  }

  return (
    <div className="App">
      <Header user={user} onLogout={handleLogout} />
      <Switch>
        <Route exact path="/">
          <Home />
        </Route>
        <Route exact path="/articles/:id">
          <Article />
        </Route>
        <Route exact path="/login">
          <Login onLogin={handleLogin} />
        </Route>
        <Route exact path="/logout">
          <button onClick={handleLogout}>Logout</button>
        </Route>
      </Switch>
    </div>
  );
}


export default App;

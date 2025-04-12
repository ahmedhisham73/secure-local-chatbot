import React, { useState } from 'react';
import Login from './pages/Login';
import Chat from './pages/Chat';

const App = () => {
  const [token, setToken] = useState(null);

  return (
    <div className="App">
      {/* Check if the token exists, if not show the Login component */}
      {!token ? (
        <Login setToken={setToken} />
      ) : (
        <Chat token={token} />
      )}
    </div>
  );
};

export default App;


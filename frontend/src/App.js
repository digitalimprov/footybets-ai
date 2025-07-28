import React, { useEffect } from 'react';

const App = () => {
  useEffect(() => {
    // Redirect to maintenance page
    window.location.href = '/maintenance.html';
  }, []);

  return (
    <div style={{ 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center', 
      height: '100vh',
      backgroundColor: '#667eea',
      color: 'white',
      fontFamily: 'Arial, sans-serif'
    }}>
      <div style={{ textAlign: 'center' }}>
        <h1>FootyBets.ai</h1>
        <p>Redirecting to maintenance page...</p>
        <p>If you're not redirected, <a href="/maintenance.html" style={{ color: '#ffeb3b' }}>click here</a></p>
      </div>
    </div>
  );
};

export default App; 
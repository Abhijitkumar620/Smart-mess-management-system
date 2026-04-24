import React from 'react';
import AdminDashboard from './AdminDashboard'; 

function App() {
  return (
    <div style={{ fontFamily: 'Arial, sans-serif' }}>
      <nav style={{ padding: '20px', background: '#007bff', color: 'white' }}>
        <h2>Smart Mess Management System</h2>
      </nav>
      <div style={{ padding: '20px' }}>
        <AdminDashboard />
      </div>
    </div>
  );
}

export default App;
import React, { useState } from 'react';

const AdminDashboard = () => {
    // Dummy data - Baad mein isse database se connect karenge
    const [members] = useState([
        { id: 1, name: "Raja", room: "101", status: "Paid" },
        { id: 2, name: "Abhijit", room: "102", status: "Pending" },
        { id: 3, name: "Suresh", room: "105", status: "Paid" }
    ]);

    return (
        <div style={{ padding: '20px', fontFamily: 'Arial' }}>
            <h2 style={{ color: '#2c3e50' }}>Admin Dashboard - Mess Management</h2>
            <div style={{ display: 'flex', gap: '20px', marginBottom: '20px' }}>
                <div style={{ padding: '20px', background: '#3498db', color: 'white', borderRadius: '8px', flex: 1 }}>
                    <h3>Total Members</h3>
                    <p style={{ fontSize: '24px' }}>{members.length}</p>
                </div>
                <div style={{ padding: '20px', background: '#2ecc71', color: 'white', borderRadius: '8px', flex: 1 }}>
                    <h3>Active Mess</h3>
                    <p style={{ fontSize: '24px' }}>Ready</p>
                </div>
            </div>

            <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '20px' }}>
                <thead>
                    <tr style={{ background: '#ecf0f1', textAlign: 'left' }}>
                        <th style={{ padding: '12px', border: '1px solid #ddd' }}>Name</th>
                        <th style={{ padding: '12px', border: '1px solid #ddd' }}>Room No</th>
                        <th style={{ padding: '12px', border: '1px solid #ddd' }}>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {members.map(member => (
                        <tr key={member.id}>
                            <td style={{ padding: '12px', border: '1px solid #ddd' }}>{member.name}</td>
                            <td style={{ padding: '12px', border: '1px solid #ddd' }}>{member.room}</td>
                            <td style={{ padding: '12px', border: '1px solid #ddd', color: member.status === 'Paid' ? 'green' : 'red' }}>
                                {member.status}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default AdminDashboard;
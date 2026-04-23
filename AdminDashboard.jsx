import React, { useState, useEffect } from 'react';
import MemberManagement from '../components/admin/MemberManagement';
import MenuManagement from '../components/admin/MenuManagement';
import { api } from '../services/api';

const AdminDashboard = () => {
  const [activeTab, setActiveTab] = useState('members');
  const [stats, setStats] = useState({});

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await api.get('/admin/stats');
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const tabs = [
    { id: 'members', label: 'Member Management', component: <MemberManagement /> },
    { id: 'menu', label: 'Menu Management', component: <MenuManagement /> },
    { id: 'billing', label: 'Billing Overview', component: <div>Billing</div> },
    { id: 'leaves', label: 'Leave Requests', component: <div>Leaves</div> },
  ];

  return (
    <div className="max-w-7xl mx-auto py-10 px-4 sm:px-6 lg:px-8">
      <div className

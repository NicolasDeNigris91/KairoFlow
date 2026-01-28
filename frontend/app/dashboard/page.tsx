'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import ActivityForm from '@/components/charts/ActivityForm';
import ActivityList from '@/components/charts/ActivityList';
import ActivityChart from '@/components/charts/ActivityChart';
import StatsCards from '@/components/charts/StatsCards'; 

export default function DashboardPage() {
  const [userEmail, setUserEmail] = useState('');
  const [refreshKey, setRefreshKey] = useState(0);
  const router = useRouter();

  useEffect(() => {
    if (typeof window === 'undefined') {
      return;
    }
    
    const token = localStorage.getItem('access_token');
    const email = localStorage.getItem('user_email');
    
    if (!token) {
      router.push('/');
      return;
    }
    
    setUserEmail(email || '');
  }, [router]);

  const refreshAllComponents = () => {
    setRefreshKey(prev => prev + 1);
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_email');
    router.push('/');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-gray-900">KairoFlow Dashboard</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-gray-700">{userEmail}</span>
              <button
                onClick={handleLogout}
                className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700 transition-colors duration-200"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <StatsCards refreshKey={refreshKey} />
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div>
            <ActivityForm onActivityCreated={refreshAllComponents} />
          </div>
          <div>
            <ActivityChart refreshKey={refreshKey} />
          </div>
        </div>

        <div className="mb-8">
          <ActivityList 
            onActivityDeleted={refreshAllComponents} 
            refreshKey={refreshKey}
          />
        </div>

        <div className="border-4 border-dashed border-gray-200 rounded-lg p-8 text-center">
          <h2 className="text-2xl font-semibold text-gray-700 mb-4">
            Welcome to KairoFlow
          </h2>
          <p className="text-gray-600">
            Your productivity dashboard is now ready.
          </p>
        </div>
      </main>
    </div>
  );
}
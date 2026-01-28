'use client';

import { useState, useEffect } from 'react';
import api from '@/lib/api';

interface StatsData {
  total_activities: number;
  total_hours: number;
  week_hours: number;
  most_frequent_type: string;
  consecutive_days: number;
  daily_goal_percentage: number;
  today_minutes: number;
  activities_by_type: Record<string, number>;
}

interface StatsCardsProps {
  refreshKey?: number;
}

export default function StatsCards({ refreshKey }: StatsCardsProps) {
  const [stats, setStats] = useState<StatsData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, [refreshKey]);

  const fetchStats = async () => {
    try {
      const response = await api.get('/stats');
      setStats(response.data);
    } catch (error) {
      console.error('Erro ao buscar estatísticas:', error);
    } finally {
      setLoading(false);
    }
  };

  const getTypeName = (type: string) => {
    const names: Record<string, string> = {
      'WORK': 'Trabalho',
      'STUDY': 'Estudo',
      'EXERCISE': 'Exercício',
      'LEISURE': 'Lazer',
      'OTHER': 'Outro'
    };
    return names[type] || type;
  };

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="bg-white p-6 rounded-lg shadow">
            <div className="h-4 bg-gray-200 rounded w-1/2 mb-3"></div>
            <div className="h-8 bg-gray-200 rounded"></div>
          </div>
        ))}
      </div>
    );
  }

  if (!stats) return null;

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="font-medium text-gray-900">Total Activities</h3>
        <p className="text-3xl font-bold text-blue-600 mt-2">{stats.total_activities}</p>
        <p className="text-sm text-gray-500 mt-1">
          Esta semana: {stats.week_hours.toFixed(1)}h
        </p>
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="font-medium text-gray-900">Total Time</h3>
        <p className="text-3xl font-bold text-green-600 mt-2">{stats.total_hours.toFixed(1)}h</p>
        <p className="text-sm text-gray-500 mt-1">
          Hoje: {Math.floor(stats.today_minutes / 60)}h {stats.today_minutes % 60}min
        </p>
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="font-medium text-gray-900">Meta Diária</h3>
        <p className="text-3xl font-bold text-purple-600 mt-2">{stats.daily_goal_percentage}%</p>
        <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
          <div 
            className="bg-purple-600 h-2 rounded-full" 
            style={{ width: `${stats.daily_goal_percentage}%` }}
          ></div>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="font-medium text-gray-900">Consecutive Days</h3>
        <p className="text-3xl font-bold text-yellow-600 mt-2">{stats.consecutive_days}</p>
        <p className="text-sm text-gray-500 mt-1">
          {stats.most_frequent_type ? getTypeName(stats.most_frequent_type) : 'Nenhuma atividade'}
        </p>
      </div>
    </div>
  );
}
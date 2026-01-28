'use client';

import { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { format, subDays, parseISO } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import api from '@/lib/api';

interface Activity {
  date: string;
  activity_type: string;
  duration_minutes: number;
}

interface ChartData {
  date: string;
  dateFormatted: string;
  work: number;
  study: number;
  exercise: number;
  leisure: number;
  other: number;
  total: number;
}

interface ActivityChartProps {
  refreshKey?: number;
}

export default function ActivityChart({ refreshKey }: ActivityChartProps) {
  const [chartData, setChartData] = useState<ChartData[]>([]);
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState(7);

  useEffect(() => {
    fetchChartData();
  }, [timeRange, refreshKey]);

  const fetchChartData = async () => {
    try {
      const response = await api.get('/activities');
      const activities: Activity[] = response.data;
      const processedData = processActivitiesForChart(activities, timeRange);
      setChartData(processedData);
    } catch (error) {
      console.error('Erro ao buscar dados:', error);
    } finally {
      setLoading(false);
    }
  };

  const processActivitiesForChart = (activities: Activity[], days: number): ChartData[] => {
    const data: ChartData[] = [];
    
    for (let i = days - 1; i >= 0; i--) {
      const date = subDays(new Date(), i);
      const dateStr = format(date, 'yyyy-MM-dd');
      const dateFormatted = format(date, 'EEE', { locale: ptBR });
      
      data.push({
        date: dateStr,
        dateFormatted: dateFormatted.charAt(0).toUpperCase() + dateFormatted.slice(1),
        work: 0,
        study: 0,
        exercise: 0,
        leisure: 0,
        other: 0,
        total: 0
      });
    }

    activities.forEach(activity => {
      const activityDate = format(parseISO(activity.date), 'yyyy-MM-dd');
      const dayData = data.find(d => d.date === activityDate);
      
      if (dayData) {
        const activityTypeLower = activity.activity_type.toLowerCase();
        
        switch (activityTypeLower) {
          case 'work':
            dayData.work += activity.duration_minutes;
            break;
          case 'study':
            dayData.study += activity.duration_minutes;
            break;
          case 'exercise':
            dayData.exercise += activity.duration_minutes;
            break;
          case 'leisure':
            dayData.leisure += activity.duration_minutes;
            break;
          case 'other':
            dayData.other += activity.duration_minutes;
            break;
        }
        dayData.total += activity.duration_minutes;
      }
    });

    return data;
  };

  const getTypeColor = (type: string) => {
    const colors: { [key: string]: string } = {
      work: '#3B82F6',
      study: '#10B981',
      exercise: '#EF4444',
      leisure: '#F59E0B',
      other: '#6B7280'
    };
    return colors[type] || colors.other;
  };

  if (loading) {
    return (
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="h-6 bg-gray-200 rounded w-1/4 mb-4"></div>
        <div className="h-64 bg-gray-200 rounded"></div>
      </div>
    );
  }

  const categoryTotals = {
    work: chartData.reduce((sum, day) => sum + day.work, 0),
    study: chartData.reduce((sum, day) => sum + day.study, 0),
    exercise: chartData.reduce((sum, day) => sum + day.exercise, 0),
    leisure: chartData.reduce((sum, day) => sum + day.leisure, 0),
    other: chartData.reduce((sum, day) => sum + day.other, 0)
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold">Atividades por Dia</h3>
        
        <div className="flex space-x-2">
          {[7, 14, 30].map((days) => (
            <button
              key={days}
              onClick={() => setTimeRange(days)}
              className={`px-3 py-1 text-sm rounded-md ${
                timeRange === days 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {days}d
            </button>
          ))}
        </div>
      </div>

      <div className="h-72 mb-6">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey="dateFormatted" stroke="#6B7280" fontSize={12} />
            <YAxis stroke="#6B7280" fontSize={12} />
            <Tooltip formatter={(value) => [`${value} min`, 'Duração']} />
            <Legend />
            <Bar dataKey="work" name="Trabalho" fill={getTypeColor('work')} />
            <Bar dataKey="study" name="Estudo" fill={getTypeColor('study')} />
            <Bar dataKey="exercise" name="Exercício" fill={getTypeColor('exercise')} />
            <Bar dataKey="leisure" name="Lazer" fill={getTypeColor('leisure')} />
            <Bar dataKey="other" name="Outro" fill={getTypeColor('other')} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        {Object.entries(categoryTotals).map(([type, total]) => (
          total > 0 && (
            <div key={type} className="text-center p-3 rounded-lg" style={{ backgroundColor: `${getTypeColor(type)}20` }}>
              <div className="text-sm font-medium">
                {type === 'work' ? 'Trabalho' : 
                 type === 'study' ? 'Estudo' : 
                 type === 'exercise' ? 'Exercício' : 
                 type === 'leisure' ? 'Lazer' : 'Outro'}
              </div>
              <div className="text-xl font-bold" style={{ color: getTypeColor(type) }}>
                {Math.round(total / 60)}h {total % 60}min
              </div>
            </div>
          )
        ))}
      </div>
    </div>
  );
}
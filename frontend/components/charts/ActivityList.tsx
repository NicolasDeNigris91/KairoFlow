'use client';

import { useEffect, useState } from 'react';
import api from '@/lib/api';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';

interface Activity {
  id: number;
  title: string;
  activity_type: string;
  duration_minutes: number;
  description: string;
  date: string;
}

interface ActivityListProps {
  onActivityDeleted?: () => void;
  refreshKey?: number;
}

export default function ActivityList({ onActivityDeleted, refreshKey }: ActivityListProps) {
  const [activities, setActivities] = useState<Activity[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    console.log('🔄 ActivityList atualizando, refreshKey:', refreshKey);
    fetchActivities();
  }, [refreshKey]);

  const fetchActivities = async () => {
    try {
      const response = await api.get('/activities/');
      console.log('✅ API Response atividades:', {
        status: response.status,
        count: response.data.length
      });
      
      const sortedActivities = response.data.sort((a: Activity, b: Activity) => 
        new Date(b.date).getTime() - new Date(a.date).getTime()
      );
      
      setActivities(sortedActivities);
    } catch (error: any) {
      console.error('❌ Erro ao buscar atividades:', error.message);
    } finally {
      setLoading(false);
    }
  };

  const deleteActivity = async (id: number) => {
    if (!confirm('Tem certeza que deseja excluir esta atividade?')) return;
    
    try {
      await api.delete(`/activities/${id}/`);
      setActivities(activities.filter(activity => activity.id !== id));
      
      if (onActivityDeleted) {
        console.log('🔄 Chamando onActivityDeleted');
        onActivityDeleted();
      }
      
      alert('Atividade excluída com sucesso!');
    } catch (error: any) {
      console.error('❌ Erro ao excluir atividade:', error.message);
      alert('Erro ao excluir atividade');
    }
  };

  const getTypeColor = (type: string) => {
    const colors: { [key: string]: string } = {
      work: 'bg-blue-100 text-blue-800',
      study: 'bg-green-100 text-green-800',
      exercise: 'bg-red-100 text-red-800',
      leisure: 'bg-yellow-100 text-yellow-800',
      other: 'bg-gray-100 text-gray-800'
    };
    return colors[type] || colors.other;
  };

  const getTypeLabel = (type: string) => {
    const labels: { [key: string]: string } = {
      work: 'Trabalho',
      study: 'Estudo',
      exercise: 'Exercício',
      leisure: 'Lazer',
      other: 'Outro'
    };
    return labels[type] || type;
  };

  if (loading) {
    return (
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="h-6 bg-gray-200 rounded w-1/4 mb-4"></div>
        <div className="space-y-3">
          <div className="h-4 bg-gray-200 rounded"></div>
          <div className="h-4 bg-gray-200 rounded"></div>
          <div className="h-4 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-4">
        Suas Atividades Recentes ({activities.length})
      </h3>
      
      {activities.length === 0 ? (
        <p className="text-gray-500 text-center py-8">
          Nenhuma atividade registrada.
        </p>
      ) : (
        <div className="space-y-4">
          {activities.map((activity) => (
            <div key={activity.id} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50">
              <div className="flex justify-between items-start">
                <div>
                  <h4 className="font-medium text-gray-900">{activity.title}</h4>
                  <p className="text-sm text-gray-600 mt-1">{activity.description}</p>
                  
                  <div className="flex items-center space-x-4 mt-3">
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${getTypeColor(activity.activity_type)}`}>
                      {getTypeLabel(activity.activity_type)}
                    </span>
                    <span className="text-sm text-gray-500">
                      ⏱️ {activity.duration_minutes} minutos
                    </span>
                    <span className="text-sm text-gray-500">
                      📅 {format(new Date(activity.date), "dd/MM/yyyy HH:mm", { locale: ptBR })}
                    </span>
                  </div>
                </div>
                
                <button
                  onClick={() => deleteActivity(activity.id)}
                  className="text-red-600 hover:text-red-800 text-sm font-medium px-3 py-1 border border-red-300 rounded hover:bg-red-50 transition-colors"
                >
                  Excluir
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
'use client';

import { useState } from 'react';
import api from '@/lib/api';

interface ActivityFormData {
  title: string;
  activity_type: string;
  duration_minutes: number;
  description: string;
}

interface ActivityFormProps {
  onActivityCreated?: () => void;
}

export default function ActivityForm({ onActivityCreated }: ActivityFormProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState<ActivityFormData>({
    title: '',
    activity_type: 'WORK', 
    duration_minutes: 30,
    description: ''
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      const atividadeParaEnviar = {
        title: formData.title,
        activity_type: formData.activity_type, 
        duration_minutes: formData.duration_minutes,
        description: formData.description,
        tags: [],
        date: new Date().toISOString()
      };
      
      await api.post('/activities', atividadeParaEnviar);
      alert('Atividade criada com sucesso!');
      setFormData({
        title: '',
        activity_type: 'WORK', 
        duration_minutes: 30,
        description: ''
      });
      
      if (onActivityCreated) {
        onActivityCreated();
      }
    } catch (error: any) {
      console.error('Erro detalhado ao criar atividade:', error);
      
      if (error.response?.data?.detail) {
        alert(`Erro: ${error.response.data.detail}`);
      } else if (error.message) {
        alert(`Erro: ${error.message}`);
      } else {
        alert('Erro ao criar atividade');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-4">Adicionar Nova Atividade</h3>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Título</label>
          <input
            type="text"
            required
            value={formData.title}
            onChange={(e) => setFormData({...formData, title: e.target.value})}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            placeholder="Ex: Estudar Python"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Tipo</label>
          <select
            value={formData.activity_type}
            onChange={(e) => setFormData({...formData, activity_type: e.target.value})}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="WORK">Trabalho</option>
            <option value="STUDY">Estudo</option>
            <option value="EXERCISE">Exercício</option>
            <option value="LEISURE">Lazer</option>
            <option value="OTHER">Outro</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">
            Duração (minutos)
          </label>
          <input
            type="number"
            min="1"
            max="1440"
            value={formData.duration_minutes}
            onChange={(e) => setFormData({...formData, duration_minutes: parseInt(e.target.value)})}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Descrição (opcional)</label>
          <textarea
            value={formData.description}
            onChange={(e) => setFormData({...formData, description: e.target.value})}
            rows={3}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            placeholder="Detalhes da atividade..."
          />
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className={`w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white ${isLoading ? 'bg-blue-400' : 'bg-blue-600 hover:bg-blue-700'} focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500`}
        >
          {isLoading ? 'Adicionando...' : 'Adicionar Atividade'}
        </button>
      </form>
    </div>
  );
}
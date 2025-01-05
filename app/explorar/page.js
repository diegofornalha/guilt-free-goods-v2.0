"use client";

import Image from "next/image";
import Link from "next/link";
import { useEffect, useState } from "react";

export default function ExplorarPage() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    categoria: "",
    precoMin: "",
    precoMax: "",
    condicao: "",
  });

  useEffect(() => {
    fetchItems();
  }, [filters]);

  const fetchItems = async () => {
    try {
      const queryParams = new URLSearchParams();
      if (filters.categoria) queryParams.append("categoria", filters.categoria);
      if (filters.precoMin) queryParams.append("preco_min", filters.precoMin);
      if (filters.precoMax) queryParams.append("preco_max", filters.precoMax);
      if (filters.condicao) queryParams.append("condicao", filters.condicao);

      const response = await fetch(
        `http://localhost:8000/api/items?${queryParams}`
      );
      const data = await response.json();
      setItems(data);
      setLoading(false);
    } catch (error) {
      console.error("Erro ao carregar itens:", error);
      setLoading(false);
    }
  };

  return (
    <main className="pt-24 min-h-screen bg-gradient-to-br from-gray-50 to-white">
      <div className="container mx-auto px-6">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4">
            Explore Nossa{" "}
            <span className="bg-gradient-to-r from-teal-600 to-teal-500 text-transparent bg-clip-text">
              Coleção Sustentável
            </span>
          </h1>
          <p className="text-gray-600 text-lg max-w-2xl mx-auto">
            Descubra peças únicas e dê uma nova vida à moda, contribuindo para
            um futuro mais sustentável.
          </p>
        </div>

        {/* Filtros */}
        <div className="bg-white rounded-2xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] p-8 mb-12">
          <h2 className="text-2xl font-bold mb-8">Filtros de Busca</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Categoria
              </label>
              <select
                className="input"
                value={filters.categoria}
                onChange={(e) =>
                  setFilters({ ...filters, categoria: e.target.value })
                }
              >
                <option value="">Todas as Categorias</option>
                <option value="roupas">Roupas</option>
                <option value="acessorios">Acessórios</option>
                <option value="calcados">Calçados</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Preço Mínimo
              </label>
              <input
                type="number"
                className="input"
                value={filters.precoMin}
                onChange={(e) =>
                  setFilters({ ...filters, precoMin: e.target.value })
                }
                placeholder="R$ 0,00"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Preço Máximo
              </label>
              <input
                type="number"
                className="input"
                value={filters.precoMax}
                onChange={(e) =>
                  setFilters({ ...filters, precoMax: e.target.value })
                }
                placeholder="R$ 1000,00"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Condição
              </label>
              <select
                className="input"
                value={filters.condicao}
                onChange={(e) =>
                  setFilters({ ...filters, condicao: e.target.value })
                }
              >
                <option value="">Todas as Condições</option>
                <option value="novo">Novo</option>
                <option value="excelente">Excelente</option>
                <option value="bom">Bom</option>
                <option value="usado">Usado</option>
              </select>
            </div>
          </div>
        </div>

        {/* Lista de Produtos */}
        {loading ? (
          <div className="text-center py-20">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-teal-500 mx-auto"></div>
            <p className="mt-6 text-gray-600 text-lg">
              Buscando produtos incríveis...
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {items.map((item) => (
              <Link
                href={`/produto/${item.id}`}
                key={item.id}
                className="group"
              >
                <div className="card">
                  <div className="relative h-80">
                    <Image
                      src={item.imageUrls[0] || "/placeholder.jpg"}
                      alt={item.title}
                      fill
                      className="object-cover group-hover:scale-105 transition-transform duration-500"
                    />
                    {item.condition && (
                      <span className="absolute top-4 right-4 bg-white/90 backdrop-blur-md px-3 py-1.5 rounded-full text-sm font-medium">
                        {item.condition}
                      </span>
                    )}
                  </div>
                  <div className="p-6">
                    <h3 className="font-semibold text-lg mb-2 group-hover:text-teal-600 transition-colors">
                      {item.title}
                    </h3>
                    <p className="text-gray-600 text-sm mb-4">
                      {item.brand} • {item.detectedCategory}
                    </p>
                    <div className="flex items-center justify-between">
                      <span className="text-xl font-bold bg-gradient-to-r from-teal-600 to-teal-500 text-transparent bg-clip-text">
                        R$ {parseFloat(item.price).toFixed(2)}
                      </span>
                      <button className="btn-primary text-sm">
                        Ver Detalhes
                      </button>
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}

        {!loading && items.length === 0 && (
          <div className="text-center py-20">
            <div className="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <span className="text-4xl">🔍</span>
            </div>
            <h3 className="text-2xl font-bold mb-4">
              Nenhum produto encontrado
            </h3>
            <p className="text-gray-600 text-lg max-w-md mx-auto">
              Tente ajustar os filtros ou volte mais tarde para ver novos
              produtos.
            </p>
          </div>
        )}
      </div>
    </main>
  );
}

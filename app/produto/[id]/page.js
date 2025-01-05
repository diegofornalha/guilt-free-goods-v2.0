"use client";

import Image from "next/image";
import Link from "next/link";
import { useEffect, useState } from "react";

export default function ProdutoPage({ params }) {
  const [item, setItem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [currentImage, setCurrentImage] = useState(0);

  useEffect(() => {
    fetchItem();
  }, [params.id]);

  const fetchItem = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/items/${params.id}`
      );
      const data = await response.json();
      setItem(data);
      setLoading(false);
    } catch (error) {
      console.error("Erro ao carregar produto:", error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <main className="pt-20 min-h-screen">
        <div className="container mx-auto px-4">
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-teal-500 mx-auto"></div>
            <p className="mt-4 text-gray-600">Carregando produto...</p>
          </div>
        </div>
      </main>
    );
  }

  if (!item) {
    return (
      <main className="pt-20 min-h-screen">
        <div className="container mx-auto px-4">
          <div className="text-center py-12">
            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">😕</span>
            </div>
            <h2 className="text-2xl font-bold mb-2">Produto não encontrado</h2>
            <p className="text-gray-600 mb-6">
              O produto que você está procurando não existe ou foi removido.
            </p>
            <Link href="/explorar" className="btn-primary">
              Voltar para Explorar
            </Link>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="pt-20 min-h-screen">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Galeria de Imagens */}
          <div>
            <div className="relative h-[500px] rounded-lg overflow-hidden mb-4">
              <Image
                src={item.imageUrls[currentImage] || "/placeholder.jpg"}
                alt={item.title}
                fill
                className="object-cover"
              />
            </div>
            {item.imageUrls.length > 1 && (
              <div className="grid grid-cols-4 gap-4">
                {item.imageUrls.map((url, index) => (
                  <button
                    key={index}
                    className={`relative h-24 rounded-lg overflow-hidden ${
                      currentImage === index ? "ring-2 ring-teal-500" : ""
                    }`}
                    onClick={() => setCurrentImage(index)}
                  >
                    <Image
                      src={url}
                      alt={`${item.title} - Imagem ${index + 1}`}
                      fill
                      className="object-cover"
                    />
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Informações do Produto */}
          <div>
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h1 className="text-3xl font-bold mb-2">{item.title}</h1>
              <div className="flex items-center gap-2 text-gray-600 mb-4">
                <span>{item.brand}</span>
                {item.model && (
                  <>
                    <span>•</span>
                    <span>{item.model}</span>
                  </>
                )}
              </div>
              <div className="text-3xl font-bold text-teal-600 mb-6">
                R$ {parseFloat(item.price).toFixed(2)}
              </div>

              <div className="space-y-4 mb-8">
                <div>
                  <h3 className="font-semibold mb-2">Condição</h3>
                  <span className="inline-block bg-gray-100 px-3 py-1 rounded-full">
                    {item.condition}
                  </span>
                </div>

                <div>
                  <h3 className="font-semibold mb-2">Descrição</h3>
                  <p className="text-gray-600">{item.description}</p>
                </div>

                {item.dimensions && (
                  <div>
                    <h3 className="font-semibold mb-2">Dimensões</h3>
                    <pre className="text-sm text-gray-600 bg-gray-50 p-3 rounded">
                      {JSON.stringify(item.dimensions, null, 2)}
                    </pre>
                  </div>
                )}
              </div>

              <div className="space-y-4">
                <button className="w-full btn-primary text-lg">
                  Comprar Agora
                </button>
                <button className="w-full btn-secondary text-lg">
                  Adicionar ao Carrinho
                </button>
              </div>

              {/* Informações do Vendedor */}
              <div className="mt-8 pt-8 border-t">
                <h3 className="font-semibold mb-4">Informações do Vendedor</h3>
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-gray-200 rounded-full flex items-center justify-center">
                    <span className="text-xl">👤</span>
                  </div>
                  <div>
                    <p className="font-medium">
                      {item.user?.name || "Vendedor"}
                    </p>
                    <p className="text-sm text-gray-600">
                      Membro desde{" "}
                      {new Date(item.user?.createdAt).getFullYear()}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}

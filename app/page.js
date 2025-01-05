import Image from "next/image";
import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen">
      {/* Header/Nav */}
      <nav className="fixed top-0 w-full bg-white/80 backdrop-blur-md z-50 border-b border-gray-100">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <Link
              href="/"
              className="text-2xl font-bold bg-gradient-to-r from-teal-600 to-teal-500 text-transparent bg-clip-text"
            >
              Guilt-Free Goods
            </Link>
            <div className="flex items-center gap-8">
              <Link href="/explorar" className="nav-link">
                Explorar
              </Link>
              <Link href="/vender" className="nav-link">
                Vender
              </Link>
              <Link href="/sobre" className="nav-link">
                Sobre
              </Link>
              <button className="btn-primary">Entrar</button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="hero-section pt-32 pb-20 px-6">
        <div className="container mx-auto max-w-6xl">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-16 items-center">
            <div className="relative z-10">
              <div className="absolute -top-20 -left-20 w-64 h-64 bg-teal-50 rounded-full filter blur-3xl opacity-60"></div>
              <h1 className="text-6xl font-bold mb-8 leading-tight">
                Moda Sustentável para um{" "}
                <span className="bg-gradient-to-r from-teal-600 to-teal-500 text-transparent bg-clip-text">
                  Futuro Consciente
                </span>
              </h1>
              <p className="text-xl text-gray-600 mb-10 leading-relaxed">
                Compre e venda roupas de segunda mão com estilo. Faça parte da
                revolução da moda circular.
              </p>
              <div className="flex gap-4">
                <button className="btn-primary">Começar a Vender</button>
                <button className="btn-secondary">Explorar Produtos</button>
              </div>
            </div>
            <div className="relative">
              <div className="absolute -top-10 -right-10 w-72 h-72 bg-teal-50 rounded-full filter blur-3xl opacity-60"></div>
              <div className="relative h-[600px] rounded-3xl overflow-hidden shadow-2xl">
                <Image
                  src="/hero-image.jpg"
                  alt="Moda Sustentável"
                  fill
                  className="object-cover"
                  priority
                />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 px-6">
        <div className="container mx-auto max-w-6xl">
          <h2 className="text-4xl font-bold text-center mb-16">
            Por que escolher o{" "}
            <span className="bg-gradient-to-r from-teal-600 to-teal-500 text-transparent bg-clip-text">
              Guilt-Free Goods
            </span>
            ?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="feature-card">
              <div className="feature-icon">
                <span>🌱</span>
              </div>
              <h3 className="text-xl font-semibold mb-4">Sustentabilidade</h3>
              <p className="text-gray-600 leading-relaxed">
                Contribua para um planeta mais saudável através da moda
                circular.
              </p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">
                <span>💎</span>
              </div>
              <h3 className="text-xl font-semibold mb-4">Qualidade</h3>
              <p className="text-gray-600 leading-relaxed">
                Peças verificadas e avaliadas pela nossa equipe especializada.
              </p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">
                <span>🎯</span>
              </div>
              <h3 className="text-xl font-semibold mb-4">Preços Justos</h3>
              <p className="text-gray-600 leading-relaxed">
                Economia para você e valorização para quem vende.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 px-6 bg-gradient-to-br from-teal-50 to-white">
        <div className="container mx-auto max-w-4xl text-center">
          <h2 className="text-4xl font-bold mb-6">
            Pronto para fazer parte da mudança?
          </h2>
          <p className="text-xl text-gray-600 mb-10 max-w-2xl mx-auto leading-relaxed">
            Junte-se a milhares de pessoas que já estão fazendo a diferença
            através da moda consciente.
          </p>
          <button className="btn-primary text-lg px-10 py-4">
            Criar Conta Grátis
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-20">
        <div className="container mx-auto px-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-12">
            <div>
              <h4 className="text-xl font-bold mb-6 bg-gradient-to-r from-teal-400 to-teal-300 text-transparent bg-clip-text">
                Guilt-Free Goods
              </h4>
              <p className="text-gray-400 leading-relaxed">
                Sua plataforma de moda circular e sustentável
              </p>
            </div>
            <div>
              <h4 className="text-lg font-semibold mb-6">Links Rápidos</h4>
              <ul className="space-y-4">
                <li>
                  <Link
                    href="/explorar"
                    className="text-gray-400 hover:text-white transition-colors"
                  >
                    Explorar
                  </Link>
                </li>
                <li>
                  <Link
                    href="/vender"
                    className="text-gray-400 hover:text-white transition-colors"
                  >
                    Vender
                  </Link>
                </li>
                <li>
                  <Link
                    href="/sobre"
                    className="text-gray-400 hover:text-white transition-colors"
                  >
                    Sobre
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="text-lg font-semibold mb-6">Suporte</h4>
              <ul className="space-y-4">
                <li>
                  <Link
                    href="/ajuda"
                    className="text-gray-400 hover:text-white transition-colors"
                  >
                    Central de Ajuda
                  </Link>
                </li>
                <li>
                  <Link
                    href="/contato"
                    className="text-gray-400 hover:text-white transition-colors"
                  >
                    Contato
                  </Link>
                </li>
                <li>
                  <Link
                    href="/faq"
                    className="text-gray-400 hover:text-white transition-colors"
                  >
                    FAQ
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="text-lg font-semibold mb-6">Newsletter</h4>
              <p className="text-gray-400 mb-6 leading-relaxed">
                Receba novidades e dicas de sustentabilidade
              </p>
              <div className="space-y-4">
                <input
                  type="email"
                  placeholder="Seu e-mail"
                  className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:ring-2 focus:ring-teal-400 focus:border-transparent"
                />
                <button className="w-full btn-primary">Inscrever</button>
              </div>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-16 pt-8 text-center text-gray-400">
            <p>© 2024 Guilt-Free Goods. Todos os direitos reservados.</p>
          </div>
        </div>
      </footer>
    </main>
  );
}

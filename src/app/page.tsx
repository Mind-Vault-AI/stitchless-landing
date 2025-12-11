"use client";

import { useState } from "react";
import Logo from "@/components/Logo";
import LogoIcon from "@/components/LogoIcon";

export default function Home() {
  const [email, setEmail] = useState("");
  const [segment, setSegment] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1000));

    console.log("Pre-order:", { email, segment });
    setSubmitted(true);
    setLoading(false);
  };

  return (
    <main className="min-h-screen bg-white">
      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-white/90 backdrop-blur-sm z-50 border-b border-gray-100">
        <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
          <Logo size="small" />
          <a
            href="#preorder"
            className="bg-accent text-white px-6 py-2 rounded-full font-semibold hover:bg-orange-600 transition"
          >
            Pre-order
          </a>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 bg-gradient-to-b from-blue-50 to-white">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-block bg-secondary/10 text-secondary px-4 py-2 rounded-full text-sm font-semibold mb-6">
            Revolutionaire wondverzorging
          </div>
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6 leading-tight">
            Hechten zonder naalden.
            <span className="text-primary"> Zonder pijn.</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            STITCHLESS™ is de slimme oplossing voor kleine wonden.
            Geen ziekenhuisbezoek nodig. Direct thuis toepassen.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="#preorder"
              className="bg-accent text-white px-8 py-4 rounded-full font-bold text-lg hover:bg-orange-600 transition shadow-lg hover:shadow-xl"
            >
              Pre-order Nu - €29,99
            </a>
            <a
              href="#voordelen"
              className="border-2 border-gray-300 text-gray-700 px-8 py-4 rounded-full font-semibold hover:border-primary hover:text-primary transition"
            >
              Meer informatie
            </a>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="voordelen" className="py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-4">
            Waarom STITCHLESS™?
          </h2>
          <p className="text-gray-600 text-center mb-12 max-w-2xl mx-auto">
            Ontworpen met 99,9% kwaliteitsgarantie. Steriel, veilig en eenvoudig.
          </p>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: "⚡",
                title: "Snel & Simpel",
                desc: "Binnen 2 minuten aangebracht. Geen medische kennis vereist.",
              },
              {
                icon: "🛡️",
                title: "100% Steriel",
                desc: "Medische kwaliteit. Veilig voor het hele gezin.",
              },
              {
                icon: "💰",
                title: "Kostenbesparend",
                desc: "Geen spoedeisende hulp. Bespaar tijd en geld.",
              },
              {
                icon: "🎯",
                title: "Poka-Yoke Design",
                desc: "Foutbestendig ontwerp. Kan niet verkeerd toegepast worden.",
              },
              {
                icon: "📦",
                title: "Compact",
                desc: "Past in elke EHBO-kit, tas of dashboardkastje.",
              },
              {
                icon: "✅",
                title: "Getest & Bewezen",
                desc: "Uitgebreide QC-tests voor maximale betrouwbaarheid.",
              },
            ].map((feature, i) => (
              <div
                key={i}
                className="bg-gray-50 p-6 rounded-2xl hover:shadow-lg transition"
              >
                <div className="text-4xl mb-4">{feature.icon}</div>
                <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Target Audiences */}
      <section className="py-20 px-4 bg-gray-50">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-4">
            Voor wie is STITCHLESS™?
          </h2>
          <p className="text-gray-600 text-center mb-12">
            Eén product, meerdere toepassingen
          </p>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                title: "Ouders",
                emoji: "👨‍👩‍👧‍👦",
                desc: "Kinderen vallen en stoten. Met STITCHLESS™ ben je altijd voorbereid.",
                color: "bg-blue-500",
              },
              {
                title: "Sporters",
                emoji: "🏃",
                desc: "Schaafwonden en sneetjes? Direct behandelen zonder de training te missen.",
                color: "bg-green-500",
              },
              {
                title: "Professionals",
                emoji: "👷",
                desc: "Op de bouwplaats of in de werkplaats. Snel en veilig verder werken.",
                color: "bg-orange-500",
              },
            ].map((audience, i) => (
              <div
                key={i}
                className="bg-white p-8 rounded-2xl shadow-sm hover:shadow-lg transition text-center"
              >
                <div className="text-6xl mb-4">{audience.emoji}</div>
                <h3 className="text-2xl font-bold mb-3">{audience.title}</h3>
                <p className="text-gray-600">{audience.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-12">
            Hoe werkt het?
          </h2>
          <div className="space-y-8">
            {[
              { step: "1", title: "Reinig de wond", desc: "Spoel de wond schoon met water" },
              { step: "2", title: "Open de kit", desc: "Haal de steriele STITCHLESS™ strip eruit" },
              { step: "3", title: "Breng aan", desc: "Druk de wondranden samen en plak de strip" },
              { step: "4", title: "Klaar!", desc: "De wond geneest veilig en snel" },
            ].map((item, i) => (
              <div key={i} className="flex items-start gap-6">
                <div className="w-12 h-12 bg-primary text-white rounded-full flex items-center justify-center font-bold text-xl flex-shrink-0">
                  {item.step}
                </div>
                <div>
                  <h3 className="text-xl font-bold mb-1">{item.title}</h3>
                  <p className="text-gray-600">{item.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pre-order Section */}
      <section id="preorder" className="py-20 px-4 bg-primary">
        <div className="max-w-xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
            Pre-order Nu
          </h2>
          <p className="text-blue-100 mb-8">
            Wees er als eerste bij. Ontvang 20% vroegboekkorting.
          </p>

          {!submitted ? (
            <form onSubmit={handleSubmit} className="space-y-4">
              <input
                type="email"
                required
                placeholder="Je e-mailadres"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-6 py-4 rounded-full text-lg focus:outline-none focus:ring-4 focus:ring-blue-300"
              />
              <select
                required
                value={segment}
                onChange={(e) => setSegment(e.target.value)}
                className="w-full px-6 py-4 rounded-full text-lg focus:outline-none focus:ring-4 focus:ring-blue-300 bg-white"
              >
                <option value="">Ik ben een...</option>
                <option value="ouder">Ouder</option>
                <option value="sporter">Sporter</option>
                <option value="professional">Professional (bouw/industrie)</option>
                <option value="anders">Anders</option>
              </select>
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-accent text-white px-8 py-4 rounded-full font-bold text-lg hover:bg-orange-600 transition disabled:opacity-50"
              >
                {loading ? "Bezig..." : "Schrijf me in voor pre-order"}
              </button>
              <p className="text-blue-200 text-sm">
                * Je gegevens worden veilig bewaard. Geen spam.
              </p>
            </form>
          ) : (
            <div className="bg-white/10 p-8 rounded-2xl">
              <div className="text-5xl mb-4">✅</div>
              <h3 className="text-2xl font-bold text-white mb-2">
                Bedankt voor je aanmelding!
              </h3>
              <p className="text-blue-100">
                We houden je op de hoogte zodra STITCHLESS™ beschikbaar is.
              </p>
            </div>
          )}
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-4 bg-gray-900 text-white">
        <div className="max-w-6xl mx-auto text-center">
          <div className="flex justify-center mb-4">
            <LogoIcon size={48} />
          </div>
          <div className="text-2xl font-bold mb-2">STITCHLESS™</div>
          <p className="text-gray-400 mb-6">
            Revolutionaire wondverzorging. Gemaakt in Nederland.
          </p>
          <div className="flex justify-center gap-6 text-gray-400 text-sm">
            <span>© 2024 STITCHLESS™</span>
            <span>|</span>
            <a href="#" className="hover:text-white">Privacy</a>
            <span>|</span>
            <a href="#" className="hover:text-white">Contact</a>
          </div>
        </div>
      </footer>
    </main>
  );
}

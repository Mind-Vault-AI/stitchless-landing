"use client";

export default function QRSection() {
  return (
    <section className="py-20 px-4 bg-gradient-to-b from-gray-50 to-white">
      <div className="max-w-6xl mx-auto">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          {/* Left: QR Code */}
          <div className="flex justify-center">
            <div className="bg-white p-8 rounded-3xl shadow-lg">
              {/* QR Code SVG */}
              <svg
                width="200"
                height="200"
                viewBox="0 0 200 200"
                className="mx-auto"
              >
                {/* QR Code pattern (simplified visual representation) */}
                <rect width="200" height="200" fill="white" />

                {/* Corner squares */}
                <rect x="10" y="10" width="50" height="50" fill="#0066CC" />
                <rect x="17" y="17" width="36" height="36" fill="white" />
                <rect x="24" y="24" width="22" height="22" fill="#0066CC" />

                <rect x="140" y="10" width="50" height="50" fill="#0066CC" />
                <rect x="147" y="17" width="36" height="36" fill="white" />
                <rect x="154" y="24" width="22" height="22" fill="#0066CC" />

                <rect x="10" y="140" width="50" height="50" fill="#0066CC" />
                <rect x="17" y="147" width="36" height="36" fill="white" />
                <rect x="24" y="154" width="22" height="22" fill="#0066CC" />

                {/* Data pattern (simplified) */}
                <rect x="70" y="10" width="10" height="10" fill="#0066CC" />
                <rect x="90" y="10" width="10" height="10" fill="#0066CC" />
                <rect x="110" y="10" width="10" height="10" fill="#0066CC" />
                <rect x="70" y="30" width="10" height="10" fill="#0066CC" />
                <rect x="110" y="30" width="10" height="10" fill="#0066CC" />
                <rect x="80" y="50" width="10" height="10" fill="#0066CC" />
                <rect x="100" y="50" width="10" height="10" fill="#0066CC" />

                <rect x="70" y="70" width="60" height="60" fill="none" stroke="#0066CC" strokeWidth="2" />
                <rect x="85" y="85" width="30" height="30" fill="#0066CC" />

                <rect x="10" y="70" width="10" height="10" fill="#0066CC" />
                <rect x="30" y="70" width="10" height="10" fill="#0066CC" />
                <rect x="10" y="90" width="10" height="10" fill="#0066CC" />
                <rect x="30" y="90" width="10" height="10" fill="#0066CC" />
                <rect x="50" y="90" width="10" height="10" fill="#0066CC" />
                <rect x="10" y="110" width="10" height="10" fill="#0066CC" />
                <rect x="40" y="110" width="10" height="10" fill="#0066CC" />

                <rect x="140" y="70" width="10" height="10" fill="#0066CC" />
                <rect x="160" y="70" width="10" height="10" fill="#0066CC" />
                <rect x="180" y="70" width="10" height="10" fill="#0066CC" />
                <rect x="150" y="90" width="10" height="10" fill="#0066CC" />
                <rect x="170" y="90" width="10" height="10" fill="#0066CC" />
                <rect x="140" y="110" width="10" height="10" fill="#0066CC" />
                <rect x="160" y="110" width="10" height="10" fill="#0066CC" />
                <rect x="180" y="110" width="10" height="10" fill="#0066CC" />

                <rect x="70" y="140" width="10" height="10" fill="#0066CC" />
                <rect x="90" y="140" width="10" height="10" fill="#0066CC" />
                <rect x="110" y="140" width="10" height="10" fill="#0066CC" />
                <rect x="80" y="160" width="10" height="10" fill="#0066CC" />
                <rect x="100" y="160" width="10" height="10" fill="#0066CC" />
                <rect x="70" y="180" width="10" height="10" fill="#0066CC" />
                <rect x="90" y="180" width="10" height="10" fill="#0066CC" />
                <rect x="110" y="180" width="10" height="10" fill="#0066CC" />

                <rect x="140" y="150" width="10" height="10" fill="#0066CC" />
                <rect x="160" y="150" width="10" height="10" fill="#0066CC" />
                <rect x="150" y="170" width="10" height="10" fill="#0066CC" />
                <rect x="180" y="170" width="10" height="10" fill="#0066CC" />
                <rect x="140" y="180" width="10" height="10" fill="#0066CC" />
                <rect x="170" y="180" width="20" height="10" fill="#0066CC" />
              </svg>
              <p className="text-center text-gray-500 mt-4 text-sm">
                Scan voor instructievideo
              </p>
            </div>
          </div>

          {/* Right: Content */}
          <div>
            <div className="inline-block bg-primary/10 text-primary px-4 py-2 rounded-full text-sm font-semibold mb-4">
              Nieuw: Smart Instructies
            </div>
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Geen ziekenhuis nodig.
              <span className="text-primary"> Scan & leer.</span>
            </h2>
            <p className="text-gray-600 mb-6 text-lg">
              Elke STITCHLESS™ kit bevat een QR-code die je direct naar een
              stapsgewijze instructievideo brengt. Zo weet je precies wat je moet
              doen, ook in stressvolle situaties.
            </p>

            <div className="space-y-4">
              {[
                { icon: "📱", text: "Scan met je telefoon" },
                { icon: "🎬", text: "Bekijk de video-instructie" },
                { icon: "✅", text: "Volg de stappen" },
              ].map((item, i) => (
                <div key={i} className="flex items-center gap-4">
                  <div className="text-2xl">{item.icon}</div>
                  <span className="text-gray-700 font-medium">{item.text}</span>
                </div>
              ))}
            </div>

            <div className="mt-8 p-4 bg-green-50 rounded-xl border border-green-200">
              <p className="text-green-800 font-medium">
                💡 44% van Nederlandse huishoudens heeft een EHBO-kit, maar weet
                niet hoe ze deze moeten gebruiken. STITCHLESS™ lost dat op.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

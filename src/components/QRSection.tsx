"use client";

import { useState } from "react";

export default function QRSection() {
  const [activeTab, setActiveTab] = useState<"qr" | "barcode">("qr");

  return (
    <section className="py-20 px-4 bg-gradient-to-b from-gray-50 to-white">
      <div className="max-w-6xl mx-auto">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          {/* Left: Scan Codes */}
          <div className="flex flex-col items-center">
            {/* Toggle Tabs */}
            <div className="flex bg-gray-100 rounded-full p-1 mb-6">
              <button
                onClick={() => setActiveTab("qr")}
                className={`px-6 py-2 rounded-full text-sm font-semibold transition ${
                  activeTab === "qr"
                    ? "bg-primary text-white"
                    : "text-gray-600 hover:text-gray-900"
                }`}
              >
                QR Code
              </button>
              <button
                onClick={() => setActiveTab("barcode")}
                className={`px-6 py-2 rounded-full text-sm font-semibold transition ${
                  activeTab === "barcode"
                    ? "bg-primary text-white"
                    : "text-gray-600 hover:text-gray-900"
                }`}
              >
                Barcode
              </button>
            </div>

            <div className="bg-white p-8 rounded-3xl shadow-lg">
              {activeTab === "qr" ? (
                /* QR Code SVG */
                <svg
                  width="200"
                  height="200"
                  viewBox="0 0 200 200"
                  className="mx-auto"
                >
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
                  {/* Data pattern */}
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
                  <rect x="140" y="70" width="10" height="10" fill="#0066CC" />
                  <rect x="160" y="70" width="10" height="10" fill="#0066CC" />
                  <rect x="180" y="70" width="10" height="10" fill="#0066CC" />
                  <rect x="150" y="90" width="10" height="10" fill="#0066CC" />
                  <rect x="170" y="90" width="10" height="10" fill="#0066CC" />
                  <rect x="70" y="140" width="10" height="10" fill="#0066CC" />
                  <rect x="90" y="140" width="10" height="10" fill="#0066CC" />
                  <rect x="110" y="140" width="10" height="10" fill="#0066CC" />
                  <rect x="140" y="150" width="10" height="10" fill="#0066CC" />
                  <rect x="160" y="150" width="10" height="10" fill="#0066CC" />
                  <rect x="140" y="180" width="10" height="10" fill="#0066CC" />
                  <rect x="170" y="180" width="20" height="10" fill="#0066CC" />
                </svg>
              ) : (
                /* Barcode SVG - EAN-13 / Code 128 style */
                <svg
                  width="200"
                  height="120"
                  viewBox="0 0 200 120"
                  className="mx-auto"
                >
                  <rect width="200" height="120" fill="white" />
                  {/* Barcode lines - Code 128 pattern */}
                  <g fill="#0066CC">
                    {/* Start pattern */}
                    <rect x="10" y="10" width="2" height="80" />
                    <rect x="14" y="10" width="1" height="80" />
                    <rect x="17" y="10" width="3" height="80" />
                    <rect x="22" y="10" width="1" height="80" />
                    {/* Data bars */}
                    <rect x="26" y="10" width="2" height="80" />
                    <rect x="30" y="10" width="1" height="80" />
                    <rect x="33" y="10" width="4" height="80" />
                    <rect x="40" y="10" width="1" height="80" />
                    <rect x="43" y="10" width="2" height="80" />
                    <rect x="48" y="10" width="3" height="80" />
                    <rect x="54" y="10" width="1" height="80" />
                    <rect x="57" y="10" width="2" height="80" />
                    <rect x="62" y="10" width="1" height="80" />
                    <rect x="65" y="10" width="4" height="80" />
                    <rect x="72" y="10" width="2" height="80" />
                    <rect x="76" y="10" width="1" height="80" />
                    <rect x="80" y="10" width="3" height="80" />
                    <rect x="86" y="10" width="1" height="80" />
                    <rect x="89" y="10" width="2" height="80" />
                    <rect x="94" y="10" width="4" height="80" />
                    <rect x="100" y="10" width="1" height="80" />
                    <rect x="103" y="10" width="2" height="80" />
                    <rect x="108" y="10" width="1" height="80" />
                    <rect x="112" y="10" width="3" height="80" />
                    <rect x="118" y="10" width="2" height="80" />
                    <rect x="122" y="10" width="1" height="80" />
                    <rect x="126" y="10" width="4" height="80" />
                    <rect x="133" y="10" width="1" height="80" />
                    <rect x="136" y="10" width="2" height="80" />
                    <rect x="141" y="10" width="3" height="80" />
                    <rect x="147" y="10" width="1" height="80" />
                    <rect x="150" y="10" width="2" height="80" />
                    <rect x="155" y="10" width="1" height="80" />
                    <rect x="159" y="10" width="4" height="80" />
                    <rect x="166" y="10" width="2" height="80" />
                    {/* End pattern */}
                    <rect x="172" y="10" width="1" height="80" />
                    <rect x="175" y="10" width="3" height="80" />
                    <rect x="180" y="10" width="2" height="80" />
                    <rect x="184" y="10" width="1" height="80" />
                    <rect x="187" y="10" width="3" height="80" />
                  </g>
                  {/* Barcode number */}
                  <text
                    x="100"
                    y="108"
                    textAnchor="middle"
                    fontSize="12"
                    fontFamily="monospace"
                    fill="#333"
                  >
                    8 719326 000123
                  </text>
                </svg>
              )}
              <p className="text-center text-gray-500 mt-4 text-sm">
                {activeTab === "qr" ? "Smartphone camera" : "Industriële scanner"}
              </p>
            </div>

            {/* Compatibility info */}
            <div className="mt-6 text-center">
              <p className="text-sm text-gray-500 mb-2">Compatibel met:</p>
              <div className="flex flex-wrap justify-center gap-2">
                {activeTab === "qr" ? (
                  <>
                    <span className="px-3 py-1 bg-gray-100 rounded-full text-xs text-gray-600">iPhone</span>
                    <span className="px-3 py-1 bg-gray-100 rounded-full text-xs text-gray-600">Android</span>
                    <span className="px-3 py-1 bg-gray-100 rounded-full text-xs text-gray-600">Tablet</span>
                  </>
                ) : (
                  <>
                    <span className="px-3 py-1 bg-gray-100 rounded-full text-xs text-gray-600">Motorola</span>
                    <span className="px-3 py-1 bg-gray-100 rounded-full text-xs text-gray-600">Zebra</span>
                    <span className="px-3 py-1 bg-gray-100 rounded-full text-xs text-gray-600">Honeywell</span>
                    <span className="px-3 py-1 bg-gray-100 rounded-full text-xs text-gray-600">Datalogic</span>
                  </>
                )}
              </div>
            </div>
          </div>

          {/* Right: Content */}
          <div>
            <div className="inline-block bg-primary/10 text-primary px-4 py-2 rounded-full text-sm font-semibold mb-4">
              Universeel: QR + Barcode
            </div>
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Geen ziekenhuis nodig.
              <span className="text-primary"> Scan & leer.</span>
            </h2>
            <p className="text-gray-600 mb-6 text-lg">
              Elke STITCHLESS™ kit bevat <strong>beide</strong> codes: een QR-code
              voor smartphones én een barcode voor industriële scanners. Zo werkt
              het overal - thuis, op kantoor, of op de werkvloer.
            </p>

            <div className="space-y-4">
              {[
                { icon: "📱", text: "QR: Scan met smartphone camera" },
                { icon: "🔫", text: "Barcode: Werkt met handheld scanners" },
                { icon: "🎬", text: "Bekijk direct de video-instructie" },
                { icon: "✅", text: "Volg de stappen - foutloos" },
              ].map((item, i) => (
                <div key={i} className="flex items-center gap-4">
                  <div className="text-2xl">{item.icon}</div>
                  <span className="text-gray-700 font-medium">{item.text}</span>
                </div>
              ))}
            </div>

            <div className="mt-8 grid grid-cols-2 gap-4">
              <div className="p-4 bg-blue-50 rounded-xl border border-blue-200">
                <p className="text-blue-800 font-semibold text-sm">Consumenten</p>
                <p className="text-blue-600 text-xs mt-1">QR code met telefoon</p>
              </div>
              <div className="p-4 bg-orange-50 rounded-xl border border-orange-200">
                <p className="text-orange-800 font-semibold text-sm">B2B / Industrie</p>
                <p className="text-orange-600 text-xs mt-1">Barcode met scanner</p>
              </div>
            </div>

            <div className="mt-6 p-4 bg-green-50 rounded-xl border border-green-200">
              <p className="text-green-800 font-medium text-sm">
                💡 <strong>Thinking forward:</strong> Wij ondersteunen alle scanners -
                van de nieuwste smartphones tot Motorola material handling apparatuur.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

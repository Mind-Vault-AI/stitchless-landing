import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "STITCHLESS™ - Hechten zonder naalden",
  description: "Revolutionaire wondverzorging. Geen naalden, geen pijn, geen ziekenhuisbezoek. Pre-order nu!",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="nl">
      <body className="antialiased">{children}</body>
    </html>
  );
}

import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "OpenTerminal // AI-Powered Indian Economic Intelligence Platform",
  description: "A professional, high-density financial terminal focused on tracking and explaining the consequences of global market shifts on the Indian economy.",
  keywords: ["Bloomberg Terminal", "Nifty 50", "RBI policy", "Indian Economy", "Macroeconomics", "Forex", "AI Research Analyst"],
  authors: [{ name: "OpenTerminal Team" }]
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}>
      <body className="min-h-full flex flex-col bg-[#030712] text-[#f3f4f6]">
        {children}
      </body>
    </html>
  );
}

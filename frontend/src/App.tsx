import { useEffect, useState, useMemo } from "react";
import axios from "axios";

interface Listing {
  title: string;
  detail_url: string;
  price: number;
  year?: number;
  model?: string;
  slides?: number;
  converter?: string;
  featured_image?: string;
}

export default function App() {
  const [all, setAll] = useState<Listing[]>([]);
  const [query, setQuery] = useState("");
  const [sort, setSort] = useState<"price" | "year">("price");
  const [dir, setDir] = useState<"asc" | "desc">("desc");

  useEffect(() => {
    axios
      .get<Listing[]>(`http://localhost:8000/listings?sort=${sort}&dir=${dir}`)
      .then((r) => setAll(r.data))
      .catch(console.error);
  }, [sort, dir]);

  const visible = useMemo(() => {
    const q = query.trim().toLowerCase();
    return q
      ? all.filter(
          (l) =>
            l.title.toLowerCase().includes(q) ||
            l.model?.toLowerCase().includes(q) ||
            l.converter?.toLowerCase().includes(q)
        )
      : all;
  }, [all, query]);

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="px-6 py-4 max-w-5xl mx-auto">
        <h1 className="font-semibold text-2xl" style={{ color: "#2C3E50" }}>
          CoachRanger
        </h1>
        <div className="mt-4 flex flex-col sm:flex-row gap-3">
          <input
            type="search"
            placeholder="Search model, converter, etc."
            className="flex-1 bg-white/80 backdrop-blur px-4 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-[#2C3E50]/40"
            onChange={(e) => setQuery(e.target.value)}
            value={query}
          />
          <select
            value={sort}
            onChange={(e) => setSort(e.target.value as any)}
            className="bg-white/80 px-3 py-2 rounded-md"
          >
            <option value="price">Price</option>
            <option value="year">Year</option>
          </select>
          <button
            onClick={() => setDir(dir === "asc" ? "desc" : "asc")}
            className="bg-[#2C3E50] text-white px-4 py-2 rounded-md"
          >
            {dir === "asc" ? "↑" : "↓"}
          </button>
        </div>
      </header>
      <main className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 max-w-5xl mx-auto px-6 pb-12">
        {visible.map((l) => (
          <article
            key={l.detail_url}
            className="bg-white/70 backdrop-blur rounded-lg shadow-sm hover:shadow-md transition"
          >
            {l.featured_image && (
              <img
                src={l.featured_image}
                alt={l.title}
                className="w-full h-56 object-cover rounded-t-lg"
              />
            )}
            <div className="p-4">
              <h2 className="font-medium">{l.title}</h2>
              <p className="text-sm mt-1">
                ${l.price.toLocaleString()} {l.year && `• ${l.year}`}
              </p>
              {l.model && (
                <p className="text-xs text-slate-600 mt-1">
                  Model: {l.model}{" "}
                  {l.slides ? `• Slides: ${l.slides}` : ""}
                </p>
              )}
              <a
                href={l.detail_url}
                target="_blank"
                rel="noopener"
                className="inline-block mt-3 text-sm font-medium text-[#2C3E50]/80 hover:text-[#2C3E50]"
              >
                View on Prevost‑stuff →
              </a>
            </div>
          </article>
        ))}
      </main>
    </div>
  );
}
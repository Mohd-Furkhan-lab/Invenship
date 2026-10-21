import { useEffect, useMemo, useState } from "react";
import { api } from "../api/client";

// ---- Formatting ---------------------------------------------------------
// Change LOCALE / CURRENCY here if prices are not in rupees.
const LOCALE = "en-IN";
const CURRENCY = "INR";

const money = new Intl.NumberFormat(LOCALE, {
  style: "currency",
  currency: CURRENCY,
  minimumFractionDigits: 0,
  maximumFractionDigits: 2,
});
const count = new Intl.NumberFormat(LOCALE, { maximumFractionDigits: 2 });

const MONEY_KEY = /(revenue|cost|price|value|amount)/i;

// Backend field names that read badly when auto-formatted.
const LABELS = {
  pname: "Product",
  pid: "Product ID",
  suid: "Supplier ID",
  total_stock: "Units in stock",
  total_quantity: "Units",
  total_purchase_cost: "Total purchase cost",
};

function humanize(key) {
  if (LABELS[key]) return LABELS[key];
  const s = String(key).replace(/[_-]+/g, " ").replace(/([a-z])([A-Z])/g, "$1 $2").trim();
  return s.charAt(0).toUpperCase() + s.slice(1);
}

function formatCell(key, v) {
  if (v === null || v === undefined || v === "") return "—";
  if (typeof v === "number") return MONEY_KEY.test(key) ? money.format(v) : count.format(v);
  if (typeof v === "object") return JSON.stringify(v);
  return String(v);
}

const asArray = (v) => (Array.isArray(v) ? v : []);
const asObject = (v) => (v && typeof v === "object" && !Array.isArray(v) ? v : {});

// ---- Building blocks ----------------------------------------------------
function Stats({ data }) {
  const entries = Object.entries(asObject(data));
  if (entries.length === 0) return null;
  return (
    <div className="stat-grid">
      {entries.map(([k, v]) => (
        <div className="stat" key={k}>
          <span className="stat-label">{humanize(k)}</span>
          <span className="stat-value">{formatCell(k, v)}</span>
        </div>
      ))}
    </div>
  );
}

// Columns come from the data unless pinned, so sections that are empty today
// (sales, purchases) render correctly as soon as the backend returns rows.
function DataTable({ rows, columns, empty }) {
  const list = asArray(rows);
  if (list.length === 0) return <p className="empty-state">{empty}</p>;
  const cols = columns || [...new Set(list.flatMap((r) => Object.keys(asObject(r))))];
  return (
    <div className="table-scroll">
      <table>
        <thead>
          <tr>
            {cols.map((c) => (
              <th key={c}>{humanize(c)}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {list.map((r, i) => (
            <tr key={r.pid ?? r.suid ?? i}>
              {cols.map((c) => (
                <td key={c}>{formatCell(c, r[c])}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// Horizontal bars, scaled to the largest value in the list.
function BarList({ items, empty }) {
  if (items.length === 0) return <p className="empty-state">{empty}</p>;
  const max = Math.max(...items.map((i) => i.value), 1);
  return (
    <ul className="bar-list">
      {items.map((item) => (
        <li className="bar-row" key={item.label}>
          <span className="bar-label">{item.label}</span>
          <span className="bar-track" aria-hidden="true">
            <span className="bar-fill" style={{ width: `${(item.value / max) * 100}%` }} />
          </span>
          <span className="bar-value">{item.display}</span>
          {item.sub && <span className="bar-sub">{item.sub}</span>}
        </li>
      ))}
    </ul>
  );
}

function Block({ title, children }) {
  return (
    <section className="report-section">
      <h3>{title}</h3>
      {children}
    </section>
  );
}

// ---- Sections -----------------------------------------------------------
function InventoryView({ data }) {
  const d = asObject(data);
  const low = asArray(d.low_stock);
  const out = asArray(d.out_of_stock);

  const brands = asArray(d.by_brand)
    .map((b) => ({
      label: b.brand,
      value: Number(b.inventory_value) || 0,
      display: money.format(Number(b.inventory_value) || 0),
      sub: `${count.format(b.product_count ?? 0)} products, ${count.format(b.total_stock ?? 0)} units`,
    }))
    .sort((a, b) => b.value - a.value);

  const productCols = ["pname", "brand", "size", "price", "stock"];

  return (
    <div className="report">
      <Stats data={d.summary} />

      <Block title="Needs restocking">
        {low.length === 0 && out.length === 0 ? (
          <p className="empty-state">Every product is above the low-stock level.</p>
        ) : (
          <>
            {out.length > 0 && (
              <>
                <p className="hint">Out of stock ({out.length})</p>
                <DataTable rows={out} columns={productCols} />
              </>
            )}
            {low.length > 0 && (
              <>
                <p className="hint">Low stock ({low.length})</p>
                <DataTable rows={low} columns={productCols} />
              </>
            )}
          </>
        )}
      </Block>

      <Block title="Stock value by brand">
        <BarList items={brands} empty="No brand data yet." />
      </Block>

      <Block title="Highest priced products">
        <DataTable rows={d.most_expensive} columns={productCols} empty="No products yet." />
      </Block>
    </div>
  );
}

function SalesView({ data }) {
  const d = asObject(data);
  const noSales = asObject(d.summary).total_sales === 0;

  return (
    <div className="report">
      <Stats data={d.summary} />
      {noSales ? (
        <p className="empty-state">No sales yet. Rankings will appear after the first sale.</p>
      ) : (
        <>
          <Block title="Top selling products">
            <DataTable rows={d.top_selling_products} empty="Nothing to show." />
          </Block>
          <Block title="Top revenue products">
            <DataTable rows={d.top_revenue_products} empty="Nothing to show." />
          </Block>
          <Block title="By brand">
            <DataTable rows={d.by_brand} empty="Nothing to show." />
          </Block>
          <Block title="By size">
            <DataTable rows={d.by_size} empty="Nothing to show." />
          </Block>
          <Block title="By product">
            <DataTable rows={d.by_product} empty="Nothing to show." />
          </Block>
        </>
      )}
    </div>
  );
}

function PurchasesView({ data }) {
  const d = asObject(data);
  const nothing = asObject(d.summary).total_purchases === 0;

  return (
    <div className="report">
      <Stats data={d.summary} />
      {nothing ? (
        <p className="empty-state">No purchases yet. Rankings will appear after the first purchase.</p>
      ) : (
        <>
          <Block title="Most purchased products">
            <DataTable rows={d.top_purchased_products} empty="Nothing to show." />
          </Block>
          <Block title="By supplier">
            <DataTable rows={d.by_supplier} empty="Nothing to show." />
          </Block>
        </>
      )}
    </div>
  );
}

function SuppliersView({ data }) {
  const d = asObject(data);
  return (
    <div className="report">
      <Block title="Supplier summary">
        <DataTable
          rows={d.summary}
          columns={["name", "total_quantity", "total_purchase_cost"]}
          empty="No suppliers yet."
        />
      </Block>
    </div>
  );
}

const SECTIONS = [
  { id: "inventory", label: "Inventory", View: InventoryView },
  { id: "sales", label: "Sales", View: SalesView },
  { id: "purchases", label: "Purchases", View: PurchasesView },
  { id: "suppliers", label: "Suppliers", View: SuppliersView },
];

// Exported separately so it can be rendered with sample data.
export function ReportView({ report }) {
  const [section, setSection] = useState("inventory");
  const current = SECTIONS.find((s) => s.id === section) || SECTIONS[0];
  const { View } = current;

  const updated = useMemo(() => {
    const t = report?.generated_at ? new Date(report.generated_at) : null;
    return t && !Number.isNaN(t.getTime()) ? t.toLocaleString() : "";
  }, [report]);

  return (
    <>
      <div className="subtabs" role="tablist">
        {SECTIONS.map((s) => (
          <button
            key={s.id}
            role="tab"
            aria-selected={section === s.id}
            className={section === s.id ? "tab active" : "tab"}
            onClick={() => setSection(s.id)}
          >
            {s.label}
          </button>
        ))}
      </div>
      {updated && <p className="hint">Updated {updated}</p>}
      <View data={report?.[current.id]} />
    </>
  );
}

export default function AnalysisPanel() {
  const [report, setReport] = useState(undefined); // undefined = not loaded yet
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function load() {
    setLoading(true);
    setError("");
    try {
      setReport(await api.getReport());
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  return (
    <div className="panel">
      <div className="panel-header">
        <h2>Analysis</h2>
        <button className="ghost" onClick={load} disabled={loading}>
          {loading ? "Refreshing..." : "Refresh"}
        </button>
      </div>
      {error && <p className="error">{error}</p>}

      {loading && report === undefined && <p className="empty-state">Building your report...</p>}

      {/* Non-admins get a 200 with a null body from this endpoint. */}
      {!loading && !error && !report && (
        <p className="empty-state">No report is available for this account.</p>
      )}

      {report && <ReportView report={report} />}
    </div>
  );
}
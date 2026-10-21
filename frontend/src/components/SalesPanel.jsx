import { useEffect, useMemo, useState } from "react";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";

const emptyForm = { pid: "", quantity: "", price: "" };

export default function SalesPanel() {
  const { isAdmin } = useAuth();
  const [sales, setSales] = useState([]);
  const [products, setProducts] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function load() {
    try {
      const [s, p] = await Promise.all([api.getSales(), api.getProducts()]);
      setSales(s?.sales || []);
      setProducts(p?.products || []);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    load();
  }, []);

  const selected = useMemo(
    () => products.find((p) => p.pid === Number(form.pid)),
    [products, form.pid]
  );

  const quantity = parseInt(form.quantity, 10);
  const price = parseFloat(form.price);
  const total = Number.isFinite(quantity) && Number.isFinite(price) ? quantity * price : null;
  const overStock = selected && Number.isFinite(quantity) && quantity > selected.stock;

  function handleProductChange(pid) {
    const product = products.find((p) => p.pid === Number(pid));
    // Pre-fill the list price; the cashier can still change it.
    setForm((f) => ({ ...f, pid, price: product ? String(product.price) : "" }));
  }

  async function handleAdd(e) {
    e.preventDefault();
    setError("");
    if (!selected) {
      setError("Choose a product.");
      return;
    }
    if (overStock) {
      setError(`Only ${selected.stock} in stock for ${selected.pname}.`);
      return;
    }
    setBusy(true);
    try {
      await api.addSale({
        name: selected.pname,
        size: selected.size,
        quantity,
        price,
      });
      setForm(emptyForm);
      load();
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  async function handleClear() {
    if (!confirm("Clear all sales? This can't be undone.")) return;
    try {
      await api.clearSales();
      load();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="panel">
      <div className="panel-header">
        <h2>Sales</h2>
        {/* Clearing is admin-only on the backend (non-admins get a silent null). */}
        {isAdmin && (
          <button className="danger" onClick={handleClear} disabled={sales.length === 0}>
            Clear sales
          </button>
        )}
      </div>
      {error && <p className="error">{error}</p>}

      <form className="card form-grid" onSubmit={handleAdd}>
        <h3>Record sale</h3>
        <select value={form.pid} onChange={(e) => handleProductChange(e.target.value)} required>
          <option value="">Product</option>
          {products.map((p) => (
            <option key={p.pid} value={p.pid} disabled={p.stock <= 0}>
              {p.pname} ({p.size}) — {p.stock > 0 ? `${p.stock} in stock` : "out of stock"}
            </option>
          ))}
        </select>
        <input
          placeholder="Quantity"
          type="number"
          min="1"
          max={selected ? selected.stock : undefined}
          value={form.quantity}
          onChange={(e) => setForm((f) => ({ ...f, quantity: e.target.value }))}
          required
        />
        <input
          placeholder="Unit price"
          type="number"
          step="0.01"
          min="0"
          value={form.price}
          onChange={(e) => setForm((f) => ({ ...f, price: e.target.value }))}
          required
        />
        <span className="total-preview">{total !== null ? `Total ${total.toFixed(2)}` : ""}</span>
        <button type="submit" disabled={busy || overStock}>
          {busy ? "Saving..." : "Add sale"}
        </button>
      </form>

      {sales.length === 0 ? (
        <p className="empty-state">No sales recorded yet.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Product</th>
              <th>Size</th>
              <th>Qty</th>
              <th>Price</th>
              <th>Total</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {sales.map((s) => (
              <tr key={s.sid}>
                <td>{s.pname}</td>
                <td>{s.size}</td>
                <td>{s.quantity}</td>
                <td>{s.price}</td>
                <td>{s.total}</td>
                <td>{s.date ? new Date(s.date).toLocaleString() : ""}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      {sales.length >= 50 && <p className="hint">Showing the 50 most recent sales.</p>}
    </div>
  );
}
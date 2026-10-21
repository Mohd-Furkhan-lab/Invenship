import { useEffect, useMemo, useState } from "react";
import { api } from "../api/client";

const emptyForm = { pid: "", supplier: "", quantity: "", price: "" };

function toList(data) {
  return Array.isArray(data) ? data : data ? [data] : [];
}

export default function PurchasesPanel() {
  const [purchases, setPurchases] = useState([]);
  const [products, setProducts] = useState([]);
  const [suppliers, setSuppliers] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function load() {
    try {
      const [pu, pr, su] = await Promise.all([
        api.getPurchases(),
        api.getProducts(),
        api.getSuppliers(),
      ]);
      // Backend nests this as { puchases: { purchases: [...] } } (sic).
      setPurchases(pu?.puchases?.purchases || []);
      setProducts(pr?.products || []);
      setSuppliers(toList(su?.data));
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    load();
  }, []);

  // Purchase rows only carry ids, so resolve names client-side.
  const productById = useMemo(() => new Map(products.map((p) => [p.pid, p])), [products]);
  const supplierById = useMemo(() => new Map(suppliers.map((s) => [s.suid, s])), [suppliers]);

  function update(field, value) {
    setForm((f) => ({ ...f, [field]: value }));
  }

  async function handleAdd(e) {
    e.preventDefault();
    setError("");
    const product = productById.get(Number(form.pid));
    if (!product) {
      setError("Choose a product.");
      return;
    }
    setBusy(true);
    try {
      await api.addPurchase({
        name: product.pname,
        size: product.size,
        quantity: parseInt(form.quantity, 10),
        price: parseFloat(form.price),
        supplier: form.supplier,
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
    if (!confirm("Clear all purchase history?")) return;
    try {
      await api.clearPurchases();
      load();
    } catch (err) {
      setError(err.message);
    }
  }

  const sorted = useMemo(
    () => [...purchases].sort((a, b) => new Date(b.date || 0) - new Date(a.date || 0)),
    [purchases]
  );

  return (
    <div className="panel">
      <div className="panel-header">
        <h2>Purchases</h2>
        <button className="danger" onClick={handleClear} disabled={purchases.length === 0}>
          Clear history
        </button>
      </div>
      {error && <p className="error">{error}</p>}

      <form className="card form-grid" onSubmit={handleAdd}>
        <h3>Record purchase</h3>
        <select value={form.pid} onChange={(e) => update("pid", e.target.value)} required>
          <option value="">Product</option>
          {products.map((p) => (
            <option key={p.pid} value={p.pid}>
              {p.pname} ({p.size})
            </option>
          ))}
        </select>
        <select value={form.supplier} onChange={(e) => update("supplier", e.target.value)} required>
          <option value="">Supplier</option>
          {suppliers.map((s) => (
            <option key={s.suid} value={s.name}>
              {s.name}
            </option>
          ))}
        </select>
        <input
          placeholder="Quantity"
          type="number"
          min="1"
          value={form.quantity}
          onChange={(e) => update("quantity", e.target.value)}
          required
        />
        <input
          placeholder="Unit price"
          type="number"
          step="0.01"
          min="0"
          value={form.price}
          onChange={(e) => update("price", e.target.value)}
          required
        />
        <button type="submit" disabled={busy}>
          {busy ? "Saving..." : "Add purchase"}
        </button>
      </form>

      {sorted.length === 0 ? (
        <p className="empty-state">No purchases recorded yet.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Product</th>
              <th>Size</th>
              <th>Supplier</th>
              <th>Qty</th>
              <th>Price</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {sorted.map((p) => {
              const product = productById.get(p.pid);
              const supplier = supplierById.get(p.supplier);
              return (
                <tr key={p.puid}>
                  <td>{product?.pname ?? `#${p.pid}`}</td>
                  <td>{product?.size ?? "—"}</td>
                  <td>{supplier?.name ?? (p.supplier ? `#${p.supplier}` : "—")}</td>
                  <td>{p.quantity}</td>
                  <td>{p.price}</td>
                  <td>{p.date ? new Date(p.date).toLocaleDateString() : ""}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      )}
    </div>
  );
}
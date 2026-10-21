import { useEffect, useState } from "react";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";

const LOW_STOCK = 5; // rows at or below this get a "Low" badge
const emptyForm = { category: "", name: "", size: "", brand: "", price: "", stock: "" };

export default function ProductsPanel() {
  const { isAdmin } = useAuth();
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [query, setQuery] = useState("");

  async function load() {
    try {
      const p = await api.getProducts();
      setProducts(p.products || []);
      if (isAdmin) {
        const c = await api.getCategories();
        setCategories(c.categories || []);
      }
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    load();
  }, []);

  function update(field, value) {
    setForm((f) => ({ ...f, [field]: value }));
  }

  async function handleAdd(e) {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      let url = ""; // AddProduct.url is a required string; null would be rejected
      if (file) {
        url = await api.uploadProductImage(file);
      }
      // Stock is optional: if left blank it starts at 0 and goes up via purchases
      const parsedStock = parseInt(form.stock, 10);
      await api.addProduct({
        category: form.category,
        name: form.name,
        size: form.size,
        brand: form.brand,
        price: parseFloat(form.price),
        stock: Number.isNaN(parsedStock) ? 0 : parsedStock,
        url,
      });
      setForm(emptyForm);
      setFile(null);
      load();
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  async function handleUpdate(pname, price, stock) {
    try {
      await api.updateProduct(pname, {
        price: price !== "" ? parseFloat(price) : undefined,
        stock: stock !== "" ? parseInt(stock, 10) : undefined,
      });
      load();
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleDelete(pname) {
    if (!confirm(`Delete product "${pname}"?`)) return;
    try {
      await api.deleteProduct(pname);
      load();
    } catch (err) {
      setError(err.message);
    }
  }

  const q = query.trim().toLowerCase();
  const visible = q
    ? products.filter((p) =>
        [p.pname, p.brand, p.size].some((v) => String(v ?? "").toLowerCase().includes(q))
      )
    : products;

  return (
    <div className="panel">
      <h2>Products</h2>
      {error && <p className="error">{error}</p>}

      {isAdmin && (
      <form className="card form-grid" onSubmit={handleAdd}>
        <h3>Add product</h3>
        <select value={form.category} onChange={(e) => update("category", e.target.value)} required>
          <option value="">Category</option>
          {categories.map((c) => (
            <option key={c.cid} value={c.cname}>
              {c.cname}
            </option>
          ))}
        </select>
        <input placeholder="Name" value={form.name} onChange={(e) => update("name", e.target.value)} required />
        <input placeholder="Brand" value={form.brand} onChange={(e) => update("brand", e.target.value)} required />
        <input placeholder="Size" value={form.size} onChange={(e) => update("size", e.target.value)} required />
        <input
          placeholder="Price"
          type="number"
          step="0.01"
          value={form.price}
          onChange={(e) => update("price", e.target.value)}
          required
        />
        <input
          placeholder="Stock (optional)"
          type="number"
          min="0"
          value={form.stock}
          onChange={(e) => update("stock", e.target.value)}
        />
        <input type="file" accept="image/*" onChange={(e) => setFile(e.target.files[0])} />
        <button type="submit" disabled={busy}>
          {busy ? "Saving..." : "Add product"}
        </button>
      </form>
      )}

      <div className="inline-form">
        <input
          placeholder="Search name, brand or size"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          aria-label="Search products"
        />
      </div>

      {visible.length === 0 && (
        <p className="empty-state">
          {products.length === 0 ? "No products yet." : "No products match your search."}
        </p>
      )}

      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Brand</th>
            <th>Size</th>
            <th>Price</th>
            <th>Stock</th>
            <th>Image</th>
            {isAdmin && <th></th>}
          </tr>
        </thead>
        <tbody>
          {visible.map((p) => (
            <ProductRow
              key={`${p.pid}-${p.price}-${p.stock}`}
              product={p}
              isAdmin={isAdmin}
              onUpdate={handleUpdate}
              onDelete={handleDelete}
            />
          ))}
        </tbody>
      </table>
    </div>
  );
}

function ProductRow({ product, isAdmin, onUpdate, onDelete }) {
  const [price, setPrice] = useState(product.price);
  const [stock, setStock] = useState(product.stock);

  return (
    <tr>
      <td>{product.pname}</td>
      <td>{product.brand}</td>
      <td>{product.size}</td>
      <td>
        {isAdmin ? (
          <input type="number" step="0.01" value={price} onChange={(e) => setPrice(e.target.value)} />
        ) : (
          product.price
        )}
      </td>
      <td>
        {isAdmin ? (
          <input type="number" value={stock} onChange={(e) => setStock(e.target.value)} />
        ) : (
          product.stock
        )}
        {product.stock <= LOW_STOCK && (
          <span className="badge-low">{product.stock === 0 ? "Out" : "Low"}</span>
        )}
      </td>
      <td>{product.pimage ? <img src={product.pimage} alt="" className="thumb" /> : "—"}</td>
      {isAdmin && (
        <td className="row-actions">
          <button
            onClick={() => onUpdate(product.pname, price, stock)}
            disabled={String(price) === String(product.price) && String(stock) === String(product.stock)}
          >
            Save
          </button>
          <button className="danger" onClick={() => onDelete(product.pname)}>
            Delete
          </button>
        </td>
      )}
    </tr>
  );
}
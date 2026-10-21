import { useEffect, useState } from "react";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";

export default function SuppliersPanel() {
  const { isAdmin } = useAuth();
  const [suppliers, setSuppliers] = useState([]);
  const [form, setForm] = useState({ name: "", phno: "" });
  const [error, setError] = useState("");

  async function load() {
    try {
      const res = await api.getSuppliers();
      const data = res.data;
      setSuppliers(Array.isArray(data) ? data : data ? [data] : []);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    if (isAdmin) load();
  }, [isAdmin]);

  // Guard first: don't even attempt the fetch for a role the backend will
  // reject anyway — that's what produced the "Forbidden Admin only" flash.
  if (!isAdmin) {
    return (
      <div className="panel">
        <h2>Suppliers</h2>
        <p className="empty-state">This section is only available to admins.</p>
      </div>
    );
  }

  async function handleAdd(e) {
    e.preventDefault();
    setError("");
    try {
      await api.addSupplier(form);
      setForm({ name: "", phno: "" });
      load();
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleDelete(name) {
    if (!confirm(`Remove supplier "${name}"?`)) return;
    try {
      await api.removeSupplier(name);
      load();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="panel">
      <h2>Suppliers</h2>
      {error && <p className="error">{error}</p>}
      <form className="inline-form" onSubmit={handleAdd}>
        <input
          placeholder="Name"
          value={form.name}
          onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
          required
        />
        <input
          placeholder="Contact"
          value={form.phno}
          onChange={(e) => setForm((f) => ({ ...f, phno: e.target.value }))}
          required
        />
        <button type="submit">Add supplier</button>
      </form>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Contact</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {suppliers.map((s) => (
            <tr key={s.suid}>
              <td>{s.name}</td>
              <td>{s.contact}</td>
              <td>
                <button className="danger" onClick={() => handleDelete(s.name)}>
                  Remove
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
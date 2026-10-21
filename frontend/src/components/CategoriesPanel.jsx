import { useEffect, useState } from "react";
import { api } from "../api/client";

export default function CategoriesPanel() {
  const [categories, setCategories] = useState([]);
  const [name, setName] = useState("");
  const [error, setError] = useState("");

  async function load() {
    try {
      const res = await api.getCategories();
      setCategories(res.categories || []);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function handleAdd(e) {
    e.preventDefault();
    setError("");
    try {
      await api.addCategory(name);
      setName("");
      load();
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleDelete(cname) {
    if (!confirm(`Delete category "${cname}"?`)) return;
    try {
      await api.deleteCategory(cname);
      load();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="panel">
      <h2>Categories</h2>
      {error && <p className="error">{error}</p>}
      <form className="inline-form" onSubmit={handleAdd}>
        <input
          placeholder="New category name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <button type="submit">Add</button>
      </form>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {categories.map((c) => (
            <tr key={c.cid}>
              <td>{c.cname}</td>
              <td>
                <button className="danger" onClick={() => handleDelete(c.cname)}>
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
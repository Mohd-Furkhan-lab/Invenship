import { useEffect, useState } from "react";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";

const ROLES = ["admin", "receptionist", "user"];
const emptyForm = { name: "", email: "", password: "", role: "user" };

export default function UsersPanel() {
  const { isAdmin } = useAuth();
  const [users, setUsers] = useState([]);
  const [search, setSearch] = useState("");
  const [form, setForm] = useState(emptyForm);
  const [error, setError] = useState("");

  async function load(email) {
    setError("");
    try {
      const res = await api.adminGetUsers(email || undefined);
      const data = res.data;
      setUsers(Array.isArray(data) ? data : data ? [data] : []);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    if (isAdmin) load();
  }, [isAdmin]);

  // This whole panel is an admin namespace on the backend — never render it,
  // let alone fire the fetch, for anyone else.
  if (!isAdmin) {
    return (
      <div className="panel">
        <h2>Users</h2>
        <p className="empty-state">This section is only available to admins.</p>
      </div>
    );
  }

  function update(field, value) {
    setForm((f) => ({ ...f, [field]: value }));
  }

  async function handleSearch(e) {
    e.preventDefault();
    load(search);
  }

  async function handleAdd(e) {
    e.preventDefault();
    setError("");
    try {
      await api.adminAddUser(form);
      setForm(emptyForm);
      load(search);
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleRoleChange(email, new_role) {
    try {
      await api.adminUpdateRole(email, new_role);
      load(search);
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleDelete(email) {
    if (!confirm(`Delete user "${email}"?`)) return;
    try {
      await api.adminDeleteUser(email);
      load(search);
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="panel">
      <h2>Users</h2>
      {error && <p className="error">{error}</p>}

      <form className="inline-form" onSubmit={handleSearch}>
        <input
          placeholder="Search by email"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <button type="submit">Search</button>
        <button
          type="button"
          className="ghost"
          onClick={() => {
            setSearch("");
            load();
          }}
        >
          Show all
        </button>
      </form>

      <form className="card form-grid" onSubmit={handleAdd}>
        <h3>Add user</h3>
        <input placeholder="Name" value={form.name} onChange={(e) => update("name", e.target.value)} required />
        <input
          placeholder="Email"
          type="email"
          value={form.email}
          onChange={(e) => update("email", e.target.value)}
          required
        />
        <input
          placeholder="Password"
          type="password"
          value={form.password}
          onChange={(e) => update("password", e.target.value)}
          required
        />
        <select value={form.role} onChange={(e) => update("role", e.target.value)}>
          {ROLES.map((r) => (
            <option key={r} value={r}>
              {r}
            </option>
          ))}
        </select>
        <button type="submit">Add user</button>
      </form>

      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Role</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {users.map((u) => (
            <tr key={u.uid || u.email}>
              <td>{u.username}</td>
              <td>{u.email}</td>
              <td>
                <select value={u.role} onChange={(e) => handleRoleChange(u.email, e.target.value)}>
                  {ROLES.map((r) => (
                    <option key={r} value={r}>
                      {r}
                    </option>
                  ))}
                </select>
              </td>
              <td>
                <button className="danger" onClick={() => handleDelete(u.email)}>
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
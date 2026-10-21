import { useState } from "react";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";

const MIN_LENGTH = 8;
const emptyForm = { oldpassword: "", newpassword: "", confirm: "" };

export default function AccountPanel() {
  const { user, role } = useAuth();
  const [form, setForm] = useState(emptyForm);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [busy, setBusy] = useState(false);

  function update(field, value) {
    setForm((f) => ({ ...f, [field]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (form.newpassword.length < MIN_LENGTH) {
      setError(`New password must be at least ${MIN_LENGTH} characters.`);
      return;
    }
    if (form.newpassword !== form.confirm) {
      setError("New password and confirmation don't match.");
      return;
    }
    if (form.newpassword === form.oldpassword) {
      setError("New password must be different from the current one.");
      return;
    }

    setBusy(true);
    try {
      const res = await api.changePassword(form.oldpassword, form.newpassword);
      setSuccess((res && res.message) || "Password updated.");
      setForm(emptyForm);
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="panel">
      <h2>Account</h2>
      <p className="hint">
        {user?.username} &middot; {user?.email} &middot; {role}
      </p>

      <form className="card narrow-card" onSubmit={handleSubmit}>
        <h3>Change password</h3>
        {error && <p className="error">{error}</p>}
        {success && <p className="success">{success}</p>}
        <label>
          Current password
          <input
            type="password"
            autoComplete="current-password"
            value={form.oldpassword}
            onChange={(e) => update("oldpassword", e.target.value)}
            required
          />
        </label>
        <label>
          New password
          <input
            type="password"
            autoComplete="new-password"
            value={form.newpassword}
            onChange={(e) => update("newpassword", e.target.value)}
            required
          />
        </label>
        <label>
          Confirm new password
          <input
            type="password"
            autoComplete="new-password"
            value={form.confirm}
            onChange={(e) => update("confirm", e.target.value)}
            required
          />
        </label>
        <button type="submit" disabled={busy}>
          {busy ? "Saving..." : "Update password"}
        </button>
      </form>
    </div>
  );
}
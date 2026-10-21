import { useAuth } from "../context/AuthContext";

const TABS_ADMIN = [
  { id: "products", label: "Products" },
  { id: "categories", label: "Categories" },
  { id: "purchases", label: "Purchases" },
  { id: "suppliers", label: "Suppliers" },
  { id: "sales", label: "Sales" },
  { id: "users", label: "Users" },
  { id: "analysis", label: "Analysis" },
  { id: "assistant", label: "Assistant" },
];

// NOTE: "suppliers" removed here on purpose — the backend returns
// "Forbidden Admin only" for non-admins on /suppliers/, so showing the tab
// just walked receptionists into a broken page. If receptionists should get
// read-only supplier access, that needs a backend permission change first,
// then this tab can come back.
const TABS_RECEPTIONIST = [
  { id: "products", label: "Products" },
  { id: "sales", label: "Sales" },
];

export default function Layout({ active, onChange, children, theme, onToggleTheme }) {
  const { user, role, isAdmin, logout } = useAuth();
  const tabs = isAdmin ? TABS_ADMIN : TABS_RECEPTIONIST;

  return (
    <div className="layout">
      <header className="topbar">
        <span className="brand">Invenship</span>
        <nav>
          {tabs.map((t) => (
            <button
              key={t.id}
              className={active === t.id ? "tab active" : "tab"}
              onClick={() => onChange(t.id)}
            >
              {t.label}
            </button>
          ))}
        </nav>
        <div className="userbox">
          <button
            className="linklike"
            onClick={() => onChange("account")}
            title="Account and password"
          >
            {user?.username || user?.email}
          </button>
          {role && <span className="role-pill">{role}</span>}
          <button
            className="ghost"
            onClick={onToggleTheme}
            aria-label={theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
            title={theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
          >
            {theme === "dark" ? "☀ Light" : "☾ Dark"}
          </button>
          <button className="ghost" onClick={logout}>
            Log out
          </button>
        </div>
      </header>
      <main className="content">{children}</main>
    </div>
  );
}

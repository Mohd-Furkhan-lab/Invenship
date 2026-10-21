import { useState } from "react";
import { AuthProvider, useAuth } from "./context/AuthContext";
import Login from "./components/Login";
import Layout from "./components/Layout";
import ProductsPanel from "./components/ProductsPanel";
import CategoriesPanel from "./components/CategoriesPanel";
import PurchasesPanel from "./components/PurchasesPanel";
import SuppliersPanel from "./components/SuppliersPanel";
import SalesPanel from "./components/SalesPanel";
import UsersPanel from "./components/UsersPanel";
import AnalysisPanel from "./components/AnalysisPanel";
import ChatPanel from "./components/ChatPanel";
import AccountPanel from "./components/AccountPanel";
import { useTheme } from "./hooks/useTheme";
import "./styles.css";

function Shell() {
  const { user, loading, isAdmin } = useAuth();
  const [tab, setTab] = useState("sales");
  const { theme, toggle } = useTheme(); // applies data-theme to <html>, also on the login page

  if (loading) return <div className="loading">Loading...</div>;
  if (!user) return <Login />;

  return (
    <Layout active={tab} onChange={setTab} theme={theme} onToggleTheme={toggle}>
      {tab === "products" && <ProductsPanel />}
      {tab === "categories" && isAdmin && <CategoriesPanel />}
      {tab === "purchases" && isAdmin && <PurchasesPanel />}
      {tab === "suppliers" && <SuppliersPanel />}
      {tab === "sales" && <SalesPanel />}
      {tab === "users" && isAdmin && <UsersPanel />}
      {tab === "analysis" && isAdmin && <AnalysisPanel />}
      {tab === "assistant" && isAdmin && <ChatPanel />}
      {tab === "account" && <AccountPanel />}
    </Layout>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <Shell />
    </AuthProvider>
  );
}

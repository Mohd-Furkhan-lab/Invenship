import { createContext, useContext, useEffect, useState } from "react";
import { api, setOnAuthExpired } from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [role, setRole] = useState(null);
  const [loading, setLoading] = useState(true);

  const isAdmin = role === "admin";
  const isReceptionist = role === "receptionist";

  async function loadUser() {
    try {
      const res = await api.me();
      setUser(res.details);
      setRole(res.details?.role ?? null);
    } catch {
      setUser(null);
      setRole(null);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    // If a refresh attempt ever fails (refresh token itself expired/revoked),
    // drop back to a signed-out state so Login shows up instead of a broken screen.
    setOnAuthExpired(() => {
      setUser(null);
      setRole(null);
    });
    loadUser();
  }, []);

  async function login(email, password) {
    await api.login(email, password);
    await loadUser();
  }

  async function logout() {
    await api.logout();
    setUser(null);
    setRole(null);
  }

  return (
    <AuthContext.Provider value={{ user, role, isAdmin, isReceptionist, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
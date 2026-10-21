const BASE_URL = "http://127.0.0.1:8000"; // TODO: point this at your running backend

const REFRESH_PATH = "/users/refresh";
// Endpoints where a 401 means "wrong credentials", not "access token expired".
// Without this, a bad password triggered a refresh attempt and showed
// "Session expired" instead of "Invalid Credentials".
const NO_REFRESH_PATHS = [REFRESH_PATH, "/users/login"];

let onAuthExpired = null;
export function setOnAuthExpired(handler) {
  onAuthExpired = handler;
}

// Dedupe concurrent refresh calls.
let refreshPromise = null;

async function doRefresh() {
  if (!refreshPromise) {
    refreshPromise = fetch(`${BASE_URL}${REFRESH_PATH}`, {
      method: "POST",
      credentials: "include",
    })
      .then((res) => {
        if (!res.ok) throw new Error("refresh failed");
        return true;
      })
      .finally(() => {
        refreshPromise = null;
      });
  }
  return refreshPromise;
}

// FastAPI sends `detail` as a string for HTTPException and as an array of
// { loc, msg, type } objects for 422 validation errors.
function formatError(detail, fallback) {
  if (!detail) return fallback || "Request failed";
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail
      .map((d) => {
        const field = Array.isArray(d.loc) ? d.loc.filter((p) => p !== "body").join(".") : "";
        return field ? `${field}: ${d.msg}` : d.msg;
      })
      .join("; ");
  }
  return fallback || "Request failed";
}

async function request(path, { method = "GET", body, isForm = false, _retried = false } = {}) {
  const opts = { method, credentials: "include" };
  if (body !== undefined) {
    if (isForm) {
      opts.body = body;
    } else {
      opts.headers = { "Content-Type": "application/json" };
      opts.body = JSON.stringify(body);
    }
  }

  const res = await fetch(`${BASE_URL}${path}`, opts);

  if (res.status === 401 && !_retried && !NO_REFRESH_PATHS.includes(path)) {
    try {
      await doRefresh();
      return request(path, { method, body, isForm, _retried: true });
    } catch {
      if (onAuthExpired) onAuthExpired();
      throw new Error("Session expired. Please sign in again.");
    }
  }

  const text = await res.text();
  let data;
  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = text;
  }
  if (!res.ok) {
    // 309 is what the backend uses for "already exists"; fetch doesn't follow it
    // (no Location header), so it lands here with a readable `detail`.
    throw new Error(formatError(data && data.detail, res.statusText));
  }
  return data;
}

export const api = {
  // --- auth ---
  login: (email, password) =>
    request("/users/login", { method: "POST", body: { email, password } }),
  logout: () => request("/users/logout", { method: "POST" }),
  me: () => request("/users/me"),
  changePassword: (oldpassword, newpassword) =>
    request("/users/new-password", { method: "PUT", body: { oldpassword, newpassword } }),

  // --- categories ---
  getCategories: () => request("/products/category/"),
  addCategory: (name) =>
    request(`/products/category/${encodeURIComponent(name)}`, { method: "POST" }),
  deleteCategory: (name) =>
    request(`/products/category/${encodeURIComponent(name)}`, { method: "DELETE" }),

  // --- products ---
  getProducts: ({ name, brand, size } = {}) => {
    const params = new URLSearchParams();
    if (name) params.set("name", name);
    if (brand) params.set("brand", brand);
    if (size) params.set("size", size);
    const qs = params.toString();
    return request(`/products/${qs ? `?${qs}` : ""}`);
  },
  addProduct: (product) => request("/products/", { method: "POST", body: product }),
  updateProduct: (name, data) =>
    request(`/products/${encodeURIComponent(name)}`, { method: "PUT", body: data }),
  deleteProduct: (name) =>
    request(`/products/${encodeURIComponent(name)}`, { method: "DELETE" }),
  uploadProductImage: (file) => {
    const form = new FormData();
    form.append("file", file);
    return request("/products/upload", { method: "POST", body: form, isForm: true });
  },

  // --- purchases ---
  getPurchases: () => request("/purchases/"),
  addPurchase: (purchase) => request("/purchases/", { method: "POST", body: purchase }),
  clearPurchases: () => request("/purchases/", { method: "DELETE" }),

  // --- sales ---
  getSales: () => request("/sales/"),
  addSale: (sale) => request("/sales/", { method: "POST", body: sale }),
  clearSales: () => request("/sales/clear", { method: "DELETE" }),

  // --- suppliers ---
  getSuppliers: (name) =>
    request(`/suppliers/${name ? `?name=${encodeURIComponent(name)}` : ""}`),
  addSupplier: (supplier) => request("/suppliers/", { method: "POST", body: supplier }),
  removeSupplier: (name) =>
    request(`/suppliers/${encodeURIComponent(name)}`, { method: "DELETE" }),

  // --- admin: user management ---
  adminGetUsers: (email) =>
    request(`/admin/users${email ? `?email=${encodeURIComponent(email)}` : ""}`),
  adminAddUser: (user) => request("/admin/users", { method: "POST", body: user }),
  adminUpdateRole: (email, new_role) =>
    request("/admin/users/update-role", { method: "PUT", body: { email, new_role } }),
  adminDeleteUser: (email) =>
    request(`/admin/users/${encodeURIComponent(email)}`, { method: "DELETE" }),

  // --- analysis (admin only) ---
  getReport: () => request("/analysis/"),
  // Backend returns { response: "text" }
  chat: (question) => request("/analysis/chat", { method: "POST", body: { question } }),
};
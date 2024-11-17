import { paginationStore } from "./pagination.store.js";

// Initialize all stores
window.addEventListener("alpine:init", () => {
  console.log("alpine init", Alpine.store("pagination"));
  Alpine.store("pagination", paginationStore);
  // Add other stores here
});

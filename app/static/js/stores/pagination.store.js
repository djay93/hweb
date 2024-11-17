export const paginationStore = {
  data: {
    current_page: 1,
    per_page: 10,
    total: 0,
    pages: 0,
    has_prev: false,
    has_next: false,
    prev_num: null,
    next_num: null,
  },

  setData(newData) {
    this.data = { ...this.data, ...newData };
  },

  clear() {
    this.data = {
      current_page: 1,
      per_page: 10,
      total: 0,
      pages: 0,
      has_prev: false,
      has_next: false,
      prev_num: null,
      next_num: null,
    };
  },
};

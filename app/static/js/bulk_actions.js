export class BulkActions {
  constructor(options) {
    this.masterCheckbox = document.querySelector(options.masterCheckbox);
    this.itemCheckboxes = document.querySelectorAll(options.itemCheckboxes);
    this.actionButtons = document.querySelectorAll(options.actionButtons);
    this.onSelectionChange = options.onSelectionChange;

    this.initializeEventListeners();
  }

  initializeEventListeners() {
    // Master checkbox handler
    this.masterCheckbox?.addEventListener("change", () => {
      this.itemCheckboxes.forEach((checkbox) => {
        checkbox.checked = this.masterCheckbox.checked;
      });
      this.updateSelectionState();
    });

    // Individual checkbox handler
    this.itemCheckboxes.forEach((checkbox) => {
      checkbox.addEventListener("change", () => {
        this.updateMasterCheckboxState();
        this.updateSelectionState();
      });
    });
  }

  updateMasterCheckboxState() {
    if (!this.masterCheckbox) return;

    const checkedCount = this.getSelectedItems().length;
    const totalCount = this.itemCheckboxes.length;

    this.masterCheckbox.checked = checkedCount === totalCount;
    this.masterCheckbox.indeterminate = checkedCount > 0 && checkedCount < totalCount;
  }

  updateSelectionState() {
    const selectedCount = this.getSelectedItems().length;

    // Call the callback if provided
    if (this.onSelectionChange) {
      this.onSelectionChange(selectedCount);
    }
  }

  getSelectedItems() {
    return Array.from(this.itemCheckboxes)
      .filter((checkbox) => checkbox.checked)
      .map((checkbox) => checkbox.dataset.itemId);
  }
}

// ==========================
// ADMIN DASHBOARD MODALS
// ==========================

// --- OPEN / CLOSE MODALS ---
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.style.display = "flex";
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.style.display = "none";
}

// --- EDIT PRODUCT MODAL ---
function openEditModal(button) {
    document.getElementById("edit-id").value = button.dataset.id;
    document.getElementById("edit-name").value = button.dataset.name;
    document.getElementById("edit-category").value = button.dataset.category;
    document.getElementById("edit-image").value = button.dataset.image;
    document.getElementById("edit-collection").value = button.dataset.collection || "";
    document.getElementById("edit-price").value = button.dataset.price;
    document.getElementById("edit-description").value = button.dataset.description;

    openModal("editModal");
}

function closeEditModal() {
    closeModal("editModal");
}

// --- ADD PRODUCT MODAL ---
function openAddModal() {
    openModal("addModal");
}

function closeAddModal() {
    closeModal("addModal");
}

// --- EDIT PROMO MODAL ---
function openEditPromoModal(button) {
    document.getElementById("edit-promo-id").value = button.dataset.id;
    document.getElementById("edit-promo-code").value = button.dataset.code;
    document.getElementById("edit-promo-discount").value = button.dataset.discount;
    document.getElementById("edit-promo-description").value = button.dataset.description;

    openModal("editPromoModal");
}

function closeEditPromoModal() {
    closeModal("editPromoModal");
}

// --- ADD PROMO MODAL ---
function openAddPromoModal() {
    openModal("addPromoModal");
}

function closeAddPromoModal() {
    closeModal("addPromoModal");
}

// ==========================
// CLICK OUTSIDE TO CLOSE
// ==========================
window.addEventListener("click", function (event) {
    // All modals have class "admin-modal"
    const modals = document.querySelectorAll(".admin-modal");

    modals.forEach(modal => {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
});

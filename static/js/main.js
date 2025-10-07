const productContainer = document.getElementById('product-container');
const GET_URL = productContainer?.dataset.getUrl;
const CREATE_URL = productContainer?.dataset.createUrl;
const USER_ID = parseInt(productContainer?.dataset.userId) || 0;
const NO_PRODUCTS_IMAGE_URL = productContainer?.dataset.noProductsImageUrl;

function truncateWords(text, limit) {
    if (!text) return "";
    if (text.split(" ").length > limit) {
        return text.split(" ").slice(0, limit).join(" ") + "...";
    }
    return text;
}

async function refreshProducts(filter = null, category = null) {
    if (!productContainer) return;
    productContainer.innerHTML = `<p class="text-center text-gray-500">Loading...</p>`;
    let url = new URL(GET_URL, window.location.origin);
    if (filter) url.searchParams.append('filter', filter);
    if (category) url.searchParams.append('category', category);

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error('Network response was not OK');
        const products = await response.json();
        productContainer.innerHTML = "";

        if (products.length === 0) {
            productContainer.innerHTML = `
                <div class="bg-[#4B0082] rounded-lg p-12 text-center shadow-sm">
                    <img src="${NO_PRODUCTS_IMAGE_URL}" alt="No Products available" class="w-40 h-40 mx-auto mb-4">
                    <h3 class="text-lg font-medium text-[#FFD700] mb-2">No Products available</h3>
                </div>
            `;
            return;
        }

        products.forEach(product => {
            const card = document.createElement('div');
            card.className = "bg-white rounded-lg shadow-sm overflow-hidden flex transition hover:shadow-lg";
            let buttons = (USER_ID === product.user_id) ? `
                <button class="text-sm font-medium text-yellow-600 hover:text-yellow-800" data-action="edit" data-id="${product.pk}">Edit</button>
                <button class="text-sm font-medium text-red-600 hover:text-red-800" data-action="delete" data-id="${product.pk}">Delete</button>
            ` : '';
            card.innerHTML = `
                <div class="w-1/3 relative">
                    <img src="${product.thumbnail}" alt="${product.name}" class="w-full h-40 object-contain bg-gray-100">
                    <span class="absolute top-0 left-0 bg-purple-700 text-[#FFD700] text-xs font-semibold px-2 py-1 rounded-br-lg">${product.category}</span>
                </div>
                <div class="p-4 flex flex-col justify-between w-2/3">
                    <div>
                        <p class="text-xs text-gray-500">Seller: ${product.user_username} | ${product.news_views} Views</p>
                        <h3 class="font-bold text-lg text-gray-900">${product.name}</h3>
                        <p class="text-sm text-gray-600 mt-1">${truncateWords(product.description, 25)}</p>
                    </div>
                    <div class="flex justify-between items-center mt-3">
                        <p class="font-semibold text-purple-700">Rp ${product.price.toLocaleString('id-ID')}</p>
                        <div class="flex items-center gap-4">
                            ${buttons}
                            <a href="/news/${product.pk}/" class="text-sm font-medium text-purple-600 hover:text-purple-800">Read More</a>
                        </div>
                    </div>
                </div>`;
            productContainer.appendChild(card);
        });
    } catch (error) {
        productContainer.innerHTML = `<p class="text-center text-red-500">Failed to load products.</p>`;
        console.error("ERROR DISINI WOI:", error);
    }
}

document.addEventListener('DOMContentLoaded', function () {
    if (!productContainer) return;

    const formModal = document.getElementById('crudModal');
    const deleteModal = document.getElementById('deleteModal');
    const productForm = document.getElementById('productForm');
    const modalTitle = document.getElementById('modalTitle');
    const confirmDeleteButton = document.getElementById('confirm-delete-btn');

    function openAddModal() {
        productForm.reset();
        modalTitle.innerText = 'Add New Product';
        productForm.onsubmit = (event) => handleFormSubmit(event, 'create');
        formModal.classList.remove('hidden');
    }

    async function openEditModal(productId) {
        productForm.reset();
        modalTitle.innerText = 'Edit Product';
        try {
            const response = await fetch(`/json/${productId}/`);
            if (!response.ok) throw new Error('Product not found');
            const product = await response.json();

            document.getElementById('name').value = product.name;
            document.getElementById('price').value = product.price;
            document.getElementById('description').value = product.description;
            document.getElementById('category').value = product.category;
            document.getElementById('thumbnail').value = product.thumbnail;

            productForm.onsubmit = (event) => handleFormSubmit(event, 'edit', productId);
            formModal.classList.remove('hidden');
        } catch (error) {
            if (typeof showToast === 'function') showToast('Error', 'Could not load product data.', 'error');
        }
    }

    function closeFormModal() {
        formModal.classList.add('hidden');
    }

    async function handleFormSubmit(event, mode, productId = null) {
        event.preventDefault();
        const formData = new FormData(productForm);
        const url = mode === 'create' ? CREATE_URL : `/edit-news-ajax/${productId}/`;
        try {
            const response = await fetch(url, {
                method: 'POST',
                body: formData
            });
            const result = await response.json();
            if (result.status === "success") {
                closeFormModal();
                refreshProducts();
                const action = mode === 'edit' ? 'updated' : 'added';
                if (typeof showToast === 'function') showToast('Success', `Product successfully ${action}!`, 'success');
            } else {
                if (typeof showToast === 'function') showToast('Error', 'An error occurred.', 'error');
            }
        } catch {
            if (typeof showToast === 'function') showToast('Error', 'A network error occurred.', 'error');
        }
    }

    function openDeleteModal(productId) {
        if (!deleteModal) return;
        confirmDeleteButton.onclick = () => confirmDelete(productId);
        deleteModal.classList.remove('hidden');
    }

    function closeDeleteModal() {
        if (deleteModal) deleteModal.classList.add('hidden');
    }

    async function confirmDelete(productId) {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        try {
            const response = await fetch(`/delete-news-ajax/${productId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                },
            });
            const data = await response.json();
            if (data.status === 'success') {
                closeDeleteModal();
                refreshProducts();
                if (typeof showToast === 'function') showToast('Success', 'Product has been deleted.', 'success');
            } else {
                if (typeof showToast === 'function') showToast('Error', 'Failed to delete product.', 'error');
            }
        } catch {
            if (typeof showToast === 'function') showToast('Error', 'A network error occurred.', 'error');
        }
    }

    document.getElementById('add-product-btn')?.addEventListener('click', openAddModal);
    document.getElementById('close-modal-btn')?.addEventListener('click', closeFormModal);
    document.getElementById('cancel-btn')?.addEventListener('click', closeFormModal);
    document.getElementById('all-products-btn')?.addEventListener('click', () => refreshProducts());
    document.getElementById('my-products-btn')?.addEventListener('click', () => refreshProducts('my'));
    document.getElementById('cancel-delete-btn')?.addEventListener('click', closeDeleteModal);

    document.querySelectorAll('.logout-btn').forEach(button => {
        button.addEventListener('click', async () => {
            const response = await fetch('/logout-ajax/');
            const data = await response.json();
            if (data.status === 'success') {
                if (typeof showToast === 'function') showToast('Success', data.message, 'success');
                setTimeout(() => {
                    window.location.href = "/login/";
                }, 1000);
            }
        });
    });

    productContainer.addEventListener('click', function (e) {
        const action = e.target.dataset.action;
        const id = e.target.dataset.id;
        if (action === 'edit') openEditModal(id);
        if (action === 'delete') openDeleteModal(id);
    });

    refreshProducts();
});
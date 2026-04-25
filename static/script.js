let cart = [];
let appliedPromo = null;


function calculateTotal() {
    const subtotal = cart.reduce((sum, item) => {
        const price = parseFloat(item.price.replace('€', '').replace(',', '.'));
        return sum + price;
    }, 0);
    
    let discount = 0;
    if (appliedPromo) {
        discount = (subtotal * appliedPromo.discount) / 100;
    }
    
    return {
        subtotal: subtotal,
        discount: discount,
        total: subtotal - discount
    };
}

function updateCartUI() {
    const cartCount = document.getElementById('cartCount');
    const cartItems = document.getElementById('cartItems');
    const cartTotal = document.getElementById('cartTotal');
    const discountRow = document.getElementById('discountRow');
    const discountAmount = document.getElementById('discountAmount');
    
    cartCount.textContent = cart.length;
    
    if (cart.length === 0) {
        cartItems.innerHTML = '<div class="empty-cart"><p>Jūsu grozs ir tukšs</p></div>';
        cartTotal.textContent = '0.00€';
        discountRow.style.display = 'none';
        return;
    }
    
    cartItems.innerHTML = cart.map((item, index) => `
        <div class="cart-item">
            <div class="cart-item-info">
                <div class="cart-item-name">${item.name}</div>
                <div class="cart-item-price">${item.price}</div>
            </div>
            <button class="remove-button" onclick="removeFromCart(${index})">Noņemt</button>
        </div>
    `).join('');
    
    const totals = calculateTotal();
    
    if (appliedPromo) {
        discountRow.style.display = 'flex';
        discountAmount.textContent = '-' + totals.discount.toFixed(2) + '€';
    } else {
        discountRow.style.display = 'none';
    }
    
    cartTotal.textContent = totals.total.toFixed(2) + '€';
}

async function applyPromoCode() {
    const promoInput = document.getElementById('promoInput');
    const promoMessage = document.getElementById('promoMessage');
    const code = promoInput.value.trim().toUpperCase();
    
    if (!code) {
        promoMessage.className = 'promo-message error';
        promoMessage.textContent = 'Lūdzu, ievadiet promocode!';
        return;
    }
    
    if (cart.length === 0) {
        promoMessage.className = 'promo-message error';
        promoMessage.textContent = 'Grozs ir tukšs! Pievienojiet preces pirms promocode lietošanas.';
        return;
    }

    try {
        const response = await fetch(`/api/promo/${encodeURIComponent(code)}`);
        if (!response.ok) {
            promoMessage.className = 'promo-message error';
            promoMessage.textContent = '❌ Nederīgs promocode!';
            appliedPromo = null;
            updateCartUI();
            return;
        }
        const data = await response.json();
        if (!data.valid) {
            promoMessage.className = 'promo-message error';
            promoMessage.textContent = '❌ Nederīgs promocode!';
            appliedPromo = null;
            updateCartUI();
            return;
        }

        appliedPromo = { code: data.code, discount: data.discount, description: data.description };
        
        document.getElementById('promoApplied').style.display = 'flex';
        document.getElementById('appliedPromoCode').textContent = data.code;
        document.getElementById('appliedDiscount').textContent = data.discount;
        document.getElementById('promoInputSection').style.display = 'none';
        
        updateCartUI();
        
        promoMessage.className = 'promo-message success';
        promoMessage.textContent = `✓ Promocode "${data.code}" pielietots! ${data.description}`;
    } catch (err) {
        console.error('Error checking promo code', err);
        promoMessage.className = 'promo-message error';
        promoMessage.textContent = 'Radās kļūda, mēģiniet vēlreiz.';
    }
}

function removePromoCode() {
    appliedPromo = null;
    document.getElementById('promoApplied').style.display = 'none';
    document.getElementById('promoInputSection').style.display = 'block';
    document.getElementById('promoInput').value = '';
    document.getElementById('promoMessage').className = 'promo-message';
    document.getElementById('promoMessage').textContent = '';
    updateCartUI();
}

function openCart() {
    document.getElementById('cartModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closeCart() {
    document.getElementById('cartModal').style.display = 'none';
    document.body.style.overflow = 'auto';
}

function removeFromCart(index) {
    cart.splice(index, 1);
    if (cart.length === 0) {
        removePromoCode();
    }
    updateCartUI();
}

function clearCart() {
    if (confirm('Vai tiešām vēlaties iztukšot grozu?')) {
        cart = [];
        removePromoCode();
        updateCartUI();
    }
}

function checkout() {
    if (cart.length === 0) {
        alert('Jūsu grozs ir tukšs!');
        return;
    }
    
    const totals = calculateTotal();
    let message = `Paldies par pirkumu!\n\nKopsumma: ${totals.subtotal.toFixed(2)}€`;
    
    if (appliedPromo) {
        message += `\nAtlaide (${appliedPromo.discount}%): -${totals.discount.toFixed(2)}€`;
    }
    
    message += `\nKopā maksājams: ${totals.total.toFixed(2)}€`;
    
    alert(message);
    cart = [];
    removePromoCode();
    updateCartUI();
    closeCart();
}



const collectionModal = document.getElementById('collectionModal');
const modalTitle = document.getElementById('modalTitle');
const modalGrid = document.getElementById('modalGrid');
const closeButton = document.querySelector('.close-button');

const imageModal = document.getElementById('imageModal');
const fullSizeImage = document.getElementById('fullSizeImage');
const imageCloseButton = document.querySelector('.image-close');



function showFullImage(imageSrc) {
    fullSizeImage.src = imageSrc;
    imageModal.style.display = 'block';
    event.stopPropagation();
}

function addToCart(productName, price) {
    event.stopPropagation();
    
    cart.push({ name: productName, price: price });
    updateCartUI();
    
    const notification = document.getElementById('cartNotification');
    notification.textContent = `${productName} pievienots grozam! 🛒`;
    notification.classList.add('show');
    
    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

function closeCollectionModal() {
    collectionModal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

function closeImageModal() {
    imageModal.style.display = 'none';
    event.stopPropagation();
}

closeButton.addEventListener('click', closeCollectionModal);
imageCloseButton.addEventListener('click', closeImageModal);

window.addEventListener('click', (event) => {
    if (event.target === collectionModal) {
        closeCollectionModal();
    }
    if (event.target === imageModal) {
        closeImageModal();
    }
    if (event.target === document.getElementById('cartModal')) {
        closeCart();
    }
});

document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
        if (imageModal.style.display === 'block') {
            closeImageModal();
        } else if (collectionModal.style.display === 'block') {
            closeCollectionModal();
        } else if (document.getElementById('cartModal').style.display === 'block') {
            closeCart();
        }
    }
});

const items = {
    top: {
        images: ['/static/pictures/black_hoddie.png', '/static/pictures/black_ziphoodie.png', '/static/pictures/blue_ziphoodie.png', '/static/pictures/black_tshirt.png', '/static/pictures/black_longsleeve_woman.png', '/static/pictures/black_longsleeve_man.png', '/static/pictures/white_hoodie.png', '/static/pictures/white_tshirt.png', '/static/pictures/white_longsleeve_man.png', '/static/pictures/white_longsleeve_woman.png', '/static/pictures/whitee_hoodie.png', '/static/pictures/blue_hoodie.png', '/static/pictures/blue_tshirt.png', '/static/pictures/blue_longsleeve_man.png', '/static/pictures/blue_longsleeve_woman.png'],
        current: 0,
        selected: false
    },
    
    footwear: {
        images: ['/static/pictures/black_socks.png', '/static/pictures/blue_socks.png', '/static/pictures/white_socks.png'],
        current: 0,
        selected: false
    },
    hat: {
        images: ['/static/pictures/black_cap.png', '/static/pictures/black_hat.png', '/static/pictures/white_cap.png', '/static/pictures/white_hat.png', '/static/pictures/blue_cap.png', '/static/pictures/blue_hat.png'],
        current: 0,
        selected: false
    },
    pants: {
        images: ['/static/pictures/black_pants.png', '/static/pictures/white_pants.png', '/static/pictures/blue_pants.png'],
        current: 0,
        selected: false
    },
    
    bag: {
        images: ['/static/pictures/black_bag.png', '/static/pictures/white_bag.png', '/static/pictures/blue_bag.png'],
        current: 0,
        selected: false
    }
};

Object.keys(items).forEach(category => {
    const img = document.getElementById(`${category}-img`);
    const frame = img.parentElement;
    const viewer = frame.parentElement;
    const prevBtn = viewer.querySelector('.prev-btn');
    const nextBtn = viewer.querySelector('.next-btn');

    prevBtn.onclick = () => {
    const item = items[category];
    item.current = (item.current - 1 + item.images.length) % item.images.length;
    img.src = item.images[item.current];
};

nextBtn.onclick = () => {
    const item = items[category];
    item.current = (item.current + 1) % item.images.length;
    img.src = item.images[item.current];
};
    frame.onclick = () => {
        const item = items[category];
        item.selected = !item.selected;
        frame.classList.toggle('selected');
    };
});

document.getElementById('confirm-look').onclick = () => {
    const finalLook = document.getElementById('final-look');
    const selectedItems = document.querySelector('.selected-items');
    selectedItems.innerHTML = '';

    let hasSelected = false;
    
    Object.entries(items).forEach(([category, item]) => {
        if (item.selected) {
            hasSelected = true;
            selectedItems.innerHTML += `
                <div class="selected-item">
                    <img src="${item.images[item.current]}" alt="${category}">
                    <p>${category.charAt(0).toUpperCase() + category.slice(1)}</p>
                </div>
            `;
        }
    });

   
    if (!hasSelected) {
        selectedItems.innerHTML = '<p style="text-align: center; color: #666; padding: 40px;">Lūdzu, izvēlieties vismaz vienu preci, noklikšķinot uz attēla!</p>';
    }

    finalLook.style.display = 'block';

    finalLook.scrollIntoView({ behavior: 'smooth', block: 'center' });
};

document.querySelectorAll('.navbar a').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const targetId = this.getAttribute('href').substring(1);
        const targetElement = document.getElementById(targetId);

        if (targetElement) {
            const navbarHeight = document.querySelector('.navbar').offsetHeight;
            const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset;

            window.scrollTo({
                top: targetPosition - navbarHeight,
                behavior: 'smooth'
            });
        }
    });
});

window.addEventListener('scroll', () => {
    const navbarHeight = document.querySelector('.navbar').offsetHeight;
    const sections = document.querySelectorAll('div[id]');

    sections.forEach(section => {
        const sectionTop = section.offsetTop - navbarHeight - 10;
        const sectionBottom = sectionTop + section.offsetHeight;
        const scrollPosition = window.scrollY;
        const navLink = document.querySelector(`.navbar a[href="#${section.id}"]`);

        if (navLink && scrollPosition >= sectionTop && scrollPosition < sectionBottom) {
            document.querySelectorAll('.navbar a').forEach(link => {
                link.style.backgroundColor = '';
                link.style.color = 'white';
            });
            navLink.style.backgroundColor = '#e4b400';
            navLink.style.color = '#222222';
        }
    });
});
let currentCollection = null;
let currentFilter = 'all';

function filterCategory(category) {
    currentFilter = category;
   
    document.querySelectorAll('.filter-button').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    
    if (currentCollection) {
        renderCollection(currentCollection, category);
    }
}

function renderCollection(collection, filter = 'all') {
    const items = filter === 'all' 
        ? collection.items 
        : collection.items.filter(item => item.category === filter);
    
    if (items.length === 0) {
        modalGrid.innerHTML = '<p style="text-align: center; padding: 60px; color: #999; font-size: 1.2em;">Nav preču šajā kategorijā</p>';
        return;
    }
    
    modalGrid.innerHTML = items.map(item => `
        <div class="collection-item">
            <img src="${item.image}" alt="${item.name}" onclick="showFullImage('${item.image}')">
            <div class="product-info">
                <h3 class="product-name">${item.name}</h3>
                <p class="product-description">${item.description}</p>
                <p class="product-price">${item.price}</p>
                <button class="buy-button" onclick="addToCart('${item.name}', '${item.price}')">Pirkt</button>
            </div>
        </div>
    `).join('');
}

async function showCollection(collectionId) {
    try {
        const response = await fetch(`/api/collections?id=${encodeURIComponent(collectionId)}`);
        if (!response.ok) {
            console.error('Collection not found');
            return;
        }
        const collection = await response.json();

        currentCollection = collection;
        currentFilter = 'all';

        document.querySelectorAll('.filter-button').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector('.filter-button').classList.add('active');

        modalTitle.textContent = collection.title;
        renderCollection(collection, 'all');

        collectionModal.style.display = 'block';
        document.body.style.overflow = 'hidden';
    } catch (err) {
        console.error('Error loading collection', err);
    }
    
}
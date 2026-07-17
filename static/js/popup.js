// ============================================
// Restaurant Ordering System - Popup
// ============================================

document.addEventListener("DOMContentLoaded", function () {

    // Modal Elements
    const modal = document.getElementById("foodModal");
    const closeBtn = document.getElementById("closeModal");

    const modalImage = document.getElementById("modalImage");
    const modalName = document.getElementById("modalName");
    const modalRating = document.getElementById("modalRating");
    const modalPrice = document.getElementById("modalPrice");
    const modalDescription = document.getElementById("modalDescription");
    const modalCartLink = document.getElementById("modalCartLink");

    const favoriteBtn = document.getElementById("favoriteBtn");
    const popularBadge = document.getElementById("popularBadge");

    // Quick View Buttons
    const viewButtons = document.querySelectorAll(".view-btn");

    let favorite = false;

    // ===============================
    // Open Popup
    // ===============================

    viewButtons.forEach(function(button){

        button.addEventListener("click", function(){

            const card = this.closest(".menu-item");

            if(!card) return;

            modalImage.src = card.dataset.image;
            modalName.textContent = card.dataset.name;
            modalRating.textContent = "⭐ " + card.dataset.rating;
            modalPrice.textContent = "$" + parseFloat(card.dataset.price).toFixed(2);
            modalDescription.textContent = card.dataset.description;

            modalCartLink.href = "/add_to_cart/" + card.dataset.id;

            // Popular Badge
            if(card.querySelector(".popular-badge")){
                popularBadge.style.display = "inline-block";
            }else{
                popularBadge.style.display = "none";
            }

            modal.style.display = "flex";

        });

    });

    // ===============================
    // Close Button
    // ===============================

    closeBtn.addEventListener("click", function(){

        modal.style.display = "none";

    });

    // ===============================
    // Click Outside Modal
    // ===============================

    window.addEventListener("click", function(e){

        if(e.target === modal){

            modal.style.display = "none";

        }

    });

    // ===============================
    // ESC Key
    // ===============================

    document.addEventListener("keydown", function(e){

        if(e.key === "Escape"){

            modal.style.display = "none";

        }

    });

    // ===============================
    // Favorite Button
    // ===============================

    favoriteBtn.addEventListener("click", function(){

        favorite = !favorite;

        if(favorite){

            favoriteBtn.textContent = "❤️";

        }else{

            favoriteBtn.textContent = "🤍";

        }

    });

});
document.addEventListener("DOMContentLoaded", function () {

    console.log("✅ menu.js loaded");

    const searchInput = document.getElementById("searchInput");
    const categoryButtons = document.querySelectorAll(".category-btn");
    const menuItems = document.querySelectorAll(".menu-item");
    const noResult = document.getElementById("noResult");

    let selectedCategory = "all";

    function filterMenu() {

        const searchText = searchInput
            ? searchInput.value.toLowerCase().trim()
            : "";

        let visible = 0;

        menuItems.forEach(function(item){

            const name = item.dataset.name.toLowerCase();
            const category = item.dataset.category.toLowerCase();

            const searchMatch = name.includes(searchText);

            const categoryMatch =
                selectedCategory === "all" ||
                category === selectedCategory;

            if(searchMatch && categoryMatch){

                item.style.display = "";

                visible++;

            }else{

                item.style.display = "none";

            }

        });

        if(noResult){

            noResult.style.display =
                visible === 0 ? "block" : "none";

        }

    }

    if(searchInput){

        searchInput.addEventListener("input", filterMenu);

    }

    categoryButtons.forEach(function(btn){

        btn.addEventListener("click", function(){

            document
                .querySelector(".category-btn.active")
                ?.classList.remove("active");

            this.classList.add("active");

            selectedCategory = this.dataset.category;

            filterMenu();

        });

    });

    filterMenu();

});
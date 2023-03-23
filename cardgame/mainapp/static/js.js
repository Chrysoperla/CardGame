const card_boxes = document.querySelectorAll("div.card")


function paint_cards(){
    for (let card of card_boxes) {
        if (card.classList.contains("R") ){
            card.style.backgroundColor = "#ff7c73";
        }
        if (card.classList.contains("B") ){
            card.style.backgroundColor = "#739dff";
        }
        if (card.classList.contains("G") ){
            card.style.backgroundColor = "#73ff85";
        }
    }

};

paint_cards();
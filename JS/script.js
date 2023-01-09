modal = document.querySelector(".modal");

adjectives_dialog = document.getElementById("adjectives");
nouns_dialog = document.getElementById("nouns");
verbs_dialog = document.getElementById("verbs");
miscellanies_dialog = document.getElementById("miscellanies");

document.querySelectorAll("[id^='adjective-']").forEach(adjective_placeholder => {
  console.log(adjective_placeholder.id)
  adjective_placeholder.addEventListener('click', function() {
    modal.style.display = "block";
    adjectives_dialog.style.display = "inline";
    nouns_dialog.style.display = "none";
    verbs_dialog.style.display = "none";
    miscellanies_dialog.style.display = "none";
    document.querySelector("#adjectives").setAttribute("data-name", adjective_placeholder.id);

    map_my_modal('adjectives');
  });
});

document.querySelectorAll("[id^='noun-']").forEach(noun_placeholder => {
  console.log(noun_placeholder.id)
  noun_placeholder.addEventListener('click', function() {
    modal.style.display = "block";
    adjectives_dialog.style.display = "none";
    nouns_dialog.style.display = "inline";
    verbs_dialog.style.display = "none";
    miscellanies_dialog.style.display = "none";
    
    document.querySelector('#nouns').setAttribute("data-name", noun_placeholder.id);
    
    map_my_modal('nouns');    
  });
});

document.querySelectorAll("[id^='verb-']").forEach(verb_placeholder => {  
  console.log(verb_placeholder.id)
  verb_placeholder.addEventListener('click', function() {
    modal.style.display = "block";
    adjectives_dialog.style.display = "none";
    nouns_dialog.style.display = "none";
    verbs_dialog.style.display = "inline";
    miscellanies_dialog.style.display = "none";
    
    document.querySelector('#verbs').setAttribute("data-name", verb_placeholder.id);
    
    map_my_modal('verbs');
  });
});

document.querySelectorAll("[id^='miscellany-']").forEach(miscellany_placeholder => {
  console.log(miscellany_placeholder.id)
  miscellany_placeholder.addEventListener('click', function() {
    modal.style.display = "block";
    adjectives_dialog.style.display = "none";
    nouns_dialog.style.display = "none";
    verbs_dialog.style.display = "none";
    miscellanies_dialog.style.display = "inline";
    document.querySelector("#miscellanies").setAttribute("data-name", miscellany_placeholder.id);
    
    map_my_modal("miscellanies");      
  })
})
                                            
mapper_dict = {
  adjectives: {
    panel: "#adjectives",
    options: ".adjective-words"
  },
  nouns: {
    panel: '#nouns',
    options: ".noun-words"
  },
  verbs: {
    panel: '#verbs',
    options: ".verb-words"
  },
  miscellanies: {
    panel: "#miscellanies",
    options: ".miscellany-words"
  } 
}

map_my_modal = function(place_type) {
  my_mad_lib = document.getElementById(document.querySelector(mapper_dict[place_type].panel).getAttribute("data-name"));
  document.querySelectorAll(mapper_dict[place_type].options).forEach(adjective => {
    adjective.addEventListener('click', function() {       
      my_mad_lib.innerHTML = adjective.innerHTML;
      modal.style.display = "none";
    });
  });
}



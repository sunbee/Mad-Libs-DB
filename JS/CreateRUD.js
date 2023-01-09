var del_el = function() {
  /*
  Get the following elements:
  el_me: the span el with minus sign that triggered this callback
  el_mysibin: the associated input el for deletion
  el_mysibbr: the break el 
  el_parent: he enclosing div tag for the input els in this group
  */  
  var el_me = event.target
  var el_mysibin = el_me.previousElementSibling
  var el_mysibbr = el_mysibin.previousElementSibling
  var el_parent = el_me.parentNode
  
  el_parent.removeChild(el_me)
  el_parent.removeChild(el_mysibin)
  el_parent.removeChild(el_mysibbr)
};

$('.del').on('click', del_el)

$('.add').on('click', function() {
    /*
    Get the following elements:
    el_me: the span el with plus sign that triggered this callback
    el_parent: the enclosing div tag for the input els in this group
    el_sibins: all the input els in the group
    el_lastsibin: the last input el in the group
    Note: The event that is the target of the callback is available to use in the callback function as shown.
    */
    var el_me = event.target
    var el_parent = el_me.parentNode
    var el_sibins = el_parent.getElementsByTagName('input')
    var el_lastsibin = el_sibins[el_sibins.length-1]
    
    /*
    Mint the name/id for the new input el based on the name/id of the last input el in the group. Use regex to do this. The  name for reference is obtained in the prev. step.
    Note: 
    Use a regex to delete all non-digit characters, leaving only the number. Then use this result in a regex to replace the old number with the new number, which is the old number incremented by 1.
    To avoid the number being treated as string when incrementing, prepend a plus sign to the regex that extracts the number.
    */
    var name_lastsibin = el_lastsibin.getAttribute('name')
    console.log(name_lastsibin)
    var name_input = name_lastsibin.replace(/\d+$/, +name_lastsibin.replace(/^\D+/, '')+1)
    console.log(name_input)
    
    /*
    Create a new input el and set attributes including class, name and id. The name and id are from prev. step.
    */
    var el_br = document.createElement("br")
    var el_span = document.createElement("span")
    el_span.classList.add('fa', 'fa-minus', 'del')
    el_span.addEventListener('click', del_el)
    var el_input = document.createElement("input")
    el_input.setAttribute('type', 'text')
    el_input.setAttribute('id', name_input)
    el_input.setAttribute('name', name_input)
    el_input.required = true
    
    /*
    Insert the new input el before the span el with the plus sign, including a break el for separation.
    */
    console.log(el_input)
    el_me.before(el_span)
    el_me.before(el_br)
    el_me.before(el_input)
  });

$("textarea").each(function () {
  this.setAttribute("style", "height:" + (this.scrollHeight) + "px;overflow-y:hidden;width:60%;min-height:180px;");
}).on("input", function () {
  this.style.height = 0;
  this.style.height = (this.scrollHeight) + "px";
});